"""
Tests del asistente RAG: recuperación semántica, generación y calidad.

Requieren torch/transformers y descargan modelos pequeños, así que son opt-in:
ejecuta con RUN_NEURAL_TESTS=1. Sin esa variable se omiten para mantener la suite ligera.

    RUN_NEURAL_TESTS=1 python -m unittest discover -s tests
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.semantic_memory import SemanticMemory
from src.neural_backbone import NeuralBackbone
from src.rag import RAGGenerator
from src.quality import load_corpus, load_eval, evaluate_retrieval

NEURAL = SemanticMemory.available() and os.environ.get("RUN_NEURAL_TESTS")


@unittest.skipUnless(NEURAL, "Define RUN_NEURAL_TESTS=1 con torch/transformers")
class TestSemanticMemory(unittest.TestCase):
    def setUp(self):
        self.memory = SemanticMemory()
        self.memory.add([
            "Neural networks are trained with backpropagation.",
            "Mitochondria produce energy for the cell.",
            "The French Revolution began in 1789.",
        ])

    def test_retrieval_is_semantic(self):
        results = self.memory.retrieve("How do machines learn from data?", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("neural networks", results[0][0].lower())

    def test_set_documents_rebuilds(self):
        self.memory.set_documents(["Quantization shrinks model size."])
        results = self.memory.retrieve("how to make a model smaller", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("quantization", results[0][0].lower())

    def test_empty_memory_returns_empty(self):
        self.assertEqual(SemanticMemory().retrieve("cualquier cosa"), [])


@unittest.skipUnless(NEURAL, "Define RUN_NEURAL_TESTS=1 con torch/transformers")
class TestRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory = SemanticMemory()
        cls.memory.add([
            "Neural networks are trained with backpropagation and gradient descent.",
            "Retrieval-augmented generation answers using retrieved documents.",
        ])
        cls.rag = RAGGenerator(cls.memory, NeuralBackbone("distilgpt2"), top_k=2)

    def test_generate_returns_answer_and_sources(self):
        answer, retrieved = self.rag.generate("How are neural networks trained?", max_new_tokens=20)
        self.assertIsInstance(answer, str)
        self.assertGreater(len(retrieved), 0)


@unittest.skipUnless(NEURAL, "Define RUN_NEURAL_TESTS=1 con torch/transformers")
class TestQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = load_corpus()
        cls.cases = load_eval()
        cls.id_by_text = {doc["text"]: doc["id"] for doc in cls.documents}
        cls.memory = SemanticMemory()
        cls.memory.add([doc["text"] for doc in cls.documents])

    def test_retrieval_quality(self):
        result = evaluate_retrieval(self.memory, self.id_by_text, self.cases, top_k=3)
        self.assertGreaterEqual(result["hit_rate"], 0.8)
        self.assertGreaterEqual(result["recall_at_k"], 0.6)


if __name__ == "__main__":
    unittest.main()
