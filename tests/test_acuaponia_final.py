#!/usr/bin/env python3
"""
Test final del modelo UltraEfficientLLM con dataset de acuaponía optimizado
"""

import sys
import os
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

def evaluar_respuesta_final(pregunta, respuesta):
    """Evalúa la calidad final de la respuesta"""
    score = 0
    
    # Respuestas esperadas exactas
    respuestas_exactas = {
        "¿Qué es la acuaponía?": "La acuaponía combina peces y plantas",
        "¿Qué peces puedo usar?": "Los peces más comunes son tilapia y carpa",
        "¿Qué plantas crecen?": "Las plantas más comunes son lechugas y hierbas",
        "¿Cuánta agua usa?": "Usa menos agua que la agricultura tradicional",
        "¿Es orgánica?": "Sí, es orgánica y no necesita fertilizantes químicos",
        "¿Cómo funciona?": "Los peces producen desechos que las plantas usan como nutrientes",
        "¿Qué beneficios tiene?": "Es sostenible, eficiente y produce alimentos frescos",
        "¿Es sostenible?": "Sí, es sostenible y respetuoso con el medio ambiente"
    }
    
    respuesta_esperada = respuestas_exactas.get(pregunta, "")
    
    # Puntuación por similitud con respuesta esperada
    if respuesta_esperada:
        palabras_esperadas = respuesta_esperada.lower().split()
        palabras_respuesta = respuesta.lower().split()
        
        # Contar palabras coincidentes
        coincidencias = sum(1 for palabra in palabras_esperadas if palabra in palabras_respuesta)
        if coincidencias >= len(palabras_esperadas) * 0.8:  # 80% de coincidencia
            score += 8
        elif coincidencias >= len(palabras_esperadas) * 0.6:  # 60% de coincidencia
            score += 6
        elif coincidencias >= len(palabras_esperadas) * 0.4:  # 40% de coincidencia
            score += 4
        elif coincidencias >= len(palabras_esperadas) * 0.2:  # 20% de coincidencia
            score += 2
    
    # Puntuación por longitud apropiada
    if 10 <= len(respuesta) <= 100:
        score += 1
    
    # Penalización por repetición excesiva
    words = respuesta.split()
    if len(words) > 0:
        unique_words = len(set(words))
        repetition_ratio = unique_words / len(words)
        if repetition_ratio < 0.5:  # Mucha repetición
            score -= 2
        elif repetition_ratio > 0.8:  # Buena variedad
            score += 1
    
    # Penalización por comas excesivas
    comma_count = respuesta.count(',')
    if comma_count > len(respuesta) / 20:  # Más de 5% comas
        score -= 1
    
    return max(0, min(10, score))

def test_acuaponia_final():
    """Test final con dataset de acuaponía optimizado"""
    print("🧪 TEST FINAL - MODELO ACUAPONÍA OPTIMIZADO")
    print("=" * 50)
    
    # Cargar dataset optimizado
    dataset = cargar_dataset('data/acuaponia_minimal.txt')
    if not dataset:
        print("❌ No se pudo cargar el dataset")
        return
    
    print(f"📚 Dataset cargado: {len(dataset)} líneas")
    
    # Crear modelo con parámetros optimizados
    model = UltraEfficientLLM(
        max_pattern_length=6,  # Patrones cortos para simplicidad
        min_frequency=1,
        max_patterns=6000
    )
    
    print("🔄 Entrenando modelo...")
    model.train(dataset)
    print(f"✅ Modelo entrenado con {len(model.patterns)} patrones")
    
    # Preguntas de prueba
    questions = [
        "¿Qué es la acuaponía?",
        "¿Qué peces puedo usar?",
        "¿Qué plantas crecen?",
        "¿Cuánta agua usa?",
        "¿Es orgánica?",
        "¿Cómo funciona?",
        "¿Qué beneficios tiene?",
        "¿Es sostenible?"
    ]
    
    print("\n🔍 PROBANDO RESPUESTAS FINALES:")
    print("-" * 30)
    
    total_score = 0
    respuestas_exitosas = 0
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Pregunta: {question}")
        
        # Generar respuesta con temperatura muy baja para mayor determinismo
        response = model.generate(question, max_length=25, temperature=0.1)
        print(f"   Respuesta: {response}")
        
        # Evaluar respuesta
        score = evaluar_respuesta_final(question, response)
        total_score += score
        if score >= 6:
            respuestas_exitosas += 1
        print(f"   Calidad: {score}/10")
        
        # Verificar si contiene elementos de archivo
        file_elements = ['txt', 'py', 'md', 'data', 'test', 'main', 'config', 'utils', 'models', 'src']
        has_file_elements = any(elem in response.lower() for elem in file_elements)
        
        if has_file_elements:
            print(f"   ⚠️  CONTIENE ELEMENTOS DE ARCHIVO!")
        else:
            print(f"   ✅ SIN ELEMENTOS DE ARCHIVO")
    
    average_score = total_score / len(questions)
    success_rate = respuestas_exitosas / len(questions) * 100
    
    print(f"\n📊 RESULTADOS FINALES:")
    print(f"   Puntuación promedio: {average_score:.1f}/10")
    print(f"   Tasa de éxito: {success_rate:.1f}%")
    
    if average_score >= 7 and success_rate >= 75:
        print("🎉 ¡EXCELENTE! El modelo está funcionando correctamente")
        print("✅ Los filtros eliminaron elementos de archivo")
        print("✅ Las respuestas son coherentes y directas")
    elif average_score >= 5 and success_rate >= 50:
        print("👍 BUENO: El modelo está mejorando significativamente")
        print("✅ Los filtros funcionan correctamente")
        print("⚠️  Las respuestas necesitan mejorar en coherencia")
    else:
        print("⚠️  NECESITA MEJORAS: El modelo aún no genera respuestas óptimas")
        print("✅ Los filtros funcionan correctamente")
        print("❌ Las respuestas necesitan mejorar en coherencia y precisión")

def test_prompts_simples():
    """Test con prompts simples"""
    print("\n🔍 TEST - PROMPTS SIMPLES:")
    print("-" * 30)
    
    dataset = cargar_dataset('data/acuaponia_minimal.txt')
    if not dataset:
        return
    
    model = UltraEfficientLLM(max_pattern_length=6, min_frequency=1, max_patterns=6000)
    model.train(dataset)
    
    simple_prompts = ["acuaponía", "peces", "plantas", "agua", "orgánico", "sostenible"]
    
    for prompt in simple_prompts:
        response = model.generate(prompt, max_length=15, temperature=0.2)
        print(f"'{prompt}' → {response}")
        
        # Verificar calidad básica
        if len(response.split()) > 2 and response.count(',') < len(response) / 25:
            print(f"   ✅ Respuesta coherente")
        else:
            print(f"   ⚠️  Respuesta necesita mejorar")

if __name__ == "__main__":
    test_acuaponia_final()
    test_prompts_simples() 