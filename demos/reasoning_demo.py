#!/usr/bin/env python3
"""
Demostración del Razonamiento del UltraEfficientLLM
Muestra paso a paso cómo funciona el proceso de razonamiento
"""

import sys
import os
import time
from typing import List, Dict, Tuple

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ultra_efficient_llm import UltraEfficientLLM


class ReasoningDemo:
    """Demostración del razonamiento del UltraEfficientLLM"""
    
    def __init__(self):
        self.model = UltraEfficientLLM(
            max_pattern_length=6,
            min_frequency=2,
            max_patterns=3000
        )
        self.trained = False
        
    def train_with_demo_data(self):
        """Entrenar con datos de demostración"""
        print("🧠 ENTRENANDO MODELO PARA DEMOSTRACIÓN DE RAZONAMIENTO")
        print("=" * 70)
        
        # Datos de entrenamiento que muestran diferentes tipos de razonamiento
        training_texts = [
            # Razonamiento sobre machine learning
            "machine learning is a subset of artificial intelligence",
            "machine learning uses algorithms to process data",
            "machine learning can predict future outcomes",
            "machine learning models learn from training data",
            "machine learning is used in many applications",
            
            # Razonamiento sobre inteligencia artificial
            "artificial intelligence is a field of computer science",
            "artificial intelligence aims to create intelligent systems",
            "artificial intelligence includes machine learning and deep learning",
            "artificial intelligence can solve complex problems",
            "artificial intelligence is transforming industries",
            
            # Razonamiento sobre correos electrónicos
            "dear recipient i hope this email finds you well",
            "thank you for your email and your consideration",
            "i am writing to request a meeting with you",
            "please let me know if you need any clarification",
            "i look forward to hearing from you soon",
            
            # Razonamiento sobre proyectos
            "the project is progressing well and on schedule",
            "we need to discuss the project timeline and budget",
            "the project team has made significant progress",
            "project deliverables will be completed on time",
            "project stakeholders are satisfied with the results",
            
            # Razonamiento sobre tecnología
            "technology is advancing rapidly in recent years",
            "new technology can improve efficiency and productivity",
            "technology companies are investing in innovation",
            "technology solutions can solve business problems",
            "technology trends are shaping the future"
        ]
        
        print("📚 Datos de entrenamiento:")
        for i, text in enumerate(training_texts, 1):
            print(f"   {i:2d}. {text}")
        
        print(f"\n🚀 Iniciando entrenamiento...")
        self.model.train(training_texts)
        self.trained = True
        
        print("\n✅ Modelo entrenado y listo para demostración de razonamiento")
    
    def demonstrate_pattern_extraction(self, text: str):
        """Demostrar extracción de patrones"""
        print(f"\n🧩 DEMOSTRACIÓN: Extracción de Patrones")
        print("-" * 50)
        print(f"Texto: '{text}'")
        
        # Simular extracción de patrones
        tokens = text.lower().split()
        patterns = []
        
        for n in range(1, min(4, len(tokens) + 1)):
            for i in range(len(tokens) - n + 1):
                pattern = " ".join(tokens[i:i+n])
                if len(pattern.split()) > 1 or pattern not in ['a', 'an', 'the', 'is', 'are', 'was', 'were']:
                    patterns.append(pattern)
        
        print(f"\nPatrones extraídos:")
        for i, pattern in enumerate(patterns, 1):
            print(f"   {i:2d}. '{pattern}'")
        
        return patterns
    
    def demonstrate_pattern_activation(self, context: str):
        """Demostrar activación de patrones"""
        print(f"\n⚡ DEMOSTRACIÓN: Activación de Patrones")
        print("-" * 50)
        print(f"Contexto: '{context}'")
        
        if not self.trained:
            print("❌ Modelo no entrenado. Ejecutando entrenamiento...")
            self.train_with_demo_data()
        
        # Obtener patrones activos del modelo
        active_patterns = self.model._get_active_patterns(context)
        
        print(f"\nPatrones activados:")
        if active_patterns:
            for i, (pattern, score) in enumerate(active_patterns[:5], 1):
                print(f"   {i}. '{pattern}' (score: {score:.3f})")
        else:
            print("   No se encontraron patrones activos")
        
        return active_patterns
    
    def demonstrate_reasoning_chain(self, prompt: str, steps: int = 5):
        """Demostrar cadena de razonamiento paso a paso"""
        print(f"\n🧠 DEMOSTRACIÓN: Cadena de Razonamiento")
        print("-" * 50)
        print(f"Prompt inicial: '{prompt}'")
        print(f"Pasos de razonamiento: {steps}")
        
        if not self.trained:
            print("❌ Modelo no entrenado. Ejecutando entrenamiento...")
            self.train_with_demo_data()
        
        result_tokens = self.model._smart_tokenize(prompt)
        print(f"\nTokens iniciales: {result_tokens}")
        
        print(f"\n📊 PROCESO DE RAZONAMIENTO PASO A PASO:")
        print("=" * 60)
        
        for step in range(steps):
            print(f"\n🔄 PASO {step + 1}:")
            
            # Obtener contexto
            context = " ".join(result_tokens[-8:])
            print(f"   Contexto: '{context}'")
            
            # Obtener patrones activos
            active_patterns = self.model._get_active_patterns(context)
            print(f"   Patrones activos: {len(active_patterns)}")
            
            if active_patterns:
                # Mostrar top 3 patrones
                for i, (pattern, score) in enumerate(active_patterns[:3], 1):
                    print(f"     {i}. '{pattern}' (score: {score:.3f})")
                
                # Predecir siguiente token
                next_token = self.model._predict_next_token(context, active_patterns, 0.7)
                if next_token:
                    result_tokens.append(next_token)
                    print(f"   → Predicción: '{next_token}'")
                    print(f"   → Resultado parcial: '{' '.join(result_tokens)}'")
                else:
                    print(f"   → No se pudo predecir siguiente token")
                    break
            else:
                print(f"   → No hay patrones activos, terminando...")
                break
        
        final_result = " ".join(result_tokens)
        print(f"\n🎯 RESULTADO FINAL: '{final_result}'")
        
        return final_result
    
    def demonstrate_different_contexts(self):
        """Demostrar razonamiento en diferentes contextos"""
        print(f"\n🎭 DEMOSTRACIÓN: Razonamiento en Diferentes Contextos")
        print("=" * 70)
        
        contexts = [
            "machine learning",
            "artificial intelligence",
            "dear recipient",
            "the project",
            "technology is"
        ]
        
        for context in contexts:
            print(f"\n📝 Contexto: '{context}'")
            print("-" * 40)
            
            # Mostrar patrones activos
            active_patterns = self.demonstrate_pattern_activation(context)
            
            # Mostrar razonamiento
            result = self.demonstrate_reasoning_chain(context, 3)
            
            print(f"✅ Razonamiento completado para '{context}'")
    
    def demonstrate_efficiency_metrics(self):
        """Demostrar métricas de eficiencia"""
        print(f"\n📊 DEMOSTRACIÓN: Métricas de Eficiencia")
        print("=" * 50)
        
        if not self.trained:
            print("❌ Modelo no entrenado. Ejecutando entrenamiento...")
            self.train_with_demo_data()
        
        # Obtener estadísticas del modelo
        stats = self.model.get_efficiency_report()
        
        print(f"\n📈 ESTADÍSTICAS DE EFICIENCIA:")
        print(f"   Patrones almacenados: {stats['patterns_stored']:,}")
        print(f"   Memoria utilizada: {stats['memory_kb']:.2f} KB")
        print(f"   Activaciones por generación: {stats['activations_per_generation']:.1f}")
        print(f"   Cache hits: {stats['cache_hits']}")
        print(f"   Total generaciones: {stats['total_generations']}")
        
        # Calcular sparsity
        if stats['patterns_stored'] > 0:
            sparsity = 1 - (stats['activations_per_generation'] / stats['patterns_stored'])
            print(f"   Sparsity: {sparsity:.1%}")
        
        # Comparación con modelos tradicionales
        print(f"\n🔬 COMPARACIÓN CON MODELOS TRADICIONALES:")
        print(f"   Tu UltraEfficientLLM: {stats['memory_kb']:.2f} KB")
        print(f"   GPT-3: ~14,000,000 KB (14GB)")
        print(f"   Ratio de eficiencia: 1:{stats['memory_kb']/14000000:.0f}")
    
    def run_full_demo(self):
        """Ejecutar demostración completa"""
        print("🧠 DEMOSTRACIÓN COMPLETA DEL RAZONAMIENTO ULTRAEFFICIENTLLM")
        print("=" * 80)
        
        # 1. Entrenamiento
        self.train_with_demo_data()
        
        # 2. Demostración de extracción de patrones
        self.demonstrate_pattern_extraction("machine learning is a subset of artificial intelligence")
        
        # 3. Demostración de activación de patrones
        self.demonstrate_pattern_activation("machine learning")
        
        # 4. Demostración de cadena de razonamiento
        self.demonstrate_reasoning_chain("machine learning", 5)
        
        # 5. Demostración de diferentes contextos
        self.demonstrate_different_contexts()
        
        # 6. Métricas de eficiencia
        self.demonstrate_efficiency_metrics()
        
        print(f"\n🎉 DEMOSTRACIÓN COMPLETADA")
        print("=" * 80)
        print("✅ Has visto cómo tu UltraEfficientLLM:")
        print("   🧩 Extrae patrones inteligentemente")
        print("   ⚡ Activa solo patrones relevantes")
        print("   🧠 Razonamiento paso a paso")
        print("   📊 Eficiencia extrema")
        print("   🎯 Adaptación contextual")


def interactive_reasoning_demo():
    """Demostración interactiva del razonamiento"""
    
    print("🧠 DEMOSTRACIÓN INTERACTIVA DEL RAZONAMIENTO")
    print("=" * 60)
    
    demo = ReasoningDemo()
    
    while True:
        print("\n🎯 ¿Qué quieres explorar?")
        print("1. Entrenar modelo con datos de demostración")
        print("2. Ver extracción de patrones")
        print("3. Ver activación de patrones")
        print("4. Ver cadena de razonamiento")
        print("5. Comparar diferentes contextos")
        print("6. Ver métricas de eficiencia")
        print("7. Demostración completa")
        print("8. Salir")
        
        choice = input("\nSelecciona una opción (1-8): ").strip()
        
        if choice == "8":
            print("👋 ¡Hasta luego!")
            break
        
        if choice == "1":
            demo.train_with_demo_data()
        
        elif choice == "2":
            text = input("📝 Ingresa un texto para analizar: ").strip()
            if text:
                demo.demonstrate_pattern_extraction(text)
            else:
                demo.demonstrate_pattern_extraction("machine learning is a subset of artificial intelligence")
        
        elif choice == "3":
            context = input("🎯 Ingresa un contexto: ").strip()
            if context:
                demo.demonstrate_pattern_activation(context)
            else:
                demo.demonstrate_pattern_activation("machine learning")
        
        elif choice == "4":
            prompt = input("🚀 Ingresa un prompt: ").strip()
            if prompt:
                steps = input("📊 Número de pasos (Enter para 5): ").strip()
                steps = int(steps) if steps.isdigit() else 5
                demo.demonstrate_reasoning_chain(prompt, steps)
            else:
                demo.demonstrate_reasoning_chain("machine learning", 5)
        
        elif choice == "5":
            demo.demonstrate_different_contexts()
        
        elif choice == "6":
            demo.demonstrate_efficiency_metrics()
        
        elif choice == "7":
            demo.run_full_demo()
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Demostración del Razonamiento del UltraEfficientLLM")
    parser.add_argument("--interactive", action="store_true", help="Modo interactivo")
    parser.add_argument("--full", action="store_true", help="Demostración completa")
    parser.add_argument("--context", type=str, help="Contexto para analizar")
    parser.add_argument("--prompt", type=str, help="Prompt para razonamiento")
    
    args = parser.parse_args()
    
    demo = ReasoningDemo()
    
    if args.interactive:
        interactive_reasoning_demo()
    elif args.full:
        demo.run_full_demo()
    elif args.context:
        demo.train_with_demo_data()
        demo.demonstrate_pattern_activation(args.context)
    elif args.prompt:
        demo.train_with_demo_data()
        demo.demonstrate_reasoning_chain(args.prompt, 5)
    else:
        print("🧠 DEMOSTRACIÓN DEL RAZONAMIENTO ULTRAEFFICIENTLLM")
        print("=" * 60)
        print("Uso:")
        print("  python reasoning_demo.py --interactive")
        print("  python reasoning_demo.py --full")
        print("  python reasoning_demo.py --context 'machine learning'")
        print("  python reasoning_demo.py --prompt 'artificial intelligence'") 