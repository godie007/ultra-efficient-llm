"""
Backbone neuronal pequeño para augmentar el motor n-grama (Etapa 2).

El n-grama aporta recall exacto y barato pero no generaliza. Un modelo neuronal
pequeño (por defecto distilgpt2, ~82M parámetros, corre en CPU) aporta la
generalización. Aquí solo exponemos la distribución del siguiente token; la
interpolación n-grama↔neuronal vive en `hybrid.py`.

Las dependencias pesadas (torch/transformers) se importan de forma perezosa: el
resto del proyecto sigue funcionando sin ellas (motor n-grama solo).
"""

from typing import List, Optional, Tuple

_DEPS_AVAILABLE: Optional[bool] = None


def _deps_available() -> bool:
    """Comprueba (y cachea) si torch + transformers están disponibles."""
    global _DEPS_AVAILABLE
    if _DEPS_AVAILABLE is None:
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
            _DEPS_AVAILABLE = True
        except ImportError:
            _DEPS_AVAILABLE = False
    return _DEPS_AVAILABLE


class NeuralBackbone:
    """Envuelve un LM causal pequeño y expone la distribución del siguiente token."""

    def __init__(self, model_name: str = "distilgpt2", device: Optional[str] = None,
                 instruct: Optional[bool] = None):
        if not _deps_available():
            raise ImportError(
                "torch/transformers no disponibles. Instala con: "
                "pip install -r requirements-neural.txt"
            )
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._torch = torch
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Modelos instruidos (Qwen-Instruct, Gemma-it, etc.) generan respuestas de mayor
        # calidad usando su plantilla de chat. Se autodetecta por el nombre si no se indica.
        if instruct is None:
            name = model_name.lower()
            instruct = ("instruct" in name or "chat" in name or "-it" in name)
        self.instruct = instruct and getattr(self.tokenizer, "chat_template", None) is not None

    @staticmethod
    def available() -> bool:
        """True si el backbone puede instanciarse (dependencias presentes)."""
        return _deps_available()

    def next_token_probs(self, context: str):
        """Probabilidades softmax sobre el vocabulario BPE para el siguiente token.

        Una sola pasada hacia adelante. Devuelve un tensor 1D (tamaño del vocabulario)
        que el llamador puede reutilizar para varias consultas (top-k y lookups).
        """
        torch = self._torch
        if context and context.strip():
            input_ids = self.tokenizer(context, return_tensors="pt").input_ids
        else:
            # Contexto vacío: arrancar desde el token de fin/inicio de secuencia.
            input_ids = torch.tensor([[self.tokenizer.eos_token_id]])
        input_ids = input_ids.to(self.device)
        with torch.no_grad():
            logits = self.model(input_ids).logits[0, -1, :]
        return torch.softmax(logits, dim=-1)

    def prob_of_word(self, probs, word: str) -> float:
        """Probabilidad (aprox.) que el modelo asigna a `word` como siguiente palabra.

        GPT-2 usa BPE con espacio inicial; aproximamos por la probabilidad del primer
        sub-token de ' word'. Suficiente para interpolar a nivel de palabra con el n-grama.
        """
        ids = self.tokenizer(" " + word, add_special_tokens=False).input_ids
        if not ids:
            return 0.0
        return float(probs[ids[0]].item())

    def top_words(self, probs, top_k: int = 20) -> List[Tuple[str, float]]:
        """Top-k siguientes palabras del modelo, decodificando los tokens más probables."""
        torch = self._torch
        top_values, top_indices = torch.topk(probs, top_k)
        words: List[Tuple[str, float]] = []
        for prob, idx in zip(top_values.tolist(), top_indices.tolist()):
            token = self.tokenizer.decode([idx]).strip().lower()
            if token:
                words.append((token, prob))
        return words

    def generate_text(self, prompt: str, max_new_tokens: int = 40,
                      temperature: float = 0.7,
                      system: Optional[str] = None) -> str:
        """Genera una respuesta para `prompt` (solo los tokens nuevos).

        Usado por el generador RAG: el prompt incluye los ejemplos recuperados y el modelo
        genera condicionado a ellos. Si el modelo es instruido, usa su plantilla de chat
        (mejor calidad); si no, genera como continuación libre.
        """
        torch = self._torch

        if self.instruct:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            input_ids = self.tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, return_tensors="pt"
            ).to(self.device)
            attention_mask = torch.ones_like(input_ids)
        else:
            encoded = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            input_ids = encoded["input_ids"]
            attention_mask = encoded["attention_mask"]

        with torch.no_grad():
            output = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=0.95,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        new_tokens = output[0][input_ids.shape[1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
