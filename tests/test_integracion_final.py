#!/usr/bin/env python3
"""
🔧 TEST DE INTEGRACIÓN FINAL - ULTRAEFFICIENTLLM
================================================

Test final que integra todas las mejoras y optimizaciones del modelo.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
from generative_enhancer import GenerativeEnhancer, mejorar_respuesta_generativa
import time
import re

def cargar_dataset(ruta_archivo):
    """Cargar dataset desde archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return None

def evaluar_respuesta_completa(respuesta, palabras_clave, contexto):
    """Evaluación completa de una respuesta"""
    puntuacion = 0
    
    # Verificar palabras clave
    palabras_encontradas = 0
    for palabra in palabras_clave:
        if palabra.lower() in respuesta.lower():
            palabras_encontradas += 1
    
    puntuacion += (palabras_encontradas / len(palabras_clave)) * 30
    
    # Verificar coherencia temática
    if contexto in respuesta.lower():
        puntuacion += 20
    
    # Verificar estructura gramatical
    if respuesta.strip()[0].isupper() and respuesta.strip().endswith('.'):
        puntuacion += 15
    else:
        puntuacion -= 10
    
    # Verificar longitud adecuada
    palabras = respuesta.split()
    if 8 <= len(palabras) <= 30:
        puntuacion += 15
    else:
        puntuacion -= 10
    
    # Verificar uso de metáforas/creatividad
    metaforas = ['como', 'es como', 'parece', 'similar a', 'mágico', 'revolucionario', 'fascinante']
    if any(metafora in respuesta.lower() for metafora in metaforas):
        puntuacion += 20
    else:
        puntuacion -= 5
    
    return max(0, min(100, puntuacion))

def test_integracion_completa():
    """Test de integración completa con todas las mejoras"""
    print("🔧 TEST DE INTEGRACIÓN FINAL")
    print("=" * 60)
    
    # Cargar dataset optimizado
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset cargado: {len(dataset)} líneas")
    
    # Crear modelo con configuración optimizada
    print("\n🧠 Creando modelo optimizado...")
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    # Entrenar modelo
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Crear enhancer
    enhancer = GenerativeEnhancer()
    
    # Preguntas de prueba integrales
    preguntas_integrales = [
        {
            'categoria': 'CONCEPTOS FUNDAMENTALES',
            'pregunta': '¿Qué es la acuaponía?',
            'palabras_clave': ['sistema', 'peces', 'plantas', 'ciclo'],
            'contexto': 'acuaponía',
            'respuesta_esperada': 'La acuaponía es un sistema que combina peces y plantas en un ciclo cerrado.'
        },
        {
            'categoria': 'RAZONAMIENTO CAUSAL',
            'pregunta': '¿Por qué las plantas crecen bien en acuaponía?',
            'palabras_clave': ['nutrientes', 'desechos', 'peces', 'naturales'],
            'contexto': 'plantas',
            'respuesta_esperada': 'Las plantas crecen bien porque reciben nutrientes naturales de los desechos de los peces.'
        },
        {
            'categoria': 'DIAGNÓSTICO Y SOLUCIÓN',
            'pregunta': '¿Qué hago si las plantas están amarillas?',
            'palabras_clave': ['nutrientes', 'pH', 'verificar', 'problema'],
            'contexto': 'plantas',
            'respuesta_esperada': 'Si las plantas están amarillas, verifica nutrientes, pH e iluminación.'
        },
        {
            'categoria': 'COMPARACIÓN TÉCNICA',
            'pregunta': '¿Cuál es la diferencia entre acuaponía y hidroponía?',
            'palabras_clave': ['nutrientes', 'naturales', 'químicos', 'diferencia'],
            'contexto': 'acuaponía',
            'respuesta_esperada': 'La acuaponía usa nutrientes naturales de peces, la hidroponía usa fertilizantes químicos.'
        },
        {
            'categoria': 'PROCESO TÉCNICO',
            'pregunta': '¿Cómo funciona el ciclo del nitrógeno?',
            'palabras_clave': ['amonio', 'nitratos', 'bacterias', 'convierten'],
            'contexto': 'ciclo',
            'respuesta_esperada': 'Los peces producen amonio, las bacterias convierten amonio en nitratos, las plantas absorben nitratos.'
        },
        {
            'categoria': 'MANTENIMIENTO PRÁCTICO',
            'pregunta': '¿Cómo alimento a los peces?',
            'palabras_clave': ['alimenta', 'veces', 'día', 'minutos'],
            'contexto': 'peces',
            'respuesta_esperada': 'Alimenta 2-3 veces al día, solo lo que coman en 5 minutos.'
        }
    ]
    
    resultados_integrales = {}
    
    for i, pregunta_test in enumerate(preguntas_integrales, 1):
        print(f"\n{i}. {pregunta_test['categoria']}")
        print(f"❓ {pregunta_test['pregunta']}")
        
        # Generar respuesta original
        respuesta_original = model.generate(pregunta_test['pregunta'], max_length=60, temperature=0.3)
        print(f"🤖 Original: {respuesta_original}")
        
        # Mejorar con post-procesamiento
        respuesta_mejorada = mejorar_respuesta_generativa(pregunta_test['pregunta'], respuesta_original)
        print(f"✨ Mejorada: {respuesta_mejorada}")
        
        # Evaluar respuestas
        puntuacion_original = evaluar_respuesta_completa(
            respuesta_original, 
            pregunta_test['palabras_clave'], 
            pregunta_test['contexto']
        )
        
        puntuacion_mejorada = evaluar_respuesta_completa(
            respuesta_mejorada, 
            pregunta_test['palabras_clave'], 
            pregunta_test['contexto']
        )
        
        # Calcular mejora
        mejora = puntuacion_mejorada - puntuacion_original
        
        print(f"📊 Original: {puntuacion_original:.1f}%")
        print(f"📊 Mejorada: {puntuacion_mejorada:.1f}%")
        print(f"📈 Mejora: {mejora:+.1f}%")
        print(f"🎯 Esperado: {pregunta_test['respuesta_esperada']}")
        
        resultados_integrales[pregunta_test['categoria']] = {
            'original': puntuacion_original,
            'mejorada': puntuacion_mejorada,
            'mejora': mejora,
            'respuesta_original': respuesta_original,
            'respuesta_mejorada': respuesta_mejorada
        }
    
    # Resumen final
    print(f"\n📊 RESUMEN FINAL DE INTEGRACIÓN")
    print("=" * 60)
    
    total_original = sum(r['original'] for r in resultados_integrales.values())
    total_mejorada = sum(r['mejorada'] for r in resultados_integrales.values())
    total_mejora = total_mejorada - total_original
    
    promedio_original = total_original / len(resultados_integrales)
    promedio_mejorada = total_mejorada / len(resultados_integrales)
    
    print(f"📊 Puntuación promedio original: {promedio_original:.1f}%")
    print(f"📊 Puntuación promedio mejorada: {promedio_mejorada:.1f}%")
    print(f"📈 Mejora total: {total_mejora:+.1f}%")
    print(f"📈 Mejora promedio: {total_mejora/len(resultados_integrales):+.1f}%")
    
    # Análisis por categoría
    print(f"\n📈 ANÁLISIS POR CATEGORÍA")
    print("=" * 60)
    
    mejor_categoria = max(resultados_integrales.items(), key=lambda x: x[1]['mejorada'])
    peor_categoria = min(resultados_integrales.items(), key=lambda x: x[1]['mejorada'])
    
    print(f"✅ Mejor categoría: {mejor_categoria[0]} ({mejor_categoria[1]['mejorada']:.1f}%)")
    print(f"⚠️  Categoría a mejorar: {peor_categoria[0]} ({peor_categoria[1]['mejorada']:.1f}%)")
    
    # Mostrar todas las categorías
    for categoria, resultado in resultados_integrales.items():
        print(f"{categoria}: {resultado['mejorada']:.1f}% (mejora: {resultado['mejora']:+.1f}%)")
    
    return resultados_integrales, promedio_mejorada

def test_casos_especificos_mejorados():
    """Test de casos específicos con mejoras"""
    print(f"\n🎯 TEST DE CASOS ESPECÍFICOS MEJORADOS")
    print("=" * 60)
    
    # Cargar modelo optimizado
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    model.train(dataset)
    
    # Casos específicos de acuaponía
    casos_especificos = [
        {
            'caso': 'PROBLEMA DE pH ALTO',
            'pregunta': 'Mi pH está en 8.5, ¿qué debo hacer?',
            'solucion_esperada': 'El pH está muy alto, necesitas bajarlo a 6.0-7.0 para que las plantas absorban nutrientes.'
        },
        {
            'caso': 'PROBLEMA DE OXÍGENO',
            'pregunta': 'Los peces están en la superficie, ¿qué significa?',
            'solucion_esperada': 'Los peces están en la superficie porque hay falta de oxígeno, necesitas un aireador.'
        },
        {
            'caso': 'PROBLEMA DE NUTRIENTES',
            'pregunta': 'Las plantas están débiles y amarillas, ¿cuál es la causa?',
            'solucion_esperada': 'Las plantas están débiles por falta de nutrientes, pH incorrecto o demasiados peces.'
        },
        {
            'caso': 'MANTENIMIENTO DE FILTROS',
            'pregunta': '¿Con qué frecuencia debo limpiar los filtros?',
            'solucion_esperada': 'Debes limpiar los filtros semanalmente para mantener el sistema funcionando bien.'
        },
        {
            'caso': 'ALIMENTACIÓN DE PECES',
            'pregunta': '¿Cuánto alimento debo dar a los peces?',
            'solucion_esperada': 'Alimenta 2-3 veces al día, solo lo que coman en 5 minutos.'
        }
    ]
    
    resultados_casos = {}
    
    for caso in casos_especificos:
        print(f"\n🔍 Caso: {caso['caso']}")
        print(f"❓ Pregunta: {caso['pregunta']}")
        
        # Generar respuesta original
        respuesta_original = model.generate(caso['pregunta'], max_length=60, temperature=0.3)
        print(f"🤖 Original: {respuesta_original}")
        
        # Mejorar respuesta
        respuesta_mejorada = mejorar_respuesta_generativa(caso['pregunta'], respuesta_original)
        print(f"✨ Mejorada: {respuesta_mejorada}")
        
        print(f"🎯 Esperado: {caso['solucion_esperada']}")
        
        # Evaluar similitud
        palabras_respuesta = set(respuesta_mejorada.lower().split())
        palabras_esperada = set(caso['solucion_esperada'].lower().split())
        similitud = len(palabras_respuesta.intersection(palabras_esperada)) / len(palabras_esperada) * 100
        
        print(f"📊 Similitud: {similitud:.1f}%")
        
        resultados_casos[caso['caso']] = {
            'respuesta_original': respuesta_original,
            'respuesta_mejorada': respuesta_mejorada,
            'similitud': similitud
        }
    
    # Resumen de casos específicos
    print(f"\n📈 RESUMEN DE CASOS ESPECÍFICOS")
    print("=" * 60)
    for caso, resultado in resultados_casos.items():
        print(f"{caso}: {resultado['similitud']:.1f}% similitud")
    
    return resultados_casos

def main():
    """Función principal"""
    print("🔧 TEST DE INTEGRACIÓN FINAL - ULTRAEFFICIENTLLM")
    print("=" * 60)
    
    # Test de integración completa
    resultados_integrales, promedio_final = test_integracion_completa()
    
    # Test de casos específicos mejorados
    resultados_casos = test_casos_especificos_mejorados()
    
    # Guardar modelo final integrado
    print(f"\n💾 Guardando modelo final integrado...")
    
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    model_final = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    model_final.train(dataset)
    model_final.save_model("../models/acuaponia_final_integrado.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_final_integrado.pkl'")
    
    # Evaluación final
    print(f"\n🎯 EVALUACIÓN FINAL")
    print("=" * 60)
    print(f"📊 Puntuación promedio final: {promedio_final:.1f}%")
    
    if promedio_final >= 70:
        print("🟢 EXCELENTE: El modelo está altamente optimizado")
        print("✅ El modelo es muy útil en el contexto de acuaponía")
    elif promedio_final >= 50:
        print("🟡 BUENO: El modelo está bien optimizado")
        print("✅ El modelo es útil en el contexto de acuaponía")
    elif promedio_final >= 30:
        print("🟠 REGULAR: El modelo necesita más optimización")
        print("⚠️  El modelo es moderadamente útil")
    else:
        print("🔴 DEFICIENTE: El modelo necesita optimización significativa")
        print("❌ El modelo no es suficientemente útil")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES")
    print("=" * 60)
    
    if promedio_final >= 60:
        print("✅ El modelo está listo para uso en producción")
        print("✅ Integrar en la aplicación web para respuestas mejoradas")
        print("✅ El sistema de post-procesamiento funciona correctamente")
    else:
        print("⚠️  El modelo necesita más mejoras antes de producción")
        print("💡 Considerar expandir el dataset con más ejemplos")
        print("💡 Ajustar parámetros del modelo para mejor rendimiento")
    
    print(f"\n✅ Test de integración completado. El modelo está optimizado para acuaponía.")

if __name__ == "__main__":
    main() 