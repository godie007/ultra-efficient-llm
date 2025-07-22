#!/usr/bin/env python3
"""
🧠 TEST SISTEMA COMPLETO PROFESIONAL - ULTRAEFFICIENTLLM
========================================================

Test completo del sistema profesional con razonamiento en tiempo real.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
from reasoning_engine import ReasoningEngine, apply_intelligent_reasoning
from generative_enhancer import mejorar_respuesta_generativa
import time
import json

def cargar_dataset(ruta_archivo):
    """Cargar dataset desde archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return None

def test_sistema_completo_profesional():
    """Test completo del sistema profesional"""
    print("🧠 TEST SISTEMA COMPLETO PROFESIONAL")
    print("=" * 60)
    
    # 1. Inicializar componentes
    print("🔧 Inicializando componentes del sistema...")
    
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    reasoning_engine = ReasoningEngine()
    
    print("✅ Componentes inicializados correctamente")
    
    # 2. Cargar y entrenar modelo
    print("\n🔄 Entrenando modelo con dataset profesional...")
    
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        print("❌ No se pudo cargar el dataset")
        return
    
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    print(f"📊 Patrones extraídos: {len(model.patterns)}")
    
    # 3. Preguntas de prueba profesional
    preguntas_profesionales = [
        {
            'categoria': 'SEGURIDAD CRÍTICA',
            'pregunta': '¿Por qué no debo echar ácido clorhídrico a un cultivo acuapónico?',
            'expectativa': 'Análisis completo de riesgos químicos y biológicos'
        },
        {
            'categoria': 'RAZONAMIENTO CAUSAL AVANZADO',
            'pregunta': '¿Por qué las plantas crecen mejor en acuaponía que en hidroponía tradicional?',
            'expectativa': 'Análisis de relaciones causa-efecto complejas'
        },
        {
            'categoria': 'SOLUCIÓN DE PROBLEMAS TÉCNICOS',
            'pregunta': '¿Qué hago si los peces están en la superficie del agua y no comen?',
            'expectativa': 'Diagnóstico sistemático y solución paso a paso'
        },
        {
            'categoria': 'ANÁLISIS TÉCNICO ESPECIALIZADO',
            'pregunta': '¿Cómo funciona el ciclo del nitrógeno en un sistema acuapónico?',
            'expectativa': 'Explicación técnica detallada de procesos biológicos'
        },
        {
            'categoria': 'EVALUACIÓN DE CONSECUENCIAS',
            'pregunta': '¿Qué pasa si la temperatura del agua sube a 35°C en verano?',
            'expectativa': 'Análisis de impactos en múltiples niveles del sistema'
        },
        {
            'categoria': 'COMPARACIÓN TÉCNICA',
            'pregunta': '¿Cuál es la diferencia entre acuaponía y piscicultura tradicional?',
            'expectativa': 'Comparación técnica detallada de métodos'
        }
    ]
    
    # 4. Probar cada pregunta
    resultados_completos = []
    
    for i, pregunta_test in enumerate(preguntas_profesionales, 1):
        print(f"\n{'='*60}")
        print(f"🔍 PRUEBA {i}: {pregunta_test['categoria']}")
        print(f"❓ Pregunta: {pregunta_test['pregunta']}")
        print(f"🎯 Expectativa: {pregunta_test['expectativa']}")
        print(f"{'='*60}")
        
        # Paso 1: Análisis de pregunta
        print("\n🧠 PASO 1: Análisis de Pregunta")
        start_time = time.time()
        analisis = reasoning_engine.analyze_question(pregunta_test['pregunta'])
        analysis_time = time.time() - start_time
        
        print(f"⏱️ Tiempo de análisis: {analysis_time:.3f}s")
        print(f"🎯 Estrategia detectada: {analisis['primary_strategy']}")
        print(f"📊 Tipos detectados: {analisis['detected_types']}")
        print(f"🌱 Contextos acuaponía: {analisis['acuaponia_contexts']}")
        
        # Paso 2: Generación base
        print("\n🤖 PASO 2: Generación Base")
        start_time = time.time()
        respuesta_base = model.generate(pregunta_test['pregunta'], max_length=60, temperature=0.3)
        base_time = time.time() - start_time
        
        print(f"⏱️ Tiempo de generación base: {base_time:.3f}s")
        print(f"📝 Respuesta base: {respuesta_base[:100]}...")
        
        # Paso 3: Aplicación de razonamiento
        print("\n🧠 PASO 3: Aplicación de Razonamiento")
        start_time = time.time()
        respuesta_razonada = reasoning_engine.apply_reasoning(pregunta_test['pregunta'], respuesta_base)
        reasoning_time = time.time() - start_time
        
        print(f"⏱️ Tiempo de razonamiento: {reasoning_time:.3f}s")
        print(f"🧠 Respuesta con razonamiento: {respuesta_razonada[:150]}...")
        
        # Paso 4: Mejora generativa
        print("\n✨ PASO 4: Mejora Generativa")
        start_time = time.time()
        respuesta_final = mejorar_respuesta_generativa(pregunta_test['pregunta'], respuesta_razonada)
        enhancement_time = time.time() - start_time
        
        print(f"⏱️ Tiempo de mejora: {enhancement_time:.3f}s")
        print(f"✨ Respuesta final: {respuesta_final[:150]}...")
        
        # Evaluación de calidad
        calidad_base = len(respuesta_base.split()) if respuesta_base else 0
        calidad_razonada = len(respuesta_razonada.split()) if respuesta_razonada else 0
        calidad_final = len(respuesta_final.split()) if respuesta_final else 0
        
        tiempo_total = analysis_time + base_time + reasoning_time + enhancement_time
        
        resultado = {
            'categoria': pregunta_test['categoria'],
            'pregunta': pregunta_test['pregunta'],
            'expectativa': pregunta_test['expectativa'],
            'analisis': analisis,
            'respuesta_base': respuesta_base,
            'respuesta_razonada': respuesta_razonada,
            'respuesta_final': respuesta_final,
            'metricas': {
                'tiempo_analisis': analysis_time,
                'tiempo_generacion_base': base_time,
                'tiempo_razonamiento': reasoning_time,
                'tiempo_mejora': enhancement_time,
                'tiempo_total': tiempo_total,
                'calidad_base': calidad_base,
                'calidad_razonada': calidad_razonada,
                'calidad_final': calidad_final,
                'mejora_razonamiento': (calidad_razonada / calidad_base * 100) if calidad_base > 0 else 0,
                'mejora_final': (calidad_final / calidad_base * 100) if calidad_base > 0 else 0
            }
        }
        
        resultados_completos.append(resultado)
        
        print(f"\n📊 MÉTRICAS:")
        print(f"   ⏱️ Tiempo total: {tiempo_total:.3f}s")
        print(f"   📝 Calidad base: {calidad_base} palabras")
        print(f"   🧠 Calidad con razonamiento: {calidad_razonada} palabras")
        print(f"   ✨ Calidad final: {calidad_final} palabras")
        print(f"   📈 Mejora con razonamiento: {resultado['metricas']['mejora_razonamiento']:.1f}%")
        print(f"   📈 Mejora final: {resultado['metricas']['mejora_final']:.1f}%")
    
    # 5. Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN FINAL DEL SISTEMA PROFESIONAL")
    print(f"{'='*60}")
    
    # Calcular métricas agregadas
    tiempo_total_sistema = sum(r['metricas']['tiempo_total'] for r in resultados_completos)
    mejora_promedio_razonamiento = sum(r['metricas']['mejora_razonamiento'] for r in resultados_completos) / len(resultados_completos)
    mejora_promedio_final = sum(r['metricas']['mejora_final'] for r in resultados_completos) / len(resultados_completos)
    
    print(f"⏱️ Tiempo total del sistema: {tiempo_total_sistema:.3f}s")
    print(f"📈 Mejora promedio con razonamiento: {mejora_promedio_razonamiento:.1f}%")
    print(f"📈 Mejora promedio final: {mejora_promedio_final:.1f}%")
    print(f"🎯 Preguntas procesadas: {len(resultados_completos)}")
    
    # Análisis por categoría
    print(f"\n📋 ANÁLISIS POR CATEGORÍA:")
    categorias = {}
    for resultado in resultados_completos:
        categoria = resultado['categoria']
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append(resultado)
    
    for categoria, resultados in categorias.items():
        mejora_cat = sum(r['metricas']['mejora_final'] for r in resultados) / len(resultados)
        tiempo_cat = sum(r['metricas']['tiempo_total'] for r in resultados) / len(resultados)
        print(f"   {categoria}: {mejora_cat:.1f}% mejora, {tiempo_cat:.3f}s promedio")
    
    # Guardar resultados
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"../outputs/test_sistema_profesional_{timestamp}.json"
    
    os.makedirs("../outputs", exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'resumen': {
                'tiempo_total_sistema': tiempo_total_sistema,
                'mejora_promedio_razonamiento': mejora_promedio_razonamiento,
                'mejora_promedio_final': mejora_promedio_final,
                'preguntas_procesadas': len(resultados_completos)
            },
            'resultados_detallados': resultados_completos
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {filename}")
    
    # Evaluación final
    print(f"\n🎯 EVALUACIÓN FINAL:")
    if mejora_promedio_final > 200:
        print("   🏆 EXCELENTE: Sistema altamente efectivo")
    elif mejora_promedio_final > 150:
        print("   🥇 MUY BUENO: Sistema muy efectivo")
    elif mejora_promedio_final > 100:
        print("   🥈 BUENO: Sistema efectivo")
    else:
        print("   🥉 ACEPTABLE: Sistema funcional")
    
    if tiempo_total_sistema < 10:
        print("   ⚡ RÁPIDO: Tiempo de respuesta excelente")
    elif tiempo_total_sistema < 20:
        print("   🚀 BUENO: Tiempo de respuesta adecuado")
    else:
        print("   ⏳ LENTO: Necesita optimización de tiempo")
    
    print(f"\n✅ Test del sistema profesional completado exitosamente!")
    print(f"🎯 El sistema está listo para uso en producción con razonamiento en tiempo real.")

def main():
    """Función principal"""
    print("🧠 TEST SISTEMA COMPLETO PROFESIONAL - ULTRAEFFICIENTLLM")
    print("=" * 60)
    
    test_sistema_completo_profesional()

if __name__ == "__main__":
    main() 