"""
Generación aumentada por recuperación (RAG) — Etapa 3.

Une los dos componentes baratos hacia la visión "dar ejemplos y conectar conceptos
con pocos datos":

  1. SemanticMemory recupera los ejemplos conceptualmente relevantes a la consulta.
  2. NeuralBackbone genera una respuesta condicionada a esos ejemplos (few-shot).

El conocimiento no se entrena: se aporta como ejemplos en memoria y el modelo
preentrenado pequeño los conecta en contexto. Añadir/quitar conocimiento = añadir/
quitar ejemplos (cero reentrenamiento), que es la eficiencia en datos buscada.
"""

from typing import List, Tuple


# System prompt para respuestas de calidad profesional, ancladas al conocimiento recuperado.
DEFAULT_SYSTEM_PROMPT = (
    "You are a professional technical assistant. Answer the question using ONLY the provided "
    "knowledge. Be concise, accurate and professional. If the knowledge does not cover the "
    "question, say so instead of inventing an answer."
)


class RAGGenerator:
    """Recupera ejemplos relevantes y genera condicionado a ellos."""

    def __init__(self, memory, backbone, top_k: int = 3,
                 system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.memory = memory
        self.backbone = backbone
        self.top_k = top_k
        self.system_prompt = system_prompt

    def build_prompt(self, query: str, retrieved: List[Tuple[str, float]]) -> str:
        """Construye un prompt few-shot con los ejemplos recuperados como contexto."""
        context = "\n".join(f"- {example}" for example, _score in retrieved)
        return (
            "Knowledge:\n"
            f"{context}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )

    def generate(self, query: str, max_new_tokens: int = 80, temperature: float = 0.7):
        """Devuelve (respuesta_generada, ejemplos_recuperados)."""
        retrieved = self.memory.retrieve(query, self.top_k)
        prompt = self.build_prompt(query, retrieved)
        answer = self.backbone.generate_text(
            prompt, max_new_tokens, temperature, system=self.system_prompt
        )
        return answer, retrieved


if __name__ == "__main__":
    try:
        from .semantic_memory import SemanticMemory
        from .neural_backbone import NeuralBackbone
    except ImportError:
        from semantic_memory import SemanticMemory
        from neural_backbone import NeuralBackbone

    if not SemanticMemory.available():
        print("ℹ️  Instala requirements-neural.txt para ejecutar el demo RAG.")
        raise SystemExit(0)

    # Base de conocimiento con tres clusters de conceptos distintos (sin solapamiento léxico
    # con las consultas) para demostrar que la recuperación es semántica, no de palabras.
    knowledge = [
        "Photosynthesis lets plants convert sunlight into chemical energy.",
        "Mitochondria produce energy for the cell through respiration.",
        "Neural networks are trained using backpropagation and gradient descent.",
        "Transformers rely on self-attention to capture long-range dependencies.",
        "The French Revolution began in 1789 and overthrew the monarchy.",
        "Napoleon Bonaparte crowned himself Emperor of France in 1804.",
    ]

    print("🔌 Cargando memoria semántica (all-MiniLM-L6-v2)...")
    memory = SemanticMemory()
    print(f"   Dispositivo: {memory.device}")
    memory.add(knowledge)

    queries = [
        "How do machines learn from data?",
        "What gives a cell its energy?",
        "Tell me about the history of France.",
    ]

    print("\n" + "=" * 60)
    print("🔎 RECUPERACIÓN SEMÁNTICA (la consulta no comparte palabras con los ejemplos)")
    print("=" * 60)
    for query in queries:
        print(f"\n❓ {query}")
        for example, score in memory.retrieve(query, top_k=2):
            print(f"   [{score:.3f}] {example}")

    print("\n" + "=" * 60)
    print("🧠 GENERACIÓN CONDICIONADA A LOS EJEMPLOS RECUPERADOS (few-shot)")
    print("=" * 60)
    backbone = NeuralBackbone()
    rag = RAGGenerator(memory, backbone, top_k=2)
    query = "How do machines learn from data?"
    answer, retrieved = rag.generate(query, max_new_tokens=40, temperature=0.7)
    print(f"\n❓ {query}")
    print("📚 Ejemplos usados:")
    for example, score in retrieved:
        print(f"   [{score:.3f}] {example}")
    print(f"💬 Respuesta (distilgpt2): {answer}")
    print("\nℹ️  La coherencia depende del modelo base; distilgpt2 es mínimo.")
    print("   Un modelo instruido pequeño (Qwen/Gemma 0.5-1B) mejora mucho esta parte.")
