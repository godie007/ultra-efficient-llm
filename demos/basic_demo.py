"""
Demo básico para testing rápido de UltraEfficientLLM
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ultra_efficient_llm import UltraEfficientLLM
from data_processor import DataProcessor
from utils import setup_logging, print_efficiency_report, Timer


def basic_demo():
    """Demo básico con textos de ejemplo"""
    print("=" * 50)
    print("🚀 DEMO BÁSICO - ULTRAEFFICIENTLLM")
    print("=" * 50)
    
    # Crear modelo con parámetros básicos
    model = UltraEfficientLLM(
        max_pattern_length=4,
        min_frequency=2,
        max_patterns=1000
    )
    
    # Obtener textos de ejemplo
    data_processor = DataProcessor()
    training_texts = data_processor.get_sample_texts()
    
    print(f"📚 Textos de entrenamiento: {len(training_texts)}")
    for i, text in enumerate(training_texts, 1):
        print(f"   {i}. {text}")
    
    # Entrenar modelo
    print("\n🧠 ENTRENAMIENTO:")
    with Timer("Entrenamiento básico"):
        model.train(training_texts)
    
    # Generar texto
    print("\n✨ GENERACIÓN DE TEXTO:")
    test_prompts = [
        "The quick",
        "Machine learning",
        "Artificial intelligence",
        "Deep learning"
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 Prompt: '{prompt}'")
        generated = model.generate(prompt, max_length=20, temperature=0.8)
        print(f"🎯 Generated: '{generated}'")
    
    # Reporte de eficiencia
    print("\n📊 REPORTE DE EFICIENCIA:")
    report = model.get_efficiency_report()
    
    print(f"   💾 Memoria: {report['memory_kb']:.2f} KB")
    print(f"   🚀 Mejora vs tradicional: {report['memory_improvement_vs_traditional']}")
    print(f"   🧮 Patrones: {report['patterns_stored']}")
    print(f"   ⚡ Sparsity: {report['sparsity_achieved']}")
    
    return model


def interactive_demo():
    """Demo interactivo para probar prompts personalizados"""
    print("\n" + "=" * 50)
    print("🎮 DEMO INTERACTIVO")
    print("=" * 50)
    
    # Crear modelo
    model = UltraEfficientLLM(
        max_pattern_length=5,
        min_frequency=2,
        max_patterns=2000
    )
    
    # Entrenar con textos de ejemplo
    data_processor = DataProcessor()
    training_texts = data_processor.get_sample_texts()
    model.train(training_texts)
    
    print("✅ Modelo entrenado y listo!")
    print("💡 Escribe 'quit' para salir")
    print("💡 Escribe 'stats' para ver estadísticas")
    
    while True:
        try:
            prompt = input("\n🎯 Tu prompt: ").strip()
            
            if prompt.lower() == 'quit':
                break
            elif prompt.lower() == 'stats':
                report = model.get_efficiency_report()
                print_efficiency_report(report)
                continue
            elif not prompt:
                continue
            
            # Generar texto
            generated = model.generate(prompt, max_length=30, temperature=0.9)
            print(f"🤖 Respuesta: {generated}")
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Función principal"""
    logger = setup_logging(level="INFO")
    
    try:
        # Demo básico
        model = basic_demo()
        
        # Preguntar si quiere demo interactivo
        response = input("\n¿Quieres probar el demo interactivo? (y/n): ").strip().lower()
        if response in ['y', 'yes', 'sí', 'si']:
            interactive_demo()
        
        print("\n✅ Demo completado exitosamente!")
        
    except Exception as e:
        logger.error(f"Error en el demo básico: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 