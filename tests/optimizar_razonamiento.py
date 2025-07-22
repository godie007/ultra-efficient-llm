#!/usr/bin/env python3
"""
🔧 OPTIMIZACIÓN DE PARÁMETROS PARA MEJORAR RAZONAMIENTO
=======================================================

Este script prueba diferentes configuraciones del modelo para optimizar el razonamiento.
"""

import sys
import os
sys.path.append('src')

from ultra_efficient_llm import UltraEfficientLLM
import time

def cargar_dataset(ruta_archivo):
    """Cargar dataset desde archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return None

def evaluar_razonamiento_simple(respuesta, palabras_clave):
    """Evaluación simple de razonamiento"""
    puntuacion = 0
    for palabra in palabras_clave:
        if palabra.lower() in respuesta.lower():
            puntuacion += 1
    return puntuacion / len(palabras_clave) * 100

def test_configuracion(model, config_name):
    """Probar una configuración específica"""
    print(f"\n🧪 Probando configuración: {config_name}")
    print("=" * 50)
    
    preguntas_test = [
        {
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "palabras_clave": ["nutrientes", "desechos", "peces", "naturales"]
        },
        {
            "pregunta": "¿Qué pasa si no hay peces en el sistema?",
            "palabras_clave": ["nutrientes", "plantas", "morir", "sistema"]
        },
        {
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "palabras_clave": ["nutrientes", "deficiencia", "problema", "causa"]
        }
    ]
    
    puntuaciones = []
    
    for test in preguntas_test:
        respuesta = model.generate(test['pregunta'], max_length=40, temperature=0.3)
        puntuacion = evaluar_razonamiento_simple(respuesta, test['palabras_clave'])
        puntuaciones.append(puntuacion)
        
        print(f"❓ {test['pregunta']}")
        print(f"🤖 {respuesta}")
        print(f"📊 Puntuación: {puntuacion:.1f}%")
    
    promedio = sum(puntuaciones) / len(puntuaciones)
    print(f"\n📈 Puntuación promedio: {promedio:.1f}%")
    
    return promedio

def main():
    """Función principal"""
    print("🔧 OPTIMIZACIÓN DE PARÁMETROS PARA RAZONAMIENTO")
    print("=" * 60)
    
    # Cargar dataset mejorado
    dataset = cargar_dataset('data/acuaponia_razonamiento.txt')
    if not dataset:
        print("❌ No se pudo cargar el dataset mejorado")
        return
    
    print(f"📚 Dataset cargado: {len(dataset)} líneas")
    
    # Configuraciones a probar
    configuraciones = [
        {
            "name": "Configuración Básica",
            "max_pattern_length": 6,
            "min_frequency": 1,
            "max_patterns": 6000
        },
        {
            "name": "Patrones Más Largos",
            "max_pattern_length": 8,
            "min_frequency": 1,
            "max_patterns": 8000
        },
        {
            "name": "Más Patrones",
            "max_pattern_length": 6,
            "min_frequency": 1,
            "max_patterns": 10000
        },
        {
            "name": "Frecuencia Mínima Mayor",
            "max_pattern_length": 6,
            "min_frequency": 2,
            "max_patterns": 6000
        },
        {
            "name": "Configuración Avanzada",
            "max_pattern_length": 8,
            "min_frequency": 1,
            "max_patterns": 12000
        }
    ]
    
    resultados = {}
    
    for config in configuraciones:
        print(f"\n🔄 Entrenando modelo con {config['name']}...")
        
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
        
        print(f"✅ Entrenamiento completado en {training_time:.2f} segundos")
        
        # Probar configuración
        puntuacion = test_configuracion(model, config['name'])
        resultados[config['name']] = {
            'puntuacion': puntuacion,
            'tiempo_entrenamiento': training_time,
            'config': config
        }
    
    # Mostrar resultados finales
    print("\n" + "="*60)
    print("📊 RESULTADOS DE OPTIMIZACIÓN")
    print("="*60)
    
    # Ordenar por puntuación
    resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1]['puntuacion'], reverse=True)
    
    for i, (nombre, datos) in enumerate(resultados_ordenados, 1):
        print(f"\n{i}. {nombre}")
        print(f"   📈 Puntuación: {datos['puntuacion']:.1f}%")
        print(f"   ⏱️  Tiempo: {datos['tiempo_entrenamiento']:.2f}s")
        print(f"   ⚙️  Config: {datos['config']}")
    
    # Mejor configuración
    mejor_config = resultados_ordenados[0]
    print(f"\n🏆 MEJOR CONFIGURACIÓN: {mejor_config[0]}")
    print(f"   Puntuación: {mejor_config[1]['puntuacion']:.1f}%")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    print(f"   1. Usar {mejor_config[0]} para mejor razonamiento")
    print(f"   2. El dataset mejorado tiene {len(dataset)} líneas vs 72 originales")
    print(f"   3. Incluye ejemplos de razonamiento causal, inferencial y comparativo")
    
    # Guardar mejor modelo
    print(f"\n💾 Guardando mejor modelo...")
    mejor_modelo = UltraEfficientLLM(
        max_pattern_length=mejor_config[1]['config']['max_pattern_length'],
        min_frequency=mejor_config[1]['config']['min_frequency'],
        max_patterns=mejor_config[1]['config']['max_patterns']
    )
    mejor_modelo.train(dataset)
    mejor_modelo.save_model("models/mejor_razonamiento.pkl")
    print(f"✅ Modelo guardado como 'mejor_razonamiento.pkl'")

if __name__ == "__main__":
    main() 