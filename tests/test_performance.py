#!/usr/bin/env python3
"""
Test de rendimiento del modelo UltraEfficientLLM
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ultra_efficient_llm import UltraEfficientLLM

def cargar_dataset(ruta_archivo):
    """Carga el dataset desde un archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return []

def test_rendimiento():
    """Test de rendimiento del modelo"""
    print("🚀 TEST DE RENDIMIENTO - ULTRAEFFICIENTLLM")
    print("=" * 50)
    
    # Cargar dataset
    dataset = cargar_dataset('data/acuaponia_minimal.txt')
    if not dataset:
        print("❌ No se pudo cargar el dataset")
        return
    
    print(f"📚 Dataset cargado: {len(dataset)} líneas")
    
    # Crear modelo
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=6000
    )
    
    # Medir tiempo de entrenamiento
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Entrenamiento completado en {training_time:.2f} segundos")
    print(f"📊 Patrones generados: {len(model.patterns)}")
    
    # Obtener reporte de eficiencia
    efficiency_report = model.get_efficiency_report()
    print(f"💾 Memoria utilizada: {efficiency_report['memory_kb']:.2f} KB")
    print(f"🎯 Activaciones por generación: {efficiency_report.get('activations_per_generation', 0)}")
    
    # Test de velocidad de generación
    print("\n⚡ TEST DE VELOCIDAD DE GENERACIÓN:")
    print("-" * 30)
    
    test_prompts = [
        "¿Qué es la acuaponía?",
        "¿Qué peces puedo usar?",
        "¿Qué plantas crecen?",
        "¿Cuánta agua usa?",
        "¿Es orgánica?"
    ]
    
    total_generation_time = 0
    total_tokens = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Prompt: {prompt}")
        
        start_time = time.time()
        response = model.generate(prompt, max_length=20, temperature=0.3)
        generation_time = time.time() - start_time
        
        tokens = len(response.split())
        tokens_per_second = tokens / generation_time if generation_time > 0 else 0
        
        total_generation_time += generation_time
        total_tokens += tokens
        
        print(f"   Tiempo: {generation_time:.3f}s")
        print(f"   Tokens: {tokens}")
        print(f"   Velocidad: {tokens_per_second:.1f} tokens/s")
        print(f"   Respuesta: {response[:50]}...")
    
    # Estadísticas finales
    avg_generation_time = total_generation_time / len(test_prompts)
    avg_tokens_per_second = total_tokens / total_generation_time if total_generation_time > 0 else 0
    
    print(f"\n📊 ESTADÍSTICAS DE RENDIMIENTO:")
    print(f"   Tiempo promedio de generación: {avg_generation_time:.3f}s")
    print(f"   Velocidad promedio: {avg_tokens_per_second:.1f} tokens/s")
    print(f"   Total de tokens generados: {total_tokens}")
    print(f"   Tiempo total de generación: {total_generation_time:.3f}s")
    
    # Evaluar rendimiento
    if avg_tokens_per_second >= 50:
        print("🎉 ¡EXCELENTE RENDIMIENTO! Muy rápido")
    elif avg_tokens_per_second >= 30:
        print("👍 BUEN RENDIMIENTO: Aceptable")
    elif avg_tokens_per_second >= 15:
        print("⚠️  RENDIMIENTO MODERADO: Podría mejorar")
    else:
        print("❌ RENDIMIENTO BAJO: Necesita optimización")

def test_memoria():
    """Test de uso de memoria"""
    print("\n💾 TEST DE MEMORIA:")
    print("-" * 30)
    
    dataset = cargar_dataset('data/acuaponia_minimal.txt')
    if not dataset:
        return
    
    model = UltraEfficientLLM(max_pattern_length=6, min_frequency=1, max_patterns=6000)
    model.train(dataset)
    
    efficiency_report = model.get_efficiency_report()
    
    print(f"📊 Memoria utilizada: {efficiency_report['memory_kb']:.2f} KB")
    print(f"📊 Patrones almacenados: {efficiency_report.get('patterns_stored', 0)}")
    print(f"📊 Generaciones totales: {efficiency_report.get('total_generations', 0)}")
    print(f"📊 Cache hits: {efficiency_report.get('cache_hits', 0)}")
    
    # Evaluar eficiencia de memoria
    memory_mb = efficiency_report['memory_kb'] / 1024
    if memory_mb < 1:
        print("🎉 ¡MEMORIA ULTRA-EFICIENTE! < 1MB")
    elif memory_mb < 5:
        print("👍 MEMORIA EFICIENTE: < 5MB")
    elif memory_mb < 10:
        print("⚠️  MEMORIA MODERADA: < 10MB")
    else:
        print("❌ MEMORIA ALTA: > 10MB")

if __name__ == "__main__":
    test_rendimiento()
    test_memoria() 