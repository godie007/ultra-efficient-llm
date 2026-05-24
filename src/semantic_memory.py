"""
Memoria semántica de ejemplos (recuperación por embeddings).

Es la pieza que materializa "dar ejemplos y conectar conceptos" con pocos datos:
en vez de coincidencia léxica exacta (como el índice n-grama), guarda cada ejemplo
como un vector de significado y recupera los conceptualmente más cercanos a una
consulta —aunque no compartan palabras—. Esos ejemplos recuperados se le pasan al
modelo neuronal en el contexto (few-shot), que es quien "conecta los conceptos".

Usa all-MiniLM-L6-v2 directamente vía `transformers` (mean-pooling), sin añadir la
dependencia `sentence-transformers`. Las dependencias pesadas se importan perezosamente.
"""

from typing import List, Optional, Tuple

_DEPS_AVAILABLE: Optional[bool] = None


def _deps_available() -> bool:
    global _DEPS_AVAILABLE
    if _DEPS_AVAILABLE is None:
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
            _DEPS_AVAILABLE = True
        except ImportError:
            _DEPS_AVAILABLE = False
    return _DEPS_AVAILABLE


class SemanticMemory:
    """Almacena ejemplos como embeddings y recupera los más relevantes por coseno."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
    ):
        if not _deps_available():
            raise ImportError(
                "torch/transformers no disponibles. Instala con: "
                "pip install -r requirements-neural.txt"
            )
        import torch
        from transformers import AutoModel, AutoTokenizer

        self._torch = torch
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

        self.examples: List[str] = []
        self._embeddings = None  # tensor (N, dim), L2-normalizado

    @staticmethod
    def available() -> bool:
        return _deps_available()

    def _embed(self, texts: List[str]):
        """Embeddings normalizados (mean-pooling sobre los tokens, receta estándar MiniLM)."""
        torch = self._torch
        encoded = self.tokenizer(
            texts, padding=True, truncation=True, return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            output = self.model(**encoded)
        token_embeddings = output[0]  # (batch, seq, dim)
        mask = encoded["attention_mask"].unsqueeze(-1).float()
        summed = (token_embeddings * mask).sum(dim=1)
        counts = mask.sum(dim=1).clamp(min=1e-9)
        mean_pooled = summed / counts
        return torch.nn.functional.normalize(mean_pooled, p=2, dim=1)

    def add(self, texts: List[str]) -> None:
        """Añade ejemplos a la memoria."""
        if not texts:
            return
        torch = self._torch
        new_embeddings = self._embed(texts)
        self.examples.extend(texts)
        if self._embeddings is None:
            self._embeddings = new_embeddings
        else:
            self._embeddings = torch.cat([self._embeddings, new_embeddings], dim=0)

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Devuelve los `top_k` ejemplos más similares a `query` (coseno descendente)."""
        if self._embeddings is None or not self.examples:
            return []
        torch = self._torch
        query_embedding = self._embed([query])  # (1, dim)
        # Coseno = producto punto porque los vectores están normalizados.
        similarities = (self._embeddings @ query_embedding.T).squeeze(1)
        k = min(top_k, len(self.examples))
        top_values, top_indices = torch.topk(similarities, k)
        return [
            (self.examples[idx], float(score))
            for score, idx in zip(top_values.tolist(), top_indices.tolist())
        ]
