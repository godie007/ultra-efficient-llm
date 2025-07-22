#!/usr/bin/env python3
"""
🧠 TEST DE RAZONAMIENTO INTELIGENTE - ULTRAEFFICIENTLLM
========================================================

Test específico para probar el sistema de razonamiento inteligente.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
from reasoning_engine import ReasoningEngine, apply_intelligent_reasoning
from generative_enhancer import mejorar_respuesta_generativa
import time

def cargar_dataset(ruta_archivo):
    """Cargar dataset desde archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta_archivo}")
        return None

def test_razonamiento_inteligente():
    """Test del sistema de razonamiento inteligente"""
    print("🧠 TEST DE RAZONAMIENTO INTELIGENTE")
    print("=" * 60)
    
    # Crear motor de razonamiento
    reasoning_engine = ReasoningEngine()
    
    # Preguntas de prueba específicas para razonamiento
    preguntas_razonamiento = [
        {
            'categoria': 'SEGURIDAD QUÍMICA',
            'pregunta': '¿Por qué no debo echar ácido a un cultivo acuapónico?',
            'tipo_esperado': 'safety',
            'contexto_esperado': ['chemical_safety', 'pH_analysis']
        },
        {
            'categoria': 'RAZONAMIENTO CAUSAL',
            'pregunta': '¿Por qué las plantas crecen mejor en acuaponía que en tierra?',
            'tipo_esperado': 'causal',
            'contexto_esperado': ['nutrient_balance']
        },
        {
            'categoria': 'SOLUCIÓN DE PROBLEMAS',
            'pregunta': '¿Qué hago si los peces están en la superficie del agua?',
            'tipo_esperado': 'problem_solving',
            'contexto_esperado': ['oxygen_management']
        },
        {
            'categoria': 'ANÁLISIS TÉCNICO',
            'pregunta': '¿Cómo funciona el ciclo del nitrógeno en acuaponía?',
            'tipo_esperado': 'technical',
            'contexto_esperado': ['nutrient_balance']
        },
        {
            'categoria': 'CONSECUENCIAS',
            'pregunta': '¿Qué pasa si la temperatura del agua sube demasiado?',
            'tipo_esperado': 'consequence',
            'contexto_esperado': ['temperature_control']
        },
        {
            'categoria': 'COMPARACIÓN',
            'pregunta': '¿Cuál es la diferencia entre acuaponía y hidroponía?',
            'tipo_esperado': 'comparative',
            'contexto_esperado': []
        }
    ]
    
    print("🔍 Probando análisis de preguntas...")
    
    for i, pregunta_test in enumerate(preguntas_razonamiento, 1):
        print(f"\n{i}. {pregunta_test['categoria']}")
        print(f"❓ Pregunta: {pregunta_test['pregunta']}")
        
        # Analizar pregunta
        analisis = reasoning_engine.analyze_question(pregunta_test['pregunta'])
        
        print(f"🔍 Tipo detectado: {analisis['primary_strategy']}")
        print(f"🎯 Tipo esperado: {pregunta_test['tipo_esperado']}")
        print(f"📊 Tipos detectados: {analisis['detected_types']}")
        print(f"🌱 Contextos acuaponía: {analisis['acuaponia_contexts']}")
        
        # Verificar precisión del análisis
        tipo_correcto = analisis['primary_strategy'] == pregunta_test['tipo_esperado']
        print(f"✅ Tipo correcto: {'SÍ' if tipo_correcto else 'NO'}")
        
        # Mostrar cadena de razonamiento
        if analisis['reasoning_chain']:
            print(f"🧠 Razonamiento: {analisis['reasoning_chain'][0]}")
    
    return preguntas_razonamiento

def test_respuestas_inteligentes():
    """Test de respuestas con razonamiento inteligente"""
    print(f"\n🤖 TEST DE RESPUESTAS INTELIGENTES")
    print("=" * 60)
    
    # Cargar dataset y crear modelo
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Preguntas específicas para probar razonamiento
    preguntas_prueba = [
        {
            'pregunta': '¿Por qué no debo echar ácido a un cultivo acuapónico?',
            'descripcion': 'Pregunta de seguridad química'
        },
        {
            'pregunta': '¿Qué pasa si la temperatura del agua sube a 35°C?',
            'descripcion': 'Pregunta de consecuencias'
        },
        {
            'pregunta': '¿Cómo soluciono el problema de pH alto?',
            'descripcion': 'Pregunta de solución de problemas'
        },
        {
            'pregunta': '¿Por qué las plantas crecen mejor en acuaponía?',
            'descripcion': 'Pregunta de razonamiento causal'
        },
        {
            'pregunta': '¿Cuál es la diferencia entre acuaponía y piscicultura?',
            'descripcion': 'Pregunta comparativa'
        }
    ]
    
    for i, pregunta_test in enumerate(preguntas_prueba, 1):
        print(f"\n{i}. {pregunta_test['descripcion']}")
        print(f"❓ Pregunta: {pregunta_test['pregunta']}")
        
        # Generar respuesta base
        respuesta_base = model.generate(pregunta_test['pregunta'], max_length=60, temperature=0.3)
        print(f"🤖 Respuesta base: {respuesta_base}")
        
        # Aplicar razonamiento inteligente
        respuesta_razonada = apply_intelligent_reasoning(pregunta_test['pregunta'], respuesta_base)
        print(f"🧠 Respuesta con razonamiento:")
        print(f"   {respuesta_razonada}")
        
        # Aplicar mejora generativa completa
        respuesta_final = mejorar_respuesta_generativa(pregunta_test['pregunta'], respuesta_base)
        print(f"✨ Respuesta final mejorada:")
        print(f"   {respuesta_final}")
        
        # Evaluar calidad de la respuesta
        calidad_base = len(respuesta_base.split()) if respuesta_base else 0
        calidad_razonada = len(respuesta_razonada.split()) if respuesta_razonada else 0
        calidad_final = len(respuesta_final.split()) if respuesta_final else 0
        
        print(f"📊 Calidad - Base: {calidad_base} palabras, Razonada: {calidad_razonada} palabras, Final: {calidad_final} palabras")

def test_casos_especificos_razonamiento():
    """Test de casos específicos de razonamiento"""
    print(f"\n🎯 TEST DE CASOS ESPECÍFICOS DE RAZONAMIENTO")
    print("=" * 60)
    
    reasoning_engine = ReasoningEngine()
    
    # Casos específicos de razonamiento
    casos_especificos = [
        {
            'caso': 'SEGURIDAD CON ÁCIDOS',
            'pregunta': '¿Puedo usar ácido clorhídrico para bajar el pH?',
            'respuesta_esperada': 'NO, es peligroso para el sistema acuapónico'
        },
        {
            'caso': 'MANEJO DE TEMPERATURA',
            'pregunta': '¿Qué temperatura es óptima para tilapia en acuaponía?',
            'respuesta_esperada': 'Entre 24-30°C es el rango óptimo'
        },
        {
            'caso': 'CICLO DEL NITRÓGENO',
            'pregunta': '¿Por qué son importantes las bacterias en acuaponía?',
            'respuesta_esperada': 'Convierten amonio tóxico en nitratos útiles'
        },
        {
            'caso': 'OXIGENACIÓN',
            'pregunta': '¿Cuánto oxígeno necesitan los peces?',
            'respuesta_esperada': 'Al menos 5 mg/L para supervivencia'
        },
        {
            'caso': 'NUTRIENTES',
            'pregunta': '¿Qué nutrientes necesitan las plantas en acuaponía?',
            'respuesta_esperada': 'Nitrógeno, fósforo, potasio y micronutrientes'
        }
    ]
    
    for caso in casos_especificos:
        print(f"\n🔍 Caso: {caso['caso']}")
        print(f"❓ Pregunta: {caso['pregunta']}")
        
        # Analizar pregunta
        analisis = reasoning_engine.analyze_question(caso['pregunta'])
        
        print(f"🧠 Estrategia: {analisis['primary_strategy']}")
        print(f"🌱 Contextos: {analisis['acuaponia_contexts']}")
        
        # Generar respuesta con razonamiento
        respuesta_razonada = apply_intelligent_reasoning(caso['pregunta'], "Respuesta base del modelo")
        
        print(f"💡 Respuesta con razonamiento:")
        print(f"   {respuesta_razonada[:200]}...")
        
        print(f"🎯 Esperado: {caso['respuesta_esperada']}")

def evaluar_inteligencia_respuestas():
    """Evaluar la inteligencia de las respuestas"""
    print(f"\n📊 EVALUACIÓN DE INTELIGENCIA DE RESPUESTAS")
    print("=" * 60)
    
    # Cargar modelo
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    model.train(dataset)
    
    # Preguntas de evaluación
    preguntas_evaluacion = [
        '¿Por qué no debo echar ácido a un cultivo acuapónico?',
        '¿Qué pasa si la temperatura sube demasiado?',
        '¿Cómo funciona el ciclo del nitrógeno?',
        '¿Por qué las plantas crecen bien en acuaponía?',
        '¿Qué hago si los peces están en la superficie?'
    ]
    
    puntuaciones = {
        'base': [],
        'razonamiento': [],
        'final': []
    }
    
    for pregunta in preguntas_evaluacion:
        print(f"\n❓ Pregunta: {pregunta}")
        
        # Respuesta base
        respuesta_base = model.generate(pregunta, max_length=60, temperature=0.3)
        print(f"🤖 Base: {respuesta_base}")
        
        # Respuesta con razonamiento
        respuesta_razonada = apply_intelligent_reasoning(pregunta, respuesta_base)
        print(f"🧠 Razonamiento: {respuesta_razonada[:100]}...")
        
        # Respuesta final
        respuesta_final = mejorar_respuesta_generativa(pregunta, respuesta_base)
        print(f"✨ Final: {respuesta_final[:100]}...")
        
        # Evaluar calidad
        calidad_base = len(respuesta_base.split()) if respuesta_base else 0
        calidad_razonada = len(respuesta_razonada.split()) if respuesta_razonada else 0
        calidad_final = len(respuesta_final.split()) if respuesta_final else 0
        
        puntuaciones['base'].append(calidad_base)
        puntuaciones['razonamiento'].append(calidad_razonada)
        puntuaciones['final'].append(calidad_final)
    
    # Resumen de evaluación
    print(f"\n📈 RESUMEN DE EVALUACIÓN")
    print("=" * 60)
    
    for tipo, puntuaciones_tipo in puntuaciones.items():
        promedio = sum(puntuaciones_tipo) / len(puntuaciones_tipo)
        print(f"{tipo.capitalize()}: {promedio:.1f} palabras promedio")
    
    # Calcular mejora
    mejora_razonamiento = (sum(puntuaciones['razonamiento']) / len(puntuaciones['razonamiento'])) / (sum(puntuaciones['base']) / len(puntuaciones['base'])) * 100
    mejora_final = (sum(puntuaciones['final']) / len(puntuaciones['final'])) / (sum(puntuaciones['base']) / len(puntuaciones['base'])) * 100
    
    print(f"\n📊 Mejora con razonamiento: {mejora_razonamiento:.1f}%")
    print(f"📊 Mejora final: {mejora_final:.1f}%")

def main():
    """Función principal"""
    print("🧠 TEST DE RAZONAMIENTO INTELIGENTE - ULTRAEFFICIENTLLM")
    print("=" * 60)
    
    # Test de análisis de razonamiento
    preguntas_razonamiento = test_razonamiento_inteligente()
    
    # Test de respuestas inteligentes
    test_respuestas_inteligentes()
    
    # Test de casos específicos
    test_casos_especificos_razonamiento()
    
    # Evaluación de inteligencia
    evaluar_inteligencia_respuestas()
    
    print(f"\n✅ Test de razonamiento inteligente completado.")
    print(f"🎯 El sistema ahora puede analizar preguntas y aplicar estrategias de razonamiento específicas.")

if __name__ == "__main__":
    main() 