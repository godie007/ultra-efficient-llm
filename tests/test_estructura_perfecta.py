#!/usr/bin/env python3
"""
🧠 TEST FINAL DE ESTRUCTURA PERFECTA - ULTRAEFFICIENTLLM
========================================================

Test final con configuración óptima para estructura gramatical perfecta.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
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

def evaluar_razonamiento(respuesta, palabras_clave):
    """Evaluar si la respuesta muestra razonamiento"""
    puntuacion = 0
    for palabra in palabras_clave:
        if palabra.lower() in respuesta.lower():
            puntuacion += 1
    return (puntuacion / len(palabras_clave)) * 100

def evaluar_gramatica_perfecta(respuesta):
    """Evaluar la calidad gramatical perfecta de la respuesta"""
    puntuacion = 0
    
    # Verificar que la respuesta no esté vacía
    if not respuesta.strip():
        return 0
    
    # Verificar que comience con mayúscula
    if respuesta.strip()[0].isupper():
        puntuacion += 25
    else:
        puntuacion -= 25
    
    # Verificar que termine con punto
    if respuesta.strip().endswith('.'):
        puntuacion += 25
    else:
        puntuacion -= 25
    
    # Verificar que no tenga caracteres sueltos repetitivos
    caracteres_sueltos = re.findall(r'\s+[,\s]+\s+', respuesta)
    if not caracteres_sueltos:
        puntuacion += 25
    else:
        puntuacion -= 25
    
    # Verificar que tenga estructura de oración completa (mínimo 8 palabras)
    palabras = respuesta.split()
    if len(palabras) >= 8:
        puntuacion += 25
    else:
        puntuacion -= 25
    
    return max(0, min(100, puntuacion))

def evaluar_consistencia_perfecta(respuesta, pregunta):
    """Evaluar la consistencia perfecta entre pregunta y respuesta"""
    puntuacion = 0
    
    # Verificar que la respuesta no sea la pregunta repetida
    if respuesta.lower().strip() == pregunta.lower().strip():
        return 0
    
    # Verificar que la respuesta contenga información relevante
    palabras_pregunta = set(pregunta.lower().split())
    palabras_respuesta = set(respuesta.lower().split())
    
    # Al menos 40% de palabras de la pregunta deben estar en la respuesta
    palabras_comunes = palabras_pregunta.intersection(palabras_respuesta)
    if len(palabras_comunes) / len(palabras_pregunta) > 0.4:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    # Verificar que la respuesta sea suficientemente larga
    if len(respuesta.split()) >= 10:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    return max(0, min(100, puntuacion))

def main():
    """Función principal"""
    print("🧠 TEST FINAL DE ESTRUCTURA PERFECTA")
    print("=" * 60)
    
    # Cargar dataset de estructura perfecta
    dataset = cargar_dataset('../data/acuaponia_estructura_perfecta.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset de estructura perfecta cargado: {len(dataset)} líneas")
    print("📖 Características del dataset:")
    print("   - Estructura gramatical perfecta")
    print("   - Respuestas completas y coherentes")
    print("   - Ejemplos de respuestas perfectas")
    print("   - Consistencia total entre pregunta y respuesta")
    
    # Crear modelo con configuración óptima
    print("\n🧠 Creando modelo con configuración óptima...")
    model = UltraEfficientLLM(
        max_pattern_length=6,  # Patrones moderados
        min_frequency=1,
        max_patterns=8000      # Patrones suficientes
    )
    
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Pruebas finales
    print("\n🧪 PRUEBAS FINALES DE ESTRUCTURA PERFECTA")
    print("=" * 60)
    
    pruebas = [
        {
            "categoria": "RAZONAMIENTO CAUSAL",
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "palabras_clave": ["nutrientes", "desechos", "peces", "naturales"],
            "respuesta_esperada": "Las plantas crecen bien en acuaponía porque reciben nutrientes naturales de los desechos de los peces."
        },
        {
            "categoria": "RAZONAMIENTO INFERENCIAL",
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "palabras_clave": ["nutrientes", "peces", "falta", "demasiados"],
            "respuesta_esperada": "Si las plantas están amarillas, puede ser falta de nutrientes o demasiados peces en el sistema."
        },
        {
            "categoria": "RAZONAMIENTO COMPARATIVO",
            "pregunta": "¿Cuál es la diferencia entre acuaponía y agricultura tradicional?",
            "palabras_clave": ["agua", "menos", "fertilizantes", "químicos"],
            "respuesta_esperada": "La acuaponía usa menos agua y no necesita fertilizantes químicos, a diferencia de la agricultura tradicional."
        },
        {
            "categoria": "RAZONAMIENTO SECUENCIAL",
            "pregunta": "¿Cómo funciona el ciclo del agua en acuaponía?",
            "palabras_clave": ["peces", "desechos", "plantas", "absorben", "limpia"],
            "respuesta_esperada": "El ciclo del agua en acuaponía funciona así: los peces producen desechos, las plantas absorben nutrientes, el agua se limpia y vuelve a los peces."
        },
        {
            "categoria": "SOLUCIÓN DE PROBLEMAS",
            "pregunta": "¿Qué hago si las plantas están débiles?",
            "palabras_clave": ["nutrientes", "pH", "iluminación", "verificar"],
            "respuesta_esperada": "Si las plantas están débiles, debes verificar los nutrientes en el agua, ajustar el pH y revisar la iluminación."
        }
    ]
    
    total_razonamiento = 0
    total_gramatica = 0
    total_consistencia = 0
    total_pruebas = len(pruebas)
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\n{i}. {prueba['categoria']}")
        print(f"❓ {prueba['pregunta']}")
        
        respuesta = model.generate(prueba['pregunta'], max_length=60, temperature=0.1)
        print(f"🤖 {respuesta}")
        
        # Evaluar razonamiento
        puntuacion_razonamiento = evaluar_razonamiento(respuesta, prueba['palabras_clave'])
        total_razonamiento += puntuacion_razonamiento
        
        # Evaluar gramática perfecta
        puntuacion_gramatica = evaluar_gramatica_perfecta(respuesta)
        total_gramatica += puntuacion_gramatica
        
        # Evaluar consistencia perfecta
        puntuacion_consistencia = evaluar_consistencia_perfecta(respuesta, prueba['pregunta'])
        total_consistencia += puntuacion_consistencia
        
        print(f"📊 Razonamiento: {puntuacion_razonamiento:.1f}%")
        print(f"📝 Gramática: {puntuacion_gramatica:.1f}%")
        print(f"🔗 Consistencia: {puntuacion_consistencia:.1f}%")
        print(f"🎯 Esperado: {prueba['respuesta_esperada']}")
        
        # Evaluación cualitativa
        promedio_prueba = (puntuacion_razonamiento + puntuacion_gramatica + puntuacion_consistencia) / 3
        if promedio_prueba >= 80:
            print("✅ EXCELENTE: Respuesta perfecta y coherente")
        elif promedio_prueba >= 60:
            print("🟡 BUENO: Respuesta aceptable")
        else:
            print("❌ DEFICIENTE: Respuesta necesita mejora")
    
    # Resultados finales
    promedio_razonamiento = total_razonamiento / total_pruebas
    promedio_gramatica = total_gramatica / total_pruebas
    promedio_consistencia = total_consistencia / total_pruebas
    promedio_general = (promedio_razonamiento + promedio_gramatica + promedio_consistencia) / 3
    
    print("\n" + "="*60)
    print("📊 RESULTADOS FINALES")
    print("="*60)
    print(f"Razonamiento promedio: {promedio_razonamiento:.1f}%")
    print(f"Gramática promedio: {promedio_gramatica:.1f}%")
    print(f"Consistencia promedio: {promedio_consistencia:.1f}%")
    print(f"Puntuación general: {promedio_general:.1f}%")
    
    # Comparación con todos los resultados anteriores
    puntuacion_original = 51.7
    puntuacion_optima = 71.0
    puntuacion_gramatica_anterior = 49.7
    mejora_vs_original = promedio_general - puntuacion_original
    mejora_vs_optima = promedio_general - puntuacion_optima
    mejora_vs_gramatica = promedio_general - puntuacion_gramatica_anterior
    
    print(f"\n📈 COMPARACIÓN CON TODOS LOS RESULTADOS:")
    print(f"Puntuación original: {puntuacion_original}%")
    print(f"Puntuación óptima: {puntuacion_optima}%")
    print(f"Puntuación gramática anterior: {puntuacion_gramatica_anterior}%")
    print(f"Puntuación estructura perfecta: {promedio_general:.1f}%")
    print(f"Mejora vs original: {mejora_vs_original:+.1f}%")
    print(f"Mejora vs óptima: {mejora_vs_optima:+.1f}%")
    print(f"Mejora vs gramática: {mejora_vs_gramatica:+.1f}%")
    
    # Evaluación cualitativa final
    print(f"\n🎯 EVALUACIÓN CUALITATIVA FINAL:")
    if promedio_general >= 80:
        print("🟢 EXCELENTE: El modelo muestra razonamiento, gramática y consistencia perfectos")
        print("✅ El modelo está RAZONANDO y RESPONDIENDO perfectamente")
    elif promedio_general >= 60:
        print("🟡 BUENO: El modelo muestra razonamiento básico con buena estructura")
        print("✅ El modelo está RAZONANDO con estructura aceptable")
    elif promedio_general >= 40:
        print("🟠 REGULAR: El modelo muestra algo de razonamiento pero necesita mejorar estructura")
        print("⚠️  El modelo está en el límite entre razonar y autocompletar")
    else:
        print("🔴 DEFICIENTE: El modelo parece solo autocompletar sin estructura")
        print("❌ El modelo está AUTOCOMPLETANDO sin coherencia")
    
    # Guardar modelo final
    print(f"\n💾 Guardando modelo final...")
    model.save_model("../models/acuaponia_estructura_perfecta.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_estructura_perfecta.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES:")
    if mejora_vs_gramatica > 0:
        print(f"✅ El dataset de estructura perfecta ha mejorado la calidad en {mejora_vs_gramatica:.1f}%")
        print(f"✅ Usar este modelo para aplicaciones que requieran respuestas perfectas")
        print(f"✅ El modelo puede manejar preguntas con estructura gramatical correcta")
    else:
        print(f"⚠️  El dataset necesita más mejoras para estructura perfecta")
        print(f"💡 Considerar diferentes enfoques de entrenamiento")
        print(f"💡 El modelo puede necesitar arquitecturas alternativas")

if __name__ == "__main__":
    main() 