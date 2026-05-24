"""
Tests para UltraEfficientLLM
"""

import sys
import os
import math
import unittest

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ultra_efficient_llm import UltraEfficientLLM
from data_processor import DataProcessor
from utils import validate_model_parameters
from evaluation import compute_perplexity, measure_generation_speed
from neural_backbone import NeuralBackbone
from hybrid import HybridLLM
from semantic_memory import SemanticMemory
from rag import RAGGenerator


class TestUltraEfficientLLM(unittest.TestCase):
    """Tests para la clase UltraEfficientLLM"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.model = UltraEfficientLLM(
            max_pattern_length=3,
            min_frequency=2,
            max_patterns=100
        )
        
        self.test_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning is a subset of artificial intelligence.",
            "Natural language processing enables computers to understand human language."
        ]
    
    def test_model_initialization(self):
        """Test de inicialización del modelo"""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.max_pattern_length, 3)
        self.assertEqual(self.model.min_frequency, 2)
        self.assertEqual(self.model.max_patterns, 100)
        self.assertEqual(len(self.model.patterns), 0)
    
    def test_training(self):
        """Test de entrenamiento del modelo"""
        self.model.train(self.test_texts)
        
        # Verificar que se crearon patrones
        self.assertGreater(len(self.model.patterns), 0)
        self.assertGreater(self.model.stats['patterns_stored'], 0)

        # Verificar que se construyó el índice n-grama
        self.assertGreater(len(self.model.ngram_index), 0)
    
    def test_generation(self):
        """Test de generación de texto"""
        self.model.train(self.test_texts)
        
        prompt = "The quick"
        generated = self.model.generate(prompt, max_length=10, temperature=0.7)
        
        # Verificar que se generó algo
        self.assertIsNotNone(generated)
        self.assertIsInstance(generated, str)
        self.assertGreater(len(generated), len(prompt))
    
    def test_next_token_distribution(self):
        """Test de la distribución de probabilidad del siguiente token"""
        self.model.train(self.test_texts)

        # Contexto presente en los datos de entrenamiento
        distribution = self.model.next_token_distribution("machine learning")

        self.assertIsInstance(distribution, dict)
        # Si hay candidatos, debe ser una distribución de probabilidad válida
        if distribution:
            for prob in distribution.values():
                self.assertGreaterEqual(prob, 0.0)
                self.assertLessEqual(prob, 1.0)
            self.assertAlmostEqual(sum(distribution.values()), 1.0, places=6)

    def test_efficiency_report(self):
        """Test del reporte de eficiencia"""
        self.model.train(self.test_texts)
        
        report = self.model.get_efficiency_report()
        
        # Verificar que el reporte contiene las claves esperadas
        expected_keys = [
            'memory_kb', 'memory_improvement_vs_traditional',
            'patterns_stored', 'sparsity_achieved', 'cache_hit_rate',
            'activation_efficiency', 'average_activations_per_gen'
        ]
        
        for key in expected_keys:
            self.assertIn(key, report)
    
    def test_memory_stats(self):
        """Test de estadísticas de memoria"""
        self.model.train(self.test_texts)
        
        # Verificar que las estadísticas se actualizaron
        self.assertGreater(self.model.stats['memory_kb'], 0)
        self.assertGreater(self.model.stats['patterns_stored'], 0)


class TestDataProcessor(unittest.TestCase):
    """Tests para la clase DataProcessor"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.processor = DataProcessor()
    
    def test_sample_texts(self):
        """Test de textos de ejemplo"""
        texts = self.processor.get_sample_texts()
        
        self.assertIsInstance(texts, list)
        self.assertGreater(len(texts), 0)
        
        for text in texts:
            self.assertIsInstance(text, str)
            self.assertGreater(len(text), 0)
    
    def test_text_splitting(self):
        """Test de división de texto en chunks"""
        test_text = "This is a test text with multiple words to split into chunks."
        chunks = self.processor.split_into_chunks(test_text, chunk_size=5)
        
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)
        
        for chunk in chunks:
            self.assertIsInstance(chunk, str)
            self.assertGreater(len(chunk), 0)
    
    def test_gutenberg_cleaning(self):
        """Test de limpieza de contenido de Project Gutenberg"""
        # Simular contenido de Project Gutenberg
        raw_content = """
        *** START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN ***
        
        This is the actual book content.
        
        *** END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN ***
        """
        
        cleaned = self.processor._clean_gutenberg_content(raw_content)
        
        self.assertIsInstance(cleaned, str)
        self.assertNotIn("*** START OF THE PROJECT GUTENBERG EBOOK", cleaned)
        self.assertNotIn("*** END OF THE PROJECT GUTENBERG EBOOK", cleaned)
        self.assertIn("this is the actual book content", cleaned.lower())


class TestUtils(unittest.TestCase):
    """Tests para las utilidades"""
    
    def test_parameter_validation(self):
        """Test de validación de parámetros"""
        # Parámetros válidos
        self.assertTrue(validate_model_parameters(5, 2, 1000))
        
        # Parámetros inválidos
        self.assertFalse(validate_model_parameters(0, 2, 1000))  # max_pattern_length < 1
        self.assertFalse(validate_model_parameters(25, 2, 1000))  # max_pattern_length > 20
        self.assertFalse(validate_model_parameters(5, 0, 1000))   # min_frequency < 1
        self.assertFalse(validate_model_parameters(5, 2, 50))     # max_patterns < 100
        self.assertFalse(validate_model_parameters(5, 2, 200000)) # max_patterns > 100000


class TestEvaluation(unittest.TestCase):
    """Tests para el módulo de evaluación (perplejidad y velocidad)"""

    def setUp(self):
        self.model = UltraEfficientLLM(
            max_pattern_length=3,
            min_frequency=1,
            max_patterns=200
        )
        self.test_texts = [
            "Machine learning is a subset of artificial intelligence.",
            "Natural language processing enables computers to understand human language.",
            "Deep learning uses neural networks with multiple layers."
        ]
        self.model.train(self.test_texts)

    def test_perplexity_is_finite_and_positive(self):
        """La perplejidad debe ser finita y positiva sobre datos vistos"""
        result = compute_perplexity(self.model, self.test_texts)

        self.assertGreater(result["total_tokens_evaluated"], 0)
        self.assertGreater(result["perplexity"], 0.0)
        self.assertTrue(math.isfinite(result["perplexity"]))
        self.assertGreaterEqual(result["coverage"], 0.0)
        self.assertLessEqual(result["coverage"], 1.0)

    def test_generation_speed_measured(self):
        """La medición de velocidad debe reportar tokens/segundo positivos"""
        result = measure_generation_speed(
            self.model, ["Machine learning"], max_length=10
        )

        self.assertGreater(result["tokens_generated"], 0)
        self.assertGreaterEqual(result["tokens_per_second"], 0.0)


@unittest.skipUnless(
    NeuralBackbone.available() and os.environ.get("RUN_NEURAL_TESTS"),
    "Tests neuronales desactivados (define RUN_NEURAL_TESTS=1 con torch/transformers)"
)
class TestHybrid(unittest.TestCase):
    """Tests del modelo híbrido n-grama + neuronal (opt-in)"""

    def setUp(self):
        self.model = UltraEfficientLLM(
            max_pattern_length=3, min_frequency=1, max_patterns=200
        )
        self.model.train([
            "Machine learning is a subset of artificial intelligence.",
            "Neural networks learn from data."
        ])
        self.backbone = NeuralBackbone()
        self.hybrid = HybridLLM(self.model, self.backbone, lam=0.5)

    def test_hybrid_distribution_valid(self):
        """La distribución híbrida debe estar normalizada y no vacía"""
        dist = self.hybrid.next_token_distribution("machine learning")
        self.assertIsInstance(dist, dict)
        self.assertGreater(len(dist), 0)
        self.assertAlmostEqual(sum(dist.values()), 1.0, places=5)

    def test_hybrid_generation(self):
        """La generación híbrida debe producir texto"""
        out = self.hybrid.generate("machine learning", max_length=8)
        self.assertIsInstance(out, str)
        self.assertGreater(len(out.split()), 2)


@unittest.skipUnless(
    SemanticMemory.available() and os.environ.get("RUN_NEURAL_TESTS"),
    "Tests neuronales desactivados (define RUN_NEURAL_TESTS=1 con torch/transformers)"
)
class TestSemanticMemory(unittest.TestCase):
    """Tests de recuperación semántica (opt-in)"""

    def setUp(self):
        self.memory = SemanticMemory()
        self.memory.add([
            "Neural networks are trained using backpropagation and gradient descent.",
            "Mitochondria produce energy for the cell through respiration.",
            "Napoleon Bonaparte crowned himself Emperor of France in 1804.",
        ])

    def test_retrieval_is_semantic(self):
        """Una consulta sin palabras en común debe recuperar el ejemplo conceptual correcto"""
        results = self.memory.retrieve("How do machines learn from data?", top_k=1)
        self.assertEqual(len(results), 1)
        top_example = results[0][0].lower()
        # Debe traer el ejemplo de ML, no el de biología ni el de historia
        self.assertIn("neural networks", top_example)

    def test_retrieve_empty_memory(self):
        """Memoria vacía devuelve lista vacía sin error"""
        empty = SemanticMemory()
        self.assertEqual(empty.retrieve("cualquier cosa"), [])


def run_tests():
    """Ejecuta todos los tests"""
    print("🧪 Ejecutando tests para UltraEfficientLLM...")

    # Crear test suite
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    # Agregar tests
    test_suite.addTests(loader.loadTestsFromTestCase(TestUltraEfficientLLM))
    test_suite.addTests(loader.loadTestsFromTestCase(TestDataProcessor))
    test_suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    test_suite.addTests(loader.loadTestsFromTestCase(TestEvaluation))
    test_suite.addTests(loader.loadTestsFromTestCase(TestHybrid))
    test_suite.addTests(loader.loadTestsFromTestCase(TestSemanticMemory))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Reportar resultados
    print(f"\n📊 Resultados de los tests:")
    print(f"   ✅ Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Tests fallidos: {len(result.failures)}")
    print(f"   ⚠️ Tests con errores: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1) 