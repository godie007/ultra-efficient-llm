#!/usr/bin/env python3
"""
🧠 TEST DE ANÁLISIS DE PATRONES Y CONTEXTO - ULTRAEFFICIENTLLM
==============================================================

Test que analiza patrones extraídos y contexto para optimizar el modelo.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
import time
import re
from collections import Counter, defaultdict

def cargar_dataset(ruta_archivo):
    """Cargar dataset desde archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return None

def analizar_patrones_dataset(dataset):
    """Analizar patrones en el dataset"""
    print("🔍 ANÁLISIS DE PATRONES EN DATASET")
    print("=" * 50)
    
    # Estadísticas básicas
    total_lineas = len(dataset)
    total_palabras = sum(len(linea.split()) for linea in dataset)
    promedio_palabras = total_palabras / total_lineas if total_lineas > 0 else 0
    
    print(f"📊 Estadísticas básicas:")
    print(f"   Total de líneas: {total_lineas}")
    print(f"   Total de palabras: {total_palabras}")
    print(f"   Promedio palabras por línea: {promedio_palabras:.1f}")
    
    # Análisis de palabras más frecuentes
    todas_palabras = []
    for linea in dataset:
        palabras = re.findall(r'\b\w+\b', linea.lower())
        todas_palabras.extend(palabras)
    
    contador_palabras = Counter(todas_palabras)
    palabras_mas_frecuentes = contador_palabras.most_common(20)
    
    print(f"\n📈 Palabras más frecuentes:")
    for palabra, frecuencia in palabras_mas_frecuentes:
        print(f"   '{palabra}': {frecuencia} veces")
    
    # Análisis de tipos de preguntas
    tipos_preguntas = {
        'causal': 0,
        'inferencial': 0,
        'comparativo': 0,
        'secuencial': 0,
        'definicion': 0,
        'solucion': 0
    }
    
    for linea in dataset:
        linea_lower = linea.lower()
        if any(palabra in linea_lower for palabra in ['por qué', 'causa', 'razón']):
            tipos_preguntas['causal'] += 1
        elif any(palabra in linea_lower for palabra in ['si', 'cuando', 'qué pasa']):
            tipos_preguntas['inferencial'] += 1
        elif any(palabra in linea_lower for palabra in ['diferencia', 'comparar', 'mejor que']):
            tipos_preguntas['comparativo'] += 1
        elif any(palabra in linea_lower for palabra in ['cómo funciona', 'pasos', 'proceso']):
            tipos_preguntas['secuencial'] += 1
        elif any(palabra in linea_lower for palabra in ['qué es', 'definir', 'significa']):
            tipos_preguntas['definicion'] += 1
        elif any(palabra in linea_lower for palabra in ['qué hago', 'cómo soluciono', 'problema']):
            tipos_preguntas['solucion'] += 1
    
    print(f"\n🎯 Tipos de preguntas detectadas:")
    for tipo, cantidad in tipos_preguntas.items():
        porcentaje = (cantidad / total_lineas) * 100 if total_lineas > 0 else 0
        print(f"   {tipo.capitalize()}: {cantidad} ({porcentaje:.1f}%)")
    
    return {
        'total_lineas': total_lineas,
        'total_palabras': total_palabras,
        'promedio_palabras': promedio_palabras,
        'palabras_frecuentes': palabras_mas_frecuentes,
        'tipos_preguntas': tipos_preguntas
    }

def analizar_patrones_modelo(model):
    """Analizar patrones extraídos por el modelo"""
    print("\n🧠 ANÁLISIS DE PATRONES DEL MODELO")
    print("=" * 50)
    
    # Acceder a patrones del modelo
    if hasattr(model, 'patterns') and model.patterns:
        total_patrones = len(model.patterns)
        print(f"📊 Total de patrones extraídos: {total_patrones}")
        
        # Analizar longitud de patrones
        longitudes = [len(patron.split()) for patron in model.patterns]
        promedio_longitud = sum(longitudes) / len(longitudes) if longitudes else 0
        max_longitud = max(longitudes) if longitudes else 0
        min_longitud = min(longitudes) if longitudes else 0
        
        print(f"📏 Estadísticas de longitud de patrones:")
        print(f"   Promedio: {promedio_longitud:.1f} palabras")
        print(f"   Máximo: {max_longitud} palabras")
        print(f"   Mínimo: {min_longitud} palabras")
        
        # Patrones más frecuentes
        contador_patrones = Counter(model.patterns)
        patrones_mas_frecuentes = contador_patrones.most_common(10)
        
        print(f"\n🏆 Patrones más frecuentes:")
        for patron, frecuencia in patrones_mas_frecuentes:
            print(f"   '{patron}': {frecuencia} veces")
    
    # Analizar grafo de conocimiento
    if hasattr(model, 'knowledge_graph') and model.knowledge_graph:
        total_nodos = len(model.knowledge_graph.nodes())
        total_aristas = len(model.knowledge_graph.edges())
        print(f"\n🕸️  Grafo de conocimiento:")
        print(f"   Nodos: {total_nodos}")
        print(f"   Aristas: {total_aristas}")
        print(f"   Densidad: {total_aristas / (total_nodos * (total_nodos - 1)):.3f}" if total_nodos > 1 else "   Densidad: N/A")

def test_diferentes_configuraciones():
    """Probar diferentes configuraciones del modelo"""
    print("\n⚙️  TEST DE DIFERENTES CONFIGURACIONES")
    print("=" * 50)
    
    # Cargar dataset
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    configuraciones = [
        {
            'nombre': 'Configuración Conservadora',
            'max_pattern_length': 4,
            'min_frequency': 2,
            'max_patterns': 4000
        },
        {
            'nombre': 'Configuración Balanceada',
            'max_pattern_length': 6,
            'min_frequency': 1,
            'max_patterns': 8000
        },
        {
            'nombre': 'Configuración Agresiva',
            'max_pattern_length': 8,
            'min_frequency': 1,
            'max_patterns': 12000
        },
        {
            'nombre': 'Configuración Especializada',
            'max_pattern_length': 5,
            'min_frequency': 1,
            'max_patterns': 6000
        }
    ]
    
    resultados = {}
    
    for config in configuraciones:
        print(f"\n🔧 Probando: {config['nombre']}")
        
        # Crear modelo con configuración específica
        model = UltraEfficientLLM(
            max_pattern_length=config['max_pattern_length'],
            min_frequency=config['min_frequency'],
            max_patterns=config['max_patterns']
        )
        
        # Entrenar modelo
        start_time = time.time()
        model.train(dataset)
        training_time = time.time() - start_time
        
        # Analizar patrones
        analizar_patrones_modelo(model)
        
        # Probar generación
        pregunta_test = "¿Por qué las plantas crecen bien en acuaponía?"
        respuesta = model.generate(pregunta_test, max_length=50, temperature=0.3)
        
        # Evaluar respuesta
        palabras_clave = ["nutrientes", "desechos", "peces", "naturales"]
        puntuacion = sum(1 for palabra in palabras_clave if palabra.lower() in respuesta.lower()) / len(palabras_clave) * 100
        
        print(f"🤖 Respuesta: {respuesta}")
        print(f"📊 Puntuación: {puntuacion:.1f}%")
        print(f"⏱️  Tiempo entrenamiento: {training_time:.2f}s")
        
        resultados[config['nombre']] = {
            'puntuacion': puntuacion,
            'tiempo_entrenamiento': training_time,
            'patrones': len(model.patterns) if hasattr(model, 'patterns') else 0
        }
    
    # Mostrar comparación
    print(f"\n📊 COMPARACIÓN DE CONFIGURACIONES")
    print("=" * 50)
    for nombre, resultado in resultados.items():
        print(f"{nombre}:")
        print(f"   Puntuación: {resultado['puntuacion']:.1f}%")
        print(f"   Tiempo: {resultado['tiempo_entrenamiento']:.2f}s")
        print(f"   Patrones: {resultado['patrones']}")

def analizar_contexto_respuestas():
    """Analizar el contexto de las respuestas generadas"""
    print("\n🎯 ANÁLISIS DE CONTEXTO DE RESPUESTAS")
    print("=" * 50)
    
    # Cargar dataset y crear modelo
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    model.train(dataset)
    
    # Preguntas de prueba con diferentes contextos
    preguntas_contexto = [
        {
            'contexto': 'BÁSICO',
            'pregunta': '¿Qué es la acuaponía?',
            'palabras_esperadas': ['sistema', 'peces', 'plantas', 'ciclo']
        },
        {
            'contexto': 'TÉCNICO',
            'pregunta': '¿Cómo funciona el ciclo del nitrógeno en acuaponía?',
            'palabras_esperadas': ['amonio', 'nitratos', 'bacterias', 'convierten']
        },
        {
            'contexto': 'PRÁCTICO',
            'pregunta': '¿Qué necesito para empezar un sistema de acuaponía?',
            'palabras_esperadas': ['tanque', 'filtración', 'plantas', 'agua']
        },
        {
            'contexto': 'PROBLEMÁTICO',
            'pregunta': '¿Qué hago si las plantas están amarillas?',
            'palabras_esperadas': ['nutrientes', 'pH', 'verificar', 'problema']
        },
        {
            'contexto': 'COMPARATIVO',
            'pregunta': '¿Cuál es la diferencia entre acuaponía y hidroponía?',
            'palabras_esperadas': ['nutrientes', 'naturales', 'químicos', 'diferencia']
        }
    ]
    
    resultados_contexto = {}
    
    for prueba in preguntas_contexto:
        print(f"\n🔍 Contexto: {prueba['contexto']}")
        print(f"❓ Pregunta: {prueba['pregunta']}")
        
        # Generar respuesta
        respuesta = model.generate(prueba['pregunta'], max_length=60, temperature=0.3)
        print(f"🤖 Respuesta: {respuesta}")
        
        # Evaluar cobertura de palabras esperadas
        palabras_encontradas = []
        for palabra in prueba['palabras_esperadas']:
            if palabra.lower() in respuesta.lower():
                palabras_encontradas.append(palabra)
        
        cobertura = len(palabras_encontradas) / len(prueba['palabras_esperadas']) * 100
        print(f"📊 Cobertura: {cobertura:.1f}% ({len(palabras_encontradas)}/{len(prueba['palabras_esperadas'])})")
        print(f"✅ Palabras encontradas: {', '.join(palabras_encontradas)}")
        
        resultados_contexto[prueba['contexto']] = {
            'cobertura': cobertura,
            'palabras_encontradas': palabras_encontradas,
            'respuesta': respuesta
        }
    
    # Resumen de resultados por contexto
    print(f"\n📈 RESUMEN POR CONTEXTO")
    print("=" * 50)
    for contexto, resultado in resultados_contexto.items():
        print(f"{contexto}: {resultado['cobertura']:.1f}% cobertura")

def main():
    """Función principal"""
    print("🧠 TEST DE ANÁLISIS DE PATRONES Y CONTEXTO")
    print("=" * 60)
    
    # Cargar dataset
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    # Análisis del dataset
    analisis_dataset = analizar_patrones_dataset(dataset)
    
    # Test de diferentes configuraciones
    test_diferentes_configuraciones()
    
    # Análisis de contexto
    analizar_contexto_respuestas()
    
    # Recomendaciones basadas en análisis
    print(f"\n💡 RECOMENDACIONES BASADAS EN ANÁLISIS")
    print("=" * 50)
    
    # Analizar distribución de tipos de preguntas
    tipos = analisis_dataset['tipos_preguntas']
    tipo_mas_comun = max(tipos, key=tipos.get)
    tipo_menos_comun = min(tipos, key=tipos.get)
    
    print(f"🎯 Tipo de pregunta más común: {tipo_mas_comun} ({tipos[tipo_mas_comun]} preguntas)")
    print(f"🎯 Tipo de pregunta menos común: {tipo_menos_comun} ({tipos[tipo_menos_comun]} preguntas)")
    
    # Recomendaciones específicas
    if tipos['causal'] < tipos['definicion']:
        print("💡 Recomendación: Agregar más ejemplos de razonamiento causal")
    
    if tipos['solucion'] < tipos['definicion']:
        print("💡 Recomendación: Agregar más ejemplos de solución de problemas")
    
    if analisis_dataset['promedio_palabras'] < 10:
        print("💡 Recomendación: Agregar respuestas más detalladas al dataset")
    
    print(f"\n✅ Análisis completado. Usar estos insights para optimizar el modelo.")

if __name__ == "__main__":
    main() 