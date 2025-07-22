#!/usr/bin/env python3
"""
🧠 TEST GENERATIVO AVANZADO - ULTRAEFFICIENTLLM
===============================================

Test que evalúa la capacidad generativa y originalidad del modelo.
"""

import sys
import os
sys.path.append('../src')

from ultra_efficient_llm import UltraEfficientLLM
import time
import re
import random

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

def evaluar_originalidad(respuesta):
    """Evaluar la originalidad y creatividad de la respuesta"""
    puntuacion = 0
    
    # Verificar que la respuesta no esté vacía
    if not respuesta.strip():
        return 0
    
    # Verificar uso de metáforas y analogías
    metaforas = ['como', 'es como', 'parece', 'similar a', 'igual que', 'mágico', 'revolucionario']
    metaforas_encontradas = sum(1 for metafora in metaforas if metafora.lower() in respuesta.lower())
    if metaforas_encontradas > 0:
        puntuacion += 25
    
    # Verificar uso de lenguaje creativo
    lenguaje_creativo = ['imagin', 'fantástic', 'increíbl', 'perfect', 'mágic', 'revolucionari', 'ecosistema']
    creativo_encontrado = sum(1 for palabra in lenguaje_creativo if palabra.lower() in respuesta.lower())
    if creativo_encontrado > 0:
        puntuacion += 25
    
    # Verificar que no sea una respuesta repetitiva
    palabras = respuesta.split()
    palabras_unicas = set(palabras)
    if len(palabras_unicas) / len(palabras) > 0.7:  # Al menos 70% de palabras únicas
        puntuacion += 25
    else:
        puntuacion -= 10
    
    # Verificar longitud adecuada (no demasiado corta ni larga)
    if 10 <= len(palabras) <= 30:
        puntuacion += 25
    else:
        puntuacion -= 10
    
    return max(0, min(100, puntuacion))

def evaluar_coherencia_tematica(respuesta, pregunta):
    """Evaluar que la respuesta sea coherente con el tema de acuaponía"""
    puntuacion = 0
    
    # Palabras relacionadas con acuaponía
    palabras_acuaponia = ['acuaponía', 'peces', 'plantas', 'agua', 'nutrientes', 'sistema', 'desechos', 'bacterias', 'pH', 'oxígeno', 'filtración', 'hidroponía', 'piscicultura']
    
    # Contar palabras relacionadas con acuaponía
    palabras_encontradas = sum(1 for palabra in palabras_acuaponia if palabra.lower() in respuesta.lower())
    if palabras_encontradas >= 2:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    # Verificar que la respuesta no sea completamente irrelevante
    if len(respuesta.split()) >= 8:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    return max(0, min(100, puntuacion))

def evaluar_estructura_gramatical(respuesta):
    """Evaluar la estructura gramatical básica"""
    puntuacion = 0
    
    # Verificar que comience con mayúscula
    if respuesta.strip()[0].isupper():
        puntuacion += 30
    else:
        puntuacion -= 15
    
    # Verificar que termine con punto
    if respuesta.strip().endswith('.'):
        puntuacion += 30
    else:
        puntuacion -= 15
    
    # Verificar que no tenga caracteres sueltos repetitivos
    caracteres_sueltos = re.findall(r'\s+[,\s]+\s+', respuesta)
    if not caracteres_sueltos:
        puntuacion += 40
    else:
        puntuacion -= 20
    
    return max(0, min(100, puntuacion))

def main():
    """Función principal"""
    print("🧠 TEST GENERATIVO AVANZADO - ULTRAEFFICIENTLLM")
    print("=" * 60)
    
    # Cargar dataset generativo
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset generativo cargado: {len(dataset)} líneas")
    print("📖 Características del dataset:")
    print("   - Variaciones creativas y originales")
    print("   - Metáforas y analogías")
    print("   - Lenguaje accesible y atractivo")
    print("   - Respuestas similares a modelos generativos")
    
    # Crear modelo con configuración generativa
    print("\n🧠 Creando modelo generativo...")
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
    
    # Pruebas generativas
    print("\n🧪 PRUEBAS GENERATIVAS AVANZADAS")
    print("=" * 60)
    
    pruebas = [
        {
            "categoria": "RAZONAMIENTO CAUSAL CREATIVO",
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "palabras_clave": ["nutrientes", "desechos", "peces", "naturales"],
            "respuesta_esperada": "Las plantas crecen excepcionalmente bien porque reciben nutrientes naturales de los desechos de los peces."
        },
        {
            "categoria": "RAZONAMIENTO INFERENCIAL CREATIVO",
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "palabras_clave": ["nutrientes", "peces", "falta", "demasiados"],
            "respuesta_esperada": "Si las plantas están amarillas, es como una señal de SOS del sistema."
        },
        {
            "categoria": "RAZONAMIENTO COMPARATIVO CREATIVO",
            "pregunta": "¿Cuál es la diferencia entre acuaponía y agricultura tradicional?",
            "palabras_clave": ["agua", "menos", "fertilizantes", "químicos"],
            "respuesta_esperada": "La acuaponía es como un smartphone moderno comparado con un teléfono fijo antiguo."
        },
        {
            "categoria": "RAZONAMIENTO SECUENCIAL CREATIVO",
            "pregunta": "¿Cómo funciona el ciclo del agua en acuaponía?",
            "palabras_clave": ["peces", "desechos", "plantas", "absorben", "limpia"],
            "respuesta_esperada": "El ciclo del agua es como una danza perfecta entre peces y plantas."
        },
        {
            "categoria": "SOLUCIÓN DE PROBLEMAS CREATIVA",
            "pregunta": "¿Qué hago si las plantas están débiles?",
            "palabras_clave": ["nutrientes", "pH", "iluminación", "verificar"],
            "respuesta_esperada": "Si las plantas están débiles, es como diagnosticar a un paciente."
        }
    ]
    
    total_razonamiento = 0
    total_originalidad = 0
    total_coherencia = 0
    total_estructura = 0
    total_pruebas = len(pruebas)
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\n{i}. {prueba['categoria']}")
        print(f"❓ {prueba['pregunta']}")
        
        # Generar respuesta con temperatura más alta para creatividad
        respuesta = model.generate(prueba['pregunta'], max_length=60, temperature=0.4)
        print(f"🤖 {respuesta}")
        
        # Evaluar diferentes aspectos
        puntuacion_razonamiento = evaluar_razonamiento(respuesta, prueba['palabras_clave'])
        puntuacion_originalidad = evaluar_originalidad(respuesta)
        puntuacion_coherencia = evaluar_coherencia_tematica(respuesta, prueba['pregunta'])
        puntuacion_estructura = evaluar_estructura_gramatical(respuesta)
        
        total_razonamiento += puntuacion_razonamiento
        total_originalidad += puntuacion_originalidad
        total_coherencia += puntuacion_coherencia
        total_estructura += puntuacion_estructura
        
        print(f"📊 Razonamiento: {puntuacion_razonamiento:.1f}%")
        print(f"🎨 Originalidad: {puntuacion_originalidad:.1f}%")
        print(f"🔗 Coherencia: {puntuacion_coherencia:.1f}%")
        print(f"📝 Estructura: {puntuacion_estructura:.1f}%")
        print(f"🎯 Esperado: {prueba['respuesta_esperada']}")
        
        # Evaluación cualitativa
        promedio_prueba = (puntuacion_razonamiento + puntuacion_originalidad + puntuacion_coherencia + puntuacion_estructura) / 4
        if promedio_prueba >= 75:
            print("✅ EXCELENTE: Respuesta creativa y coherente")
        elif promedio_prueba >= 50:
            print("🟡 BUENO: Respuesta aceptable con elementos creativos")
        else:
            print("❌ DEFICIENTE: Respuesta necesita más creatividad")
    
    # Resultados finales
    promedio_razonamiento = total_razonamiento / total_pruebas
    promedio_originalidad = total_originalidad / total_pruebas
    promedio_coherencia = total_coherencia / total_pruebas
    promedio_estructura = total_estructura / total_pruebas
    promedio_general = (promedio_razonamiento + promedio_originalidad + promedio_coherencia + promedio_estructura) / 4
    
    print("\n" + "="*60)
    print("📊 RESULTADOS FINALES GENERATIVOS")
    print("="*60)
    print(f"Razonamiento promedio: {promedio_razonamiento:.1f}%")
    print(f"Originalidad promedio: {promedio_originalidad:.1f}%")
    print(f"Coherencia temática: {promedio_coherencia:.1f}%")
    print(f"Estructura gramatical: {promedio_estructura:.1f}%")
    print(f"Puntuación general: {promedio_general:.1f}%")
    
    # Comparación con resultados anteriores
    puntuacion_optima = 71.0
    mejora_vs_optima = promedio_general - puntuacion_optima
    
    print(f"\n📈 COMPARACIÓN:")
    print(f"Puntuación óptima (solo razonamiento): {puntuacion_optima}%")
    print(f"Puntuación generativa (general): {promedio_general:.1f}%")
    print(f"Mejora en creatividad: {mejora_vs_optima:+.1f}%")
    
    # Evaluación cualitativa final
    print(f"\n🎯 EVALUACIÓN CUALITATIVA FINAL:")
    if promedio_general >= 80:
        print("🟢 EXCELENTE: El modelo muestra capacidad generativa avanzada")
        print("✅ El modelo está GENERANDO respuestas originales y creativas")
    elif promedio_general >= 60:
        print("🟡 BUENO: El modelo muestra capacidad generativa básica")
        print("✅ El modelo está GENERANDO con elementos creativos")
    elif promedio_general >= 40:
        print("🟠 REGULAR: El modelo muestra algo de creatividad pero necesita mejorar")
        print("⚠️  El modelo está en el límite entre generar y repetir")
    else:
        print("🔴 DEFICIENTE: El modelo parece solo repetir sin creatividad")
        print("❌ El modelo está REPITIENDO sin originalidad")
    
    # Guardar modelo generativo
    print(f"\n💾 Guardando modelo generativo...")
    model.save_model("../models/acuaponia_generativo_avanzado.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_generativo_avanzado.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES:")
    if mejora_vs_optima > 0:
        print(f"✅ El dataset generativo ha mejorado la creatividad en {mejora_vs_optima:.1f}%")
        print(f"✅ Usar este modelo para aplicaciones que requieran respuestas originales")
        print(f"✅ El modelo puede generar respuestas similares a modelos generativos modernos")
    else:
        print(f"⚠️  El dataset necesita más mejoras para capacidad generativa")
        print(f"💡 Considerar agregar más ejemplos de metáforas y analogías")
        print(f"💡 El modelo necesita más entrenamiento en creatividad")

if __name__ == "__main__":
    main() 