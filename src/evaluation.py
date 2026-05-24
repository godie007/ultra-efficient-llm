"""
Evaluación honesta del UltraEfficientLLM.

Aporta las métricas que faltaban para que "eficiencia" signifique algo:
- Perplejidad: calidad real del modelo de lenguaje sobre texto de validación.
- Velocidad: tokens/segundo medidos (no estimados).

Sin una métrica de calidad, la memoria baja no dice nada: un modelo que devuelve
ruido usa poca memoria y sería "infinitamente eficiente". La perplejidad ata la
eficiencia a la utilidad. Es el baseline contra el que se medirán las siguientes
etapas (índice de sufijos, arquitectura híbrida).
"""

import io
import math
import time
from contextlib import redirect_stdout
from typing import Dict, List, Optional


def compute_perplexity(
    model,
    texts: List[str],
    context_window: int = 8,
    floor: float = 1e-9,
) -> Dict[str, float]:
    """Calcula la perplejidad del modelo sobre una lista de textos.

    Perplejidad = exp( -(1/N) * Σ log P(token_i | contexto) ). Más baja = mejor.

    Para tokens que el modelo no logra predecir (distribución vacía o token ausente)
    se aplica un piso de probabilidad `floor`. Esto penaliza la incapacidad de
    generalizar del n-grama —que es justamente lo que queremos medir—. El backoff
    real (Etapa 1) reducirá la dependencia de este piso.

    Args:
        model: objeto con `_smart_tokenize` y `next_token_distribution`.
        texts: textos de validación (idealmente NO vistos en entrenamiento).
        context_window: nº de tokens previos usados como contexto (igual que `generate`).
        floor: probabilidad mínima para tokens no predichos.

    Returns:
        dict con perplexity, total_tokens_evaluated, coverage (fracción de tokens
        a los que el modelo asignó probabilidad real > floor) y avg_log_prob.
    """
    total_nll = 0.0
    total_tokens = 0
    covered = 0

    for text in texts:
        tokens = model._smart_tokenize(text)
        for i in range(1, len(tokens)):
            context = " ".join(tokens[max(0, i - context_window):i])
            target = tokens[i]

            distribution = model.next_token_distribution(context)
            prob = distribution.get(target, 0.0)

            if prob > 0.0:
                covered += 1
            else:
                prob = floor

            total_nll += -math.log(max(prob, floor))
            total_tokens += 1

    if total_tokens == 0:
        return {
            "perplexity": float("inf"),
            "total_tokens_evaluated": 0,
            "coverage": 0.0,
            "avg_log_prob": float("-inf"),
        }

    avg_nll = total_nll / total_tokens
    return {
        "perplexity": math.exp(avg_nll),
        "total_tokens_evaluated": total_tokens,
        "coverage": covered / total_tokens,
        "avg_log_prob": -avg_nll,
    }


def measure_generation_speed(
    model,
    prompts: List[str],
    max_length: int = 30,
    temperature: float = 0.8,
) -> Dict[str, float]:
    """Mide tokens/segundo reales generando a partir de varios prompts.

    Silencia la salida de `generate` para no contaminar el reporte; lo que importa
    aquí es el tiempo de pared y el nº de tokens producidos.
    """
    total_tokens = 0
    start = time.perf_counter()

    sink = io.StringIO()
    with redirect_stdout(sink):
        for prompt in prompts:
            generated = model.generate(prompt, max_length=max_length, temperature=temperature)
            total_tokens += len(generated.split())

    elapsed = time.perf_counter() - start
    return {
        "tokens_generated": total_tokens,
        "elapsed_seconds": elapsed,
        "tokens_per_second": total_tokens / elapsed if elapsed > 0 else 0.0,
    }


def evaluate_model(
    model,
    eval_texts: List[str],
    gen_prompts: Optional[List[str]] = None,
) -> Dict[str, object]:
    """Ejecuta perplejidad + velocidad y devuelve un reporte combinado."""
    report: Dict[str, object] = {"quality": compute_perplexity(model, eval_texts)}
    if gen_prompts:
        report["speed"] = measure_generation_speed(model, gen_prompts)
    if hasattr(model, "get_model_info"):
        report["model_info"] = model.get_model_info()
    return report


def compare_perplexities(
    ngram_model,
    backbone,
    texts: List[str],
    lam: float = 0.5,
    context_window: int = 8,
    floor: float = 1e-9,
) -> Dict[str, float]:
    """Perplejidad pointwise de n-grama, neuronal e híbrido sobre el mismo texto.

    Comparación justa: para cada token objetivo se usa su probabilidad real bajo cada
    modelo (no un pool de candidatos top-k). Una sola pasada neuronal por posición,
    compartida entre el modelo neuronal y el híbrido.

    Híbrido: P(w) = lam · P_ngrama(w) + (1 − lam) · P_neuronal(w).
    """
    nll = {"ngram": 0.0, "neural": 0.0, "hybrid": 0.0}
    total = 0

    for text in texts:
        tokens = ngram_model._smart_tokenize(text)
        for i in range(1, len(tokens)):
            context = " ".join(tokens[max(0, i - context_window):i])
            target = tokens[i]

            p_ngram = ngram_model.next_token_distribution(context).get(target, 0.0)
            probs = backbone.next_token_probs(context)
            p_neural = backbone.prob_of_word(probs, target)
            p_hybrid = lam * p_ngram + (1 - lam) * p_neural

            nll["ngram"] += -math.log(max(p_ngram, floor))
            nll["neural"] += -math.log(max(p_neural, floor))
            nll["hybrid"] += -math.log(max(p_hybrid, floor))
            total += 1

    if total == 0:
        return {key: float("inf") for key in nll}
    return {key: math.exp(value / total) for key, value in nll.items()}


def print_comparison(perplexities: Dict[str, float]) -> None:
    """Imprime la tabla comparativa de perplejidad."""
    print("\n" + "=" * 60)
    print("⚖️  COMPARACIÓN DE PERPLEJIDAD (texto NO visto)")
    print("=" * 60)
    print(f"   N-grama solo : {perplexities.get('ngram', float('inf')):8.2f}")
    print(f"   Neuronal solo: {perplexities.get('neural', float('inf')):8.2f}")
    print(f"   Híbrido      : {perplexities.get('hybrid', float('inf')):8.2f}  (más baja = mejor)")
    print("=" * 60)


def print_evaluation(report: Dict[str, object]) -> None:
    """Imprime el reporte de evaluación de forma legible."""
    quality = report.get("quality", {})
    print("\n" + "=" * 60)
    print("📏 EVALUACIÓN HONESTA")
    print("=" * 60)
    print(f"📉 Perplejidad: {quality.get('perplexity', float('inf')):.2f}  (más baja = mejor)")
    print(f"🎯 Cobertura (tokens con prob. real): {quality.get('coverage', 0.0):.1%}")
    print(f"🔢 Tokens evaluados: {quality.get('total_tokens_evaluated', 0)}")

    speed = report.get("speed")
    if speed:
        print(f"⚡ Velocidad medida: {speed.get('tokens_per_second', 0.0):.1f} tokens/s")

    info = report.get("model_info")
    if info:
        print(f"🧮 Patrones: {info.get('patterns_count', 0)} | Memoria: {info.get('memory_usage_kb', 0):.1f} KB")
    print("=" * 60)


if __name__ == "__main__":
    try:
        from .ultra_efficient_llm import UltraEfficientLLM
        from .data_processor import DataProcessor
    except ImportError:
        from ultra_efficient_llm import UltraEfficientLLM
        from data_processor import DataProcessor

    print("🧪 Demo de evaluación (corpus de muestra, perplejidad in-sample)")
    print("⚠️  Nota: una evaluación rigurosa usa texto NO visto en entrenamiento.")

    processor = DataProcessor()
    sample_texts = processor.get_sample_texts()

    model = UltraEfficientLLM(max_pattern_length=4, min_frequency=1, max_patterns=2000)
    with redirect_stdout(io.StringIO()):  # silenciar logs de entrenamiento
        model.train(sample_texts)

    report = evaluate_model(
        model,
        eval_texts=sample_texts,
        gen_prompts=["Machine learning", "The future of"],
    )
    print_evaluation(report)

    # Etapa 2: comparación híbrida sobre texto NO visto (si hay backbone neuronal)
    try:
        from .neural_backbone import NeuralBackbone
        from .hybrid import HybridLLM
    except ImportError:
        from neural_backbone import NeuralBackbone
        from hybrid import HybridLLM

    if not NeuralBackbone.available():
        print("\nℹ️  Backbone neuronal no disponible (instala requirements-neural.txt)")
        print("   para ver la comparación n-grama vs neuronal vs híbrido.")
    else:
        held_out = [
            "Artificial intelligence will transform the future of science.",
            "Neural networks can learn complex patterns from data.",
            "Computers process language using statistical models.",
        ]
        print("\n🔌 Cargando backbone neuronal (distilgpt2)...")
        backbone = NeuralBackbone()
        print(f"   Dispositivo: {backbone.device}")

        perplexities = compare_perplexities(model, backbone, held_out, lam=0.5)
        print_comparison(perplexities)

        hybrid = HybridLLM(model, backbone, lam=0.5)
        with redirect_stdout(io.StringIO()):
            ngram_gen = model.generate("Artificial intelligence", max_length=12, temperature=0.7)
        hybrid_gen = hybrid.generate("Artificial intelligence", max_length=12, temperature=0.7)
        print("\n📝 Generación (prompt: 'Artificial intelligence'):")
        print(f"   N-grama: {ngram_gen}")
        print(f"   Híbrido: {hybrid_gen}")
