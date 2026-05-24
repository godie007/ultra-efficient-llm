"""
Modelo híbrido n-grama + neuronal (Etapa 2).

Interpola la distribución del siguiente token del motor n-grama (recall exacto y
barato sobre lo visto) con la de un backbone neuronal pequeño (generalización):

    P(w | contexto) = λ · P_ngrama(w) + (1 − λ) · P_neuronal(w)

Esta es la idea que Infini-gram (2024) validó: interpolar n-gramas con un LM neuronal
reduce la perplejidad. El componente caro (neuronal) se apoya en el barato (n-grama),
que ya resuelve las continuaciones frecuentes/exactas.

`HybridLLM` replica la interfaz mínima de `UltraEfficientLLM` (`_smart_tokenize`,
`next_token_distribution`, `generate`) para enchufarse sin cambios al evaluador.
"""

from typing import Dict


class HybridLLM:
    """Combina un UltraEfficientLLM entrenado con un NeuralBackbone."""

    def __init__(self, ngram_model, neural_backbone, lam: float = 0.5, top_k: int = 40):
        self.ngram_model = ngram_model
        self.neural = neural_backbone
        self.lam = lam  # peso del n-grama; (1 - lam) para el neuronal
        self.top_k = top_k

    @property
    def max_pattern_length(self) -> int:
        return self.ngram_model.max_pattern_length

    def _smart_tokenize(self, text: str):
        return self.ngram_model._smart_tokenize(text)

    def next_token_distribution(self, context: str) -> Dict[str, float]:
        """Distribución interpolada sobre un pool de candidatos.

        El pool son las palabras que propone el n-grama unidas al top-k del neuronal,
        de modo que el neuronal puede introducir palabras que el n-grama nunca vio
        (generalización) y el n-grama puede reforzar las que sí vio (recall).
        """
        ngram_dist = self.ngram_model.next_token_distribution(context)
        probs = self.neural.next_token_probs(context)
        neural_top = dict(self.neural.top_words(probs, self.top_k))

        candidates = set(ngram_dist) | set(neural_top)
        combined: Dict[str, float] = {}
        for word in candidates:
            p_ngram = ngram_dist.get(word, 0.0)
            p_neural = neural_top.get(word)
            if p_neural is None:
                p_neural = self.neural.prob_of_word(probs, word)
            combined[word] = self.lam * p_ngram + (1 - self.lam) * p_neural

        total = sum(combined.values())
        if total <= 0:
            return {}
        return {word: score / total for word, score in combined.items()}

    def generate(self, prompt: str, max_length: int = 20, temperature: float = 0.7) -> str:
        """Genera reutilizando el muestreo con anti-repetición del motor n-grama."""
        tokens = self.ngram_model._smart_tokenize(prompt)
        ctx_window = max(self.ngram_model.max_pattern_length - 1, 1)

        for _ in range(max_length):
            context = " ".join(tokens)
            distribution = self.next_token_distribution(context)
            if not distribution:
                break
            next_token = self.ngram_model._penalize_and_sample(
                distribution, tokens[-ctx_window:], temperature
            )
            if next_token is None:
                break
            tokens.append(next_token)

        return " ".join(tokens)
