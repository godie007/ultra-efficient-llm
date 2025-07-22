"""
Tests para UltraEfficientLLM
"""

import sys
import os
import unittest

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ultra_efficient_llm import UltraEfficientLLM
from data_processor import DataProcessor
from utils import validate_model_parameters


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
        
        # Verificar que se crearon embeddings
        self.assertGreater(len(self.model.word_vectors), 0)
    
    def test_generation(self):
        """Test de generación de texto"""
        self.model.train(self.test_texts)
        
        prompt = "The quick"
        generated = self.model.generate(prompt, max_length=10, temperature=0.7)
        
        # Verificar que se generó algo
        self.assertIsNotNone(generated)
        self.assertIsInstance(generated, str)
        self.assertGreater(len(generated), len(prompt))
    
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


def run_tests():
    """Ejecuta todos los tests"""
    print("🧪 Ejecutando tests para UltraEfficientLLM...")
    
    # Crear test suite
    test_suite = unittest.TestSuite()
    
    # Agregar tests
    test_suite.addTest(unittest.makeSuite(TestUltraEfficientLLM))
    test_suite.addTest(unittest.makeSuite(TestDataProcessor))
    test_suite.addTest(unittest.makeSuite(TestUtils))
    
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