#!/usr/bin/env python3
"""
🧠 TEST POST-PROCESAMIENTO GENERATIVO - ULTRAEFFICIENTLLM
=========================================================

Test que evalúa el sistema de post-procesamiento para mejorar respuestas generativas.
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
    
    # Verificar uso de metáforas y analogías
    metaforas = ['como', 'es como', 'parece', 'similar a', 'igual que', 'mágico', 'revolucionario', 'fascinante', 'increíble']
    metaforas_encontradas = sum(1 for metafora in metaforas if metafora.lower() in respuesta.lower())
    if metaforas_encontradas > 0:
        puntuacion += 30
    
    # Verificar uso de lenguaje creativo
    lenguaje_creativo = ['imagin', 'fantástic', 'increíbl', 'perfect', 'mágic', 'revolucionari', 'ecosistema', 'danza', 'fábrica']
    creativo_encontrado = sum(1 for palabra in lenguaje_creativo if palabra.lower() in respuesta.lower())
    if creativo_encontrado > 0:
        puntuacion += 30
    
    # Verificar que no sea una respuesta repetitiva
    palabras = respuesta.split()
    palabras_unicas = set(palabras)
    if len(palabras_unicas) / len(palabras) > 0.7:
        puntuacion += 20
    else:
        puntuacion -= 10
    
    # Verificar longitud adecuada
    if 8 <= len(palabras) <= 25:
        puntuacion += 20
    else:
        puntuacion -= 10
    
    return max(0, min(100, puntuacion))

def evaluar_coherencia_tematica(respuesta, pregunta):
    """Evaluar que la respuesta sea coherente con el tema de acuaponía"""
    puntuacion = 0
    
    # Palabras relacionadas con acuaponía
    palabras_acuaponia = ['acuaponía', 'peces', 'plantas', 'agua', 'nutrientes', 'sistema', 'desechos', 'bacterias', 'pH', 'oxígeno', 'filtración']
    
    # Contar palabras relacionadas con acuaponía
    palabras_encontradas = sum(1 for palabra in palabras_acuaponia if palabra.lower() in respuesta.lower())
    if palabras_encontradas >= 1:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    # Verificar que la respuesta no sea completamente irrelevante
    if len(respuesta.split()) >= 5:
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
    print("🧠 TEST POST-PROCESAMIENTO GENERATIVO")
    print("=" * 60)
    
    # Cargar dataset generativo
    dataset = cargar_dataset('../data/acuaponia_generativo.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset generativo cargado: {len(dataset)} líneas")
    
    # Crear modelo y enhancer
    print("\n🧠 Creando modelo y sistema de post-procesamiento...")
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    
    enhancer = GenerativeEnhancer()
    
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Pruebas con post-procesamiento
    print("\n🧪 PRUEBAS CON POST-PROCESAMIENTO GENERATIVO")
    print("=" * 60)
    
    pruebas = [
        {
            "categoria": "RAZONAMIENTO CAUSAL",
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "palabras_clave": ["nutrientes", "desechos", "peces", "naturales"]
        },
        {
            "categoria": "RAZONAMIENTO INFERENCIAL",
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "palabras_clave": ["nutrientes", "peces", "falta", "demasiados"]
        },
        {
            "categoria": "RAZONAMIENTO COMPARATIVO",
            "pregunta": "¿Cuál es la diferencia entre acuaponía y agricultura tradicional?",
            "palabras_clave": ["agua", "menos", "fertilizantes", "químicos"]
        },
        {
            "categoria": "RAZONAMIENTO SECUENCIAL",
            "pregunta": "¿Cómo funciona el ciclo del agua en acuaponía?",
            "palabras_clave": ["peces", "desechos", "plantas", "absorben", "limpia"]
        },
        {
            "categoria": "SOLUCIÓN DE PROBLEMAS",
            "pregunta": "¿Qué hago si las plantas están débiles?",
            "palabras_clave": ["nutrientes", "pH", "iluminación", "verificar"]
        }
    ]
    
    total_razonamiento_original = 0
    total_originalidad_original = 0
    total_coherencia_original = 0
    total_estructura_original = 0
    
    total_razonamiento_mejorada = 0
    total_originalidad_mejorada = 0
    total_coherencia_mejorada = 0
    total_estructura_mejorada = 0
    
    total_pruebas = len(pruebas)
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\n{i}. {prueba['categoria']}")
        print(f"❓ {prueba['pregunta']}")
        
        # Generar respuesta original
        respuesta_original = model.generate(prueba['pregunta'], max_length=60, temperature=0.4)
        print(f"🤖 Original: {respuesta_original}")
        
        # Mejorar respuesta con post-procesamiento
        respuesta_mejorada = mejorar_respuesta_generativa(prueba['pregunta'], respuesta_original)
        print(f"✨ Mejorada: {respuesta_mejorada}")
        
        # Evaluar respuesta original
        puntuacion_razonamiento_original = evaluar_razonamiento(respuesta_original, prueba['palabras_clave'])
        puntuacion_originalidad_original = evaluar_originalidad(respuesta_original)
        puntuacion_coherencia_original = evaluar_coherencia_tematica(respuesta_original, prueba['pregunta'])
        puntuacion_estructura_original = evaluar_estructura_gramatical(respuesta_original)
        
        # Evaluar respuesta mejorada
        puntuacion_razonamiento_mejorada = evaluar_razonamiento(respuesta_mejorada, prueba['palabras_clave'])
        puntuacion_originalidad_mejorada = evaluar_originalidad(respuesta_mejorada)
        puntuacion_coherencia_mejorada = evaluar_coherencia_tematica(respuesta_mejorada, prueba['pregunta'])
        puntuacion_estructura_mejorada = evaluar_estructura_gramatical(respuesta_mejorada)
        
        # Acumular puntuaciones
        total_razonamiento_original += puntuacion_razonamiento_original
        total_originalidad_original += puntuacion_originalidad_original
        total_coherencia_original += puntuacion_coherencia_original
        total_estructura_original += puntuacion_estructura_original
        
        total_razonamiento_mejorada += puntuacion_razonamiento_mejorada
        total_originalidad_mejorada += puntuacion_originalidad_mejorada
        total_coherencia_mejorada += puntuacion_coherencia_mejorada
        total_estructura_mejorada += puntuacion_estructura_mejorada
        
        # Mostrar comparación
        print(f"📊 Original  - Razonamiento: {puntuacion_razonamiento_original:.1f}%, Originalidad: {puntuacion_originalidad_original:.1f}%, Coherencia: {puntuacion_coherencia_original:.1f}%, Estructura: {puntuacion_estructura_original:.1f}%")
        print(f"📊 Mejorada  - Razonamiento: {puntuacion_razonamiento_mejorada:.1f}%, Originalidad: {puntuacion_originalidad_mejorada:.1f}%, Coherencia: {puntuacion_coherencia_mejorada:.1f}%, Estructura: {puntuacion_estructura_mejorada:.1f}%")
        
        # Calcular mejora
        mejora_razonamiento = puntuacion_razonamiento_mejorada - puntuacion_razonamiento_original
        mejora_originalidad = puntuacion_originalidad_mejorada - puntuacion_originalidad_original
        mejora_coherencia = puntuacion_coherencia_mejorada - puntuacion_coherencia_original
        mejora_estructura = puntuacion_estructura_mejorada - puntuacion_estructura_original
        
        print(f"📈 Mejora    - Razonamiento: {mejora_razonamiento:+.1f}%, Originalidad: {mejora_originalidad:+.1f}%, Coherencia: {mejora_coherencia:+.1f}%, Estructura: {mejora_estructura:+.1f}%")
    
    # Resultados finales
    promedio_razonamiento_original = total_razonamiento_original / total_pruebas
    promedio_originalidad_original = total_originalidad_original / total_pruebas
    promedio_coherencia_original = total_coherencia_original / total_pruebas
    promedio_estructura_original = total_estructura_original / total_pruebas
    promedio_general_original = (promedio_razonamiento_original + promedio_originalidad_original + promedio_coherencia_original + promedio_estructura_original) / 4
    
    promedio_razonamiento_mejorada = total_razonamiento_mejorada / total_pruebas
    promedio_originalidad_mejorada = total_originalidad_mejorada / total_pruebas
    promedio_coherencia_mejorada = total_coherencia_mejorada / total_pruebas
    promedio_estructura_mejorada = total_estructura_mejorada / total_pruebas
    promedio_general_mejorada = (promedio_razonamiento_mejorada + promedio_originalidad_mejorada + promedio_coherencia_mejorada + promedio_estructura_mejorada) / 4
    
    print("\n" + "="*60)
    print("📊 RESULTADOS FINALES POST-PROCESAMIENTO")
    print("="*60)
    print(f"RESPUESTAS ORIGINALES:")
    print(f"  Razonamiento: {promedio_razonamiento_original:.1f}%")
    print(f"  Originalidad: {promedio_originalidad_original:.1f}%")
    print(f"  Coherencia: {promedio_coherencia_original:.1f}%")
    print(f"  Estructura: {promedio_estructura_original:.1f}%")
    print(f"  General: {promedio_general_original:.1f}%")
    
    print(f"\nRESPUESTAS MEJORADAS:")
    print(f"  Razonamiento: {promedio_razonamiento_mejorada:.1f}%")
    print(f"  Originalidad: {promedio_originalidad_mejorada:.1f}%")
    print(f"  Coherencia: {promedio_coherencia_mejorada:.1f}%")
    print(f"  Estructura: {promedio_estructura_mejorada:.1f}%")
    print(f"  General: {promedio_general_mejorada:.1f}%")
    
    # Calcular mejoras totales
    mejora_total_razonamiento = promedio_razonamiento_mejorada - promedio_razonamiento_original
    mejora_total_originalidad = promedio_originalidad_mejorada - promedio_originalidad_original
    mejora_total_coherencia = promedio_coherencia_mejorada - promedio_coherencia_original
    mejora_total_estructura = promedio_estructura_mejorada - promedio_estructura_original
    mejora_total_general = promedio_general_mejorada - promedio_general_original
    
    print(f"\nMEJORAS TOTALES:")
    print(f"  Razonamiento: {mejora_total_razonamiento:+.1f}%")
    print(f"  Originalidad: {mejora_total_originalidad:+.1f}%")
    print(f"  Coherencia: {mejora_total_coherencia:+.1f}%")
    print(f"  Estructura: {mejora_total_estructura:+.1f}%")
    print(f"  General: {mejora_total_general:+.1f}%")
    
    # Evaluación cualitativa final
    print(f"\n🎯 EVALUACIÓN CUALITATIVA FINAL:")
    if mejora_total_general > 20:
        print("🟢 EXCELENTE: El post-procesamiento ha mejorado significativamente las respuestas")
        print("✅ El sistema está GENERANDO respuestas originales y creativas")
    elif mejora_total_general > 10:
        print("🟡 BUENO: El post-procesamiento ha mejorado las respuestas")
        print("✅ El sistema está GENERANDO con mejor calidad")
    elif mejora_total_general > 0:
        print("🟠 REGULAR: El post-procesamiento ha mejorado ligeramente las respuestas")
        print("⚠️  El sistema necesita más refinamiento")
    else:
        print("🔴 DEFICIENTE: El post-procesamiento no ha mejorado las respuestas")
        print("❌ El sistema necesita revisión")
    
    # Guardar modelo con post-procesamiento
    print(f"\n💾 Guardando modelo con post-procesamiento...")
    model.save_model("../models/acuaponia_post_procesamiento.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_post_procesamiento.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES:")
    if mejora_total_general > 0:
        print(f"✅ El sistema de post-procesamiento ha mejorado la calidad en {mejora_total_general:.1f}%")
        print(f"✅ Usar este sistema para aplicaciones que requieran respuestas originales")
        print(f"✅ El modelo puede generar respuestas similares a modelos generativos modernos")
    else:
        print(f"⚠️  El sistema de post-procesamiento necesita mejoras")
        print(f"💡 Considerar ajustar las metáforas y analogías")
        print(f"💡 El sistema necesita más refinamiento en la generación")

if __name__ == "__main__":
    main() 