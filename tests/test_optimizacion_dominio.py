#!/usr/bin/env python3
"""
🎯 TEST DE OPTIMIZACIÓN ESPECÍFICA POR DOMINIO - ULTRAEFFICIENTLLM
==================================================================

Test que optimiza el modelo específicamente para el dominio de acuaponía.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
import time
import re
import json

def cargar_dataset(ruta_archivo):
    """Cargar dataset desde archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return None

def crear_dataset_especializado():
    """Crear un dataset especializado para acuaponía"""
    dataset_especializado = [
        # CONCEPTOS FUNDAMENTALES
        "¿Qué es la acuaponía? La acuaponía es un sistema que combina peces y plantas en un ciclo cerrado.",
        "¿Cómo funciona la acuaponía? Los peces producen desechos, las bacterias convierten desechos en nutrientes, las plantas absorben nutrientes y limpian el agua.",
        "¿Cuáles son los componentes básicos? Tanque para peces, sistema de filtración, camas para plantas, bomba de agua y aireador.",
        
        # RAZONAMIENTO CAUSAL ESPECÍFICO
        "¿Por qué las plantas crecen bien en acuaponía? Porque reciben nutrientes naturales de los desechos de los peces.",
        "¿Por qué la acuaponía usa menos agua? Porque el agua se recicla continuamente en el sistema cerrado.",
        "¿Por qué necesitamos bacterias en acuaponía? Porque convierten amonio tóxico en nitratos que las plantas pueden absorber.",
        "¿Por qué los peces necesitan oxígeno? Porque respiran oxígeno disuelto en el agua para sobrevivir.",
        
        # DIAGNÓSTICO Y SOLUCIÓN DE PROBLEMAS
        "¿Qué pasa si las plantas están amarillas? Puede ser falta de nutrientes, pH incorrecto o demasiados peces.",
        "¿Qué pasa si los peces están en la superficie? Puede ser falta de oxígeno, necesitas un aireador.",
        "¿Qué pasa si el agua está turbia? Puede ser exceso de alimento, necesitas mejorar la filtración.",
        "¿Qué pasa si el pH está muy alto? Las plantas no pueden absorber nutrientes, necesitas bajarlo.",
        
        # COMPARACIONES ESPECÍFICAS
        "¿Cuál es la diferencia entre acuaponía y hidroponía? La acuaponía usa nutrientes naturales de peces, la hidroponía usa fertilizantes químicos.",
        "¿Cuál es la diferencia entre acuaponía y piscicultura? La acuaponía produce peces y plantas, la piscicultura solo peces.",
        "¿Cuál es la diferencia entre acuaponía y agricultura tradicional? La acuaponía usa 90% menos agua y no necesita tierra.",
        
        # PROCESOS Y SECUENCIAS
        "¿Cuáles son los pasos para empezar acuaponía? 1) Instalar sistema, 2) Ciclar agua, 3) Añadir bacterias, 4) Añadir peces, 5) Plantar.",
        "¿Cómo funciona el ciclo del nitrógeno? Los peces producen amonio, las bacterias convierten amonio en nitritos, luego en nitratos, las plantas absorben nitratos.",
        "¿Cómo funciona el ciclo del agua? El agua va del tanque de peces a la filtración, luego a las plantas, y regresa limpia a los peces.",
        
        # ESPECIFICACIONES TÉCNICAS
        "¿Qué pH necesito en acuaponía? Entre 6.0 y 7.0 para que las plantas absorban nutrientes y los peces estén cómodos.",
        "¿Qué temperatura necesito? Entre 20-30°C para la mayoría de peces y plantas de acuaponía.",
        "¿Cuánto oxígeno necesito? Al menos 5 mg/L para que los peces respiren bien.",
        "¿Qué tipos de peces puedo usar? Tilapia, trucha, carpa, bagre y otros peces de agua dulce.",
        
        # MANTENIMIENTO Y CUIDADO
        "¿Cómo alimento a los peces? Alimenta 2-3 veces al día, solo lo que coman en 5 minutos.",
        "¿Cuándo cosecho las plantas? Cuando estén maduras, cosecha hojas exteriores para que sigan creciendo.",
        "¿Cómo limpio el sistema? Limpia filtros semanalmente, cambia 10% del agua mensualmente.",
        "¿Cómo monitoreo el sistema? Revisa pH, amonio, nitritos, nitratos, oxígeno y temperatura regularmente.",
        
        # PROBLEMAS ESPECÍFICOS Y SOLUCIONES
        "¿Qué hago si las plantas no crecen? Verifica nutrientes, pH, iluminación y temperatura.",
        "¿Qué hago si los peces no comen? Revisa calidad del agua, temperatura y tipo de alimento.",
        "¿Qué hago si hay algas? Reduce luz, mejora filtración y añade más plantas.",
        "¿Qué hago si el agua huele mal? Cambia agua, limpia filtros y reduce alimentación.",
        
        # RENTABILIDAD Y ESCALABILIDAD
        "¿Es rentable la acuaponía? Sí, especialmente a mediana y gran escala con mercados locales.",
        "¿Qué plantas son más rentables? Lechugas, hierbas, tomates, pepinos y pimientos.",
        "¿Cuánto tiempo tarda en madurar? El sistema tarda 4-6 semanas en madurar completamente.",
        "¿Qué inversión inicial necesito? Depende del tamaño, desde $500 para sistemas pequeños hasta $50,000 para comerciales."
    ]
    
    return dataset_especializado

def evaluar_respuesta_especifica(respuesta, palabras_clave, contexto):
    """Evaluar respuesta específica para el dominio de acuaponía"""
    puntuacion = 0
    
    # Verificar palabras clave específicas
    palabras_encontradas = 0
    for palabra in palabras_clave:
        if palabra.lower() in respuesta.lower():
            palabras_encontradas += 1
    
    puntuacion += (palabras_encontradas / len(palabras_clave)) * 40
    
    # Verificar coherencia con el contexto
    if contexto in respuesta.lower():
        puntuacion += 30
    
    # Verificar longitud adecuada
    palabras = respuesta.split()
    if 8 <= len(palabras) <= 25:
        puntuacion += 20
    else:
        puntuacion -= 10
    
    # Verificar estructura gramatical
    if respuesta.strip()[0].isupper() and respuesta.strip().endswith('.'):
        puntuacion += 10
    else:
        puntuacion -= 5
    
    return max(0, min(100, puntuacion))

def test_optimizacion_por_dominio():
    """Test de optimización específica para acuaponía"""
    print("🎯 TEST DE OPTIMIZACIÓN ESPECÍFICA POR DOMINIO")
    print("=" * 60)
    
    # Crear dataset especializado
    dataset_especializado = crear_dataset_especializado()
    print(f"📚 Dataset especializado creado: {len(dataset_especializado)} líneas")
    
    # Configuraciones optimizadas para acuaponía
    configuraciones_acuaponia = [
        {
            'nombre': 'Configuración Básica Acuaponía',
            'max_pattern_length': 5,
            'min_frequency': 1,
            'max_patterns': 5000,
            'temperature': 0.2
        },
        {
            'nombre': 'Configuración Técnica Acuaponía',
            'max_pattern_length': 6,
            'min_frequency': 1,
            'max_patterns': 7000,
            'temperature': 0.3
        },
        {
            'nombre': 'Configuración Avanzada Acuaponía',
            'max_pattern_length': 7,
            'min_frequency': 1,
            'max_patterns': 9000,
            'temperature': 0.4
        },
        {
            'nombre': 'Configuración Especializada Acuaponía',
            'max_pattern_length': 6,
            'min_frequency': 1,
            'max_patterns': 8000,
            'temperature': 0.25
        }
    ]
    
    # Preguntas de prueba específicas para acuaponía
    preguntas_prueba = [
        {
            'categoria': 'CONCEPTOS BÁSICOS',
            'pregunta': '¿Qué es la acuaponía?',
            'palabras_clave': ['sistema', 'peces', 'plantas', 'ciclo'],
            'contexto': 'acuaponía'
        },
        {
            'categoria': 'RAZONAMIENTO CAUSAL',
            'pregunta': '¿Por qué las plantas crecen bien en acuaponía?',
            'palabras_clave': ['nutrientes', 'desechos', 'peces', 'naturales'],
            'contexto': 'plantas'
        },
        {
            'categoria': 'DIAGNÓSTICO',
            'pregunta': '¿Qué pasa si las plantas están amarillas?',
            'palabras_clave': ['nutrientes', 'pH', 'peces', 'problema'],
            'contexto': 'plantas'
        },
        {
            'categoria': 'COMPARACIÓN',
            'pregunta': '¿Cuál es la diferencia entre acuaponía y hidroponía?',
            'palabras_clave': ['nutrientes', 'naturales', 'químicos', 'diferencia'],
            'contexto': 'acuaponía'
        },
        {
            'categoria': 'PROCESO',
            'pregunta': '¿Cómo funciona el ciclo del nitrógeno?',
            'palabras_clave': ['amonio', 'nitratos', 'bacterias', 'convierten'],
            'contexto': 'ciclo'
        },
        {
            'categoria': 'MANTENIMIENTO',
            'pregunta': '¿Cómo alimento a los peces?',
            'palabras_clave': ['alimenta', 'veces', 'día', 'minutos'],
            'contexto': 'peces'
        }
    ]
    
    resultados_configuraciones = {}
    
    for config in configuraciones_acuaponia:
        print(f"\n🔧 Probando: {config['nombre']}")
        
        # Crear modelo con configuración específica
        model = UltraEfficientLLM(
            max_pattern_length=config['max_pattern_length'],
            min_frequency=config['min_frequency'],
            max_patterns=config['max_patterns']
        )
        
        # Entrenar modelo
        start_time = time.time()
        model.train(dataset_especializado)
        training_time = time.time() - start_time
        
        print(f"⏱️  Tiempo entrenamiento: {training_time:.2f}s")
        
        # Probar con preguntas específicas
        puntuaciones_categoria = {}
        total_puntuacion = 0
        
        for pregunta_test in preguntas_prueba:
            print(f"\n  🎯 {pregunta_test['categoria']}")
            print(f"  ❓ {pregunta_test['pregunta']}")
            
            # Generar respuesta
            respuesta = model.generate(
                pregunta_test['pregunta'], 
                max_length=60, 
                temperature=config['temperature']
            )
            
            # Evaluar respuesta
            puntuacion = evaluar_respuesta_especifica(
                respuesta, 
                pregunta_test['palabras_clave'], 
                pregunta_test['contexto']
            )
            
            print(f"  🤖 {respuesta}")
            print(f"  📊 Puntuación: {puntuacion:.1f}%")
            
            puntuaciones_categoria[pregunta_test['categoria']] = puntuacion
            total_puntuacion += puntuacion
        
        promedio_puntuacion = total_puntuacion / len(preguntas_prueba)
        
        resultados_configuraciones[config['nombre']] = {
            'promedio': promedio_puntuacion,
            'tiempo_entrenamiento': training_time,
            'puntuaciones_categoria': puntuaciones_categoria
        }
        
        print(f"  📈 Promedio general: {promedio_puntuacion:.1f}%")
    
    # Mostrar comparación final
    print(f"\n📊 COMPARACIÓN FINAL DE CONFIGURACIONES")
    print("=" * 60)
    
    mejor_config = None
    mejor_puntuacion = 0
    
    for nombre, resultado in resultados_configuraciones.items():
        print(f"\n{nombre}:")
        print(f"  📊 Promedio general: {resultado['promedio']:.1f}%")
        print(f"  ⏱️  Tiempo entrenamiento: {resultado['tiempo_entrenamiento']:.2f}s")
        
        if resultado['promedio'] > mejor_puntuacion:
            mejor_puntuacion = resultado['promedio']
            mejor_config = nombre
        
        print(f"  📈 Puntuaciones por categoría:")
        for categoria, puntuacion in resultado['puntuaciones_categoria'].items():
            print(f"    {categoria}: {puntuacion:.1f}%")
    
    print(f"\n🏆 MEJOR CONFIGURACIÓN: {mejor_config}")
    print(f"📊 Puntuación: {mejor_puntuacion:.1f}%")
    
    return mejor_config, resultados_configuraciones

def test_especializacion_avanzada():
    """Test de especialización avanzada para casos específicos"""
    print(f"\n🎯 TEST DE ESPECIALIZACIÓN AVANZADA")
    print("=" * 60)
    
    # Crear modelo con la mejor configuración
    dataset_especializado = crear_dataset_especializado()
    
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    model.train(dataset_especializado)
    
    # Casos específicos de acuaponía
    casos_especificos = [
        {
            'caso': 'PROBLEMA DE pH',
            'pregunta': 'Mi pH está en 8.5, ¿qué hago?',
            'respuesta_esperada': 'El pH está muy alto, necesitas bajarlo a 6.0-7.0 para que las plantas absorban nutrientes.'
        },
        {
            'caso': 'PROBLEMA DE OXÍGENO',
            'pregunta': 'Los peces están en la superficie, ¿qué significa?',
            'respuesta_esperada': 'Los peces están en la superficie porque hay falta de oxígeno, necesitas un aireador.'
        },
        {
            'caso': 'PROBLEMA DE NUTRIENTES',
            'pregunta': 'Las plantas están débiles y amarillas, ¿cuál es la causa?',
            'respuesta_esperada': 'Las plantas están débiles por falta de nutrientes, pH incorrecto o demasiados peces.'
        },
        {
            'caso': 'MANTENIMIENTO',
            'pregunta': '¿Con qué frecuencia debo limpiar los filtros?',
            'respuesta_esperada': 'Debes limpiar los filtros semanalmente para mantener el sistema funcionando bien.'
        },
        {
            'caso': 'ALIMENTACIÓN',
            'pregunta': '¿Cuánto alimento debo dar a los peces?',
            'respuesta_esperada': 'Alimenta 2-3 veces al día, solo lo que coman en 5 minutos.'
        }
    ]
    
    resultados_casos = {}
    
    for caso in casos_especificos:
        print(f"\n🔍 Caso: {caso['caso']}")
        print(f"❓ Pregunta: {caso['pregunta']}")
        
        # Generar respuesta
        respuesta = model.generate(caso['pregunta'], max_length=60, temperature=0.3)
        print(f"🤖 Respuesta: {respuesta}")
        print(f"🎯 Esperado: {caso['respuesta_esperada']}")
        
        # Evaluar similitud
        palabras_respuesta = set(respuesta.lower().split())
        palabras_esperada = set(caso['respuesta_esperada'].lower().split())
        similitud = len(palabras_respuesta.intersection(palabras_esperada)) / len(palabras_esperada) * 100
        
        print(f"📊 Similitud: {similitud:.1f}%")
        
        resultados_casos[caso['caso']] = {
            'respuesta': respuesta,
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
    print("🎯 TEST DE OPTIMIZACIÓN ESPECÍFICA POR DOMINIO")
    print("=" * 60)
    
    # Test de optimización por dominio
    mejor_config, resultados = test_optimizacion_por_dominio()
    
    # Test de especialización avanzada
    resultados_casos = test_especializacion_avanzada()
    
    # Guardar modelo optimizado
    print(f"\n💾 Guardando modelo optimizado...")
    
    dataset_especializado = crear_dataset_especializado()
    model_optimizado = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    model_optimizado.train(dataset_especializado)
    model_optimizado.save_model("../models/acuaponia_optimizado_dominio.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_optimizado_dominio.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES")
    print("=" * 60)
    print(f"🏆 Mejor configuración: {mejor_config}")
    print(f"📊 Puntuación promedio: {resultados[mejor_config]['promedio']:.1f}%")
    print(f"⏱️  Tiempo de entrenamiento: {resultados[mejor_config]['tiempo_entrenamiento']:.2f}s")
    
    # Análisis de fortalezas y debilidades
    puntuaciones = resultados[mejor_config]['puntuaciones_categoria']
    mejor_categoria = max(puntuaciones, key=puntuaciones.get)
    peor_categoria = min(puntuaciones, key=puntuaciones.get)
    
    print(f"\n📈 Análisis de categorías:")
    print(f"✅ Mejor categoría: {mejor_categoria} ({puntuaciones[mejor_categoria]:.1f}%)")
    print(f"⚠️  Categoría a mejorar: {peor_categoria} ({puntuaciones[peor_categoria]:.1f}%)")
    
    print(f"\n✅ Optimización completada. El modelo está especializado para acuaponía.")

if __name__ == "__main__":
    main() 