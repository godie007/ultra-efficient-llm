#!/usr/bin/env python3
"""
UltraEfficientLLM - Punto de entrada principal
"""

import sys
import os
import argparse

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ultra_efficient_llm import UltraEfficientLLM
from data_processor import DataProcessor
from utils import setup_logging, print_efficiency_report, Timer


def main():
    """Función principal del programa"""
    parser = argparse.ArgumentParser(
        description="UltraEfficientLLM - Modelo de Lenguaje Ultra-Eficiente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                                    # Demo completo con Frankenstein
  python main.py --basic                            # Demo básico con textos de ejemplo
  python main.py --interactive                      # Demo interactivo
  python main.py --test                             # Ejecutar tests
  python main.py --inference --model models/frankenstein_model.pkl  # Inferencia con modelo guardado
  python main.py --save-model models/frankenstein_model.pkl         # Guardar modelo entrenado
        """
    )
    
    parser.add_argument(
        '--basic', 
        action='store_true',
        help='Ejecutar demo básico con textos de ejemplo'
    )
    
    parser.add_argument(
        '--interactive', 
        action='store_true',
        help='Ejecutar demo interactivo'
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Ejecutar tests del proyecto'
    )
    
    parser.add_argument(
        '--inference',
        action='store_true',
        help='Modo de inferencia con modelo guardado'
    )
    
    parser.add_argument(
        '--save-model',
        type=str,
        help='Ruta donde guardar el modelo entrenado'
    )
    
    parser.add_argument(
        '--load-model',
        type=str,
        help='Ruta del modelo a cargar para inferencia'
    )
    
    parser.add_argument(
        '--book-url',
        type=str,
        default="https://www.gutenberg.org/files/84/84-0.txt",
        help='URL del libro a descargar (default: Frankenstein)'
    )
    
    parser.add_argument(
        '--max-patterns',
        type=int,
        default=20000,
        help='Número máximo de patrones (default: 20000)'
    )
    
    parser.add_argument(
        '--min-frequency',
        type=int,
        default=5,
        help='Frecuencia mínima de patrones (default: 5)'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Prompt para generación (solo en modo inferencia)'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    logger = setup_logging(level="INFO")
    
    try:
        if args.test:
            # Ejecutar tests
            from tests.test_ultra_efficient_llm import run_tests
            success = run_tests()
            return 0 if success else 1
        
        elif args.basic:
            # Demo básico
            from examples.basic_demo import basic_demo
            model = basic_demo()
            return 0
        
        elif args.interactive:
            # Demo interactivo
            from examples.basic_demo import interactive_demo
            interactive_demo()
            return 0
        
        elif args.inference:
            # Modo de inferencia
            return run_inference_mode(args)
        
        else:
            # Demo completo con libro
            return run_book_demo(args)
    
    except KeyboardInterrupt:
        print("\n👋 Programa interrumpido por el usuario")
        return 0
    except Exception as e:
        logger.error(f"Error en el programa principal: {e}")
        print(f"❌ Error: {e}")
        return 1


def run_inference_mode(args):
    """Ejecuta el modo de inferencia con modelo guardado"""
    print("=" * 60)
    print("🤖 ULTRAEFFICIENTLLM - MODO INFERENCIA")
    print("=" * 60)
    
    # Verificar que se proporcionó un modelo
    model_path = args.load_model
    if not model_path:
        print("❌ Error: Debes especificar --load-model para el modo de inferencia")
        return 1
    
    # Crear modelo y cargar
    model = UltraEfficientLLM()
    
    try:
        model.load_model(model_path)
        
        # Mostrar información del modelo
        info = model.get_model_info()
        print(f"\n📊 Información del modelo:")
        print(f"   ✅ Entrenado: {info['is_trained']}")
        print(f"   🧮 Patrones: {info['patterns_count']}")
        print(f"   🔗 Contextos n-grama: {info['ngram_contexts']}")
        print(f"   💾 Memoria: {info['memory_usage_kb']:.2f} KB")
        
        if args.prompt:
            # Generar con prompt específico
            print(f"\n🎯 Generando con prompt: '{args.prompt}'")
            generated = model.generate(args.prompt, max_length=50, temperature=0.9)
            print(f"🤖 Respuesta: {generated}")
        else:
            # Modo interactivo de inferencia
            print("\n💡 Modo interactivo de inferencia")
            print("💡 Escribe 'quit' para salir")
            print("💡 Escribe 'info' para ver información del modelo")
            
            while True:
                try:
                    prompt = input("\n🎯 Tu prompt: ").strip()
                    
                    if prompt.lower() == 'quit':
                        break
                    elif prompt.lower() == 'info':
                        report = model.get_efficiency_report()
                        print_efficiency_report(report)
                        continue
                    elif not prompt:
                        continue
                    
                    # Generar texto
                    generated = model.generate(prompt, max_length=50, temperature=0.9)
                    print(f"🤖 Respuesta: {generated}")
                    
                except KeyboardInterrupt:
                    print("\n👋 ¡Hasta luego!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error en modo de inferencia: {e}")
        return 1


def run_book_demo(args):
    """Ejecuta el demo completo con libro"""
    print("=" * 60)
    print("🚀 ULTRAEFFICIENTLLM - DEMO COMPLETO CON LIBRO")
    print("=" * 60)
    
    # Crear procesador de datos
    data_processor = DataProcessor()
    
    # URL del libro
    book_url = args.book_url
    book_filename = 'data/books/frankenstein.txt'
    
    try:
        # Descargar y procesar el libro
        print(f"📥 Descargando libro desde: {book_url}")
        with Timer("Descarga y procesamiento del libro"):
            book_content = data_processor.download_book(book_url, book_filename)
        
        # Guardar contenido procesado
        processed_filename = 'data/books/frankenstein_processed.txt'
        data_processor.save_processed_data(book_content, processed_filename)
        
        # Crear modelo con parámetros personalizados
        model = UltraEfficientLLM(
            max_pattern_length=6,
            min_frequency=args.min_frequency,
            max_patterns=args.max_patterns
        )
        
        # Preparar datos de entrenamiento
        training_data_list = [line.strip() for line in book_content.splitlines() if line.strip()]
        print(f"📚 Datos de entrenamiento preparados: {len(training_data_list)} líneas")
        
        # Entrenar modelo
        print("\n🧠 ENTRENAMIENTO DEL MODELO:")
        with Timer("Entrenamiento completo"):
            model.train(training_data_list)
        
        # Guardar modelo si se especifica
        if args.save_model:
            model.save_model(args.save_model)
        
        # Generar texto con prompts temáticos
        print("\n✨ GENERACIÓN DE TEXTO:")
        test_prompts = [
            "The creature felt",
            "Victor Frankenstein",
            "I was miserable",
            "The laboratory was filled",
            "Nature surrounding me",
            "The monster said",
            "Electricity flowed through"
        ]
        
        for prompt in test_prompts:
            print(f"\n📝 Prompt: '{prompt}'")
            generated = model.generate(prompt, max_length=50, temperature=0.9)
            print(f"🎯 Generated: '{generated}'")
        
        # Reporte de recursos del motor n-grama
        print("\n" + "="*60)
        print("📊 RECURSOS DEL MOTOR N-GRAMA")
        print("="*60)

        report = model.get_efficiency_report()
        print_efficiency_report(report)

        print("\nℹ️  Recuerda: el motor n-grama recombina lo visto y NO generaliza.")
        print("   Para calidad real (perplejidad) y el híbrido neuronal: python src/evaluation.py")

        # Instrucciones para reutilizar el modelo
        if args.save_model:
            print(f"\n💡 Para reutilizar este modelo:")
            print(f"   python main.py --inference --load-model {args.save_model}")
            print(f"   python main.py --inference --load-model {args.save_model} --prompt 'Tu prompt aquí'")

        print("\n" + "="*60)
        print("✅ Demo del motor n-grama completado")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error en el demo con libro: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 