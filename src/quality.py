"""
Validación de calidad del asistente RAG.

Mide dos cosas medibles automáticamente, sobre el corpus y el set de evaluación de
`data/corpus/`:

1. **Calidad de recuperación**: ¿la memoria semántica trae los documentos correctos para
   cada pregunta? (precision@k, recall@k, MRR). Es determinista y valida el núcleo "dar
   ejemplos y conectar conceptos".
2. **Calidad de respuesta**: similitud semántica (coseno de embeddings) entre la respuesta
   generada y una respuesta de referencia profesional. Sirve como proxy automatizable de
   "respuesta de calidad profesional".

La calidad de respuesta depende del modelo base: distilgpt2 da puntajes bajos; un modelo
instruido pequeño (Qwen2.5-0.5B-Instruct, vía RAG_MODEL) los sube mucho.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

CORPUS_DIR = Path(__file__).parent.parent / "data" / "corpus"
KNOWLEDGE_PATH = CORPUS_DIR / "knowledge_base.json"
EVAL_PATH = CORPUS_DIR / "qa_eval.json"


def load_corpus(path: Path = KNOWLEDGE_PATH) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["documents"]


def load_eval(path: Path = EVAL_PATH) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["cases"]


def evaluate_retrieval(
    memory,
    id_by_text: Dict[str, str],
    cases: List[Dict],
    top_k: int = 3,
) -> Dict[str, float]:
    """Calidad de recuperación: precision@k, recall@k, hit rate y MRR sobre el set."""
    precisions, recalls, hits, reciprocal_ranks = [], [], [], []

    for case in cases:
        relevant = set(case["relevant_ids"])
        retrieved = memory.retrieve(case["question"], top_k=top_k)
        retrieved_ids = [id_by_text.get(text) for text, _score in retrieved]

        found = [rid for rid in retrieved_ids if rid in relevant]
        precisions.append(len(found) / max(len(retrieved_ids), 1))
        recalls.append(len(set(found)) / max(len(relevant), 1))
        hits.append(1.0 if found else 0.0)

        rank = next((i + 1 for i, rid in enumerate(retrieved_ids) if rid in relevant), 0)
        reciprocal_ranks.append(1.0 / rank if rank else 0.0)

    n = max(len(cases), 1)
    return {
        "precision_at_k": sum(precisions) / n,
        "recall_at_k": sum(recalls) / n,
        "hit_rate": sum(hits) / n,
        "mrr": sum(reciprocal_ranks) / n,
        "top_k": top_k,
        "num_cases": len(cases),
    }


def _cosine(memory, text_a: str, text_b: str) -> float:
    """Similitud coseno entre dos textos usando el embebedor de la memoria semántica."""
    embeddings = memory._embed([text_a, text_b])  # normalizados
    return float((embeddings[0] * embeddings[1]).sum().item())


def evaluate_answers(
    rag,
    memory,
    cases: List[Dict],
    threshold: float = 0.5,
    max_new_tokens: int = 80,
) -> Dict:
    """Calidad de respuesta: similitud generada-vs-referencia y tasa de aprobados."""
    similarities = []
    details = []

    for case in cases:
        answer, _retrieved = rag.generate(
            case["question"], max_new_tokens=max_new_tokens, temperature=0.3
        )
        similarity = _cosine(memory, answer, case["reference_answer"])
        similarities.append(similarity)
        details.append({
            "question": case["question"],
            "answer": answer,
            "reference": case["reference_answer"],
            "similarity": similarity,
        })

    n = max(len(cases), 1)
    passed = sum(1 for s in similarities if s >= threshold)
    return {
        "mean_similarity": sum(similarities) / n,
        "pass_rate": passed / n,
        "threshold": threshold,
        "num_cases": len(cases),
        "details": details,
    }


def print_quality_report(retrieval: Dict, answers: Dict = None) -> None:
    print("\n" + "=" * 60)
    print("✅ VALIDACIÓN DE CALIDAD")
    print("=" * 60)
    print(f"🔎 Recuperación (top-{retrieval['top_k']}, {retrieval['num_cases']} casos):")
    print(f"   precision@k: {retrieval['precision_at_k']:.2f}")
    print(f"   recall@k   : {retrieval['recall_at_k']:.2f}")
    print(f"   hit rate   : {retrieval['hit_rate']:.2f}")
    print(f"   MRR        : {retrieval['mrr']:.2f}")

    if answers:
        print(f"\n💬 Respuestas ({answers['num_cases']} casos):")
        print(f"   similitud media vs referencia: {answers['mean_similarity']:.2f}")
        print(f"   tasa de aprobados (>= {answers['threshold']}): {answers['pass_rate']:.0%}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        from .semantic_memory import SemanticMemory
        from .neural_backbone import NeuralBackbone
        from .rag import RAGGenerator
    except ImportError:
        from semantic_memory import SemanticMemory
        from neural_backbone import NeuralBackbone
        from rag import RAGGenerator

    if not SemanticMemory.available():
        print("ℹ️  Instala requirements-neural.txt para la validación de calidad.")
        raise SystemExit(0)

    documents = load_corpus()
    cases = load_eval()
    id_by_text = {doc["text"]: doc["id"] for doc in documents}

    print(f"📚 Corpus: {len(documents)} documentos | Evaluación: {len(cases)} preguntas")
    print("🔌 Cargando memoria semántica (all-MiniLM-L6-v2)...")
    memory = SemanticMemory()
    memory.add([doc["text"] for doc in documents])
    print(f"   Dispositivo: {memory.device}")

    retrieval = evaluate_retrieval(memory, id_by_text, cases, top_k=3)

    model_name = os.environ.get("RAG_MODEL", "distilgpt2")
    print(f"🔌 Cargando modelo de generación: {model_name} ...")
    backbone = NeuralBackbone(model_name)
    print(f"   Instruido: {backbone.instruct} | Dispositivo: {backbone.device}")
    rag = RAGGenerator(memory, backbone, top_k=3)

    answers = evaluate_answers(rag, memory, cases, threshold=0.5)
    print_quality_report(retrieval, answers)

    # Muestra de una respuesta para inspección cualitativa
    sample = answers["details"][0]
    print("\n📝 Ejemplo de respuesta:")
    print(f"   ❓ {sample['question']}")
    print(f"   💬 {sample['answer']}")
    print(f"   📌 Referencia: {sample['reference']}")
    print(f"   📊 Similitud: {sample['similarity']:.2f}")
