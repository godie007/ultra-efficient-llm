#!/usr/bin/env python3
"""
🧠 TEST AVANZADO DE GRAMÁTICA Y CONSISTENCIA - ULTRAEFFICIENTLLM
================================================================

Test que evalúa razonamiento, gramática y consistencia de las respuestas.
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

def evaluar_gramatica(respuesta):
    """Evaluar la calidad gramatical de la respuesta"""
    puntuacion = 0
    max_puntuacion = 100
    
    # Verificar que la respuesta no esté vacía
    if not respuesta.strip():
        return 0
    
    # Verificar que comience con mayúscula
    if respuesta.strip()[0].isupper():
        puntuacion += 20
    else:
        puntuacion -= 10
    
    # Verificar que termine con punto
    if respuesta.strip().endswith('.'):
        puntuacion += 20
    else:
        puntuacion -= 10
    
    # Verificar que no tenga caracteres sueltos repetitivos
    caracteres_sueltos = re.findall(r'\s+[,\s]+\s+', respuesta)
    if not caracteres_sueltos:
        puntuacion += 20
    else:
        puntuacion -= 20
    
    # Verificar que tenga estructura de oración completa
    palabras = respuesta.split()
    if len(palabras) >= 5:  # Mínimo 5 palabras para una oración completa
        puntuacion += 20
    else:
        puntuacion -= 10
    
    # Verificar que no tenga repeticiones excesivas
    palabras_unicas = set(palabras)
    if len(palabras_unicas) / len(palabras) > 0.6:  # Al menos 60% de palabras únicas
        puntuacion += 20
    else:
        puntuacion -= 20
    
    return max(0, min(100, puntuacion))

def evaluar_consistencia(respuesta, pregunta):
    """Evaluar la consistencia entre pregunta y respuesta"""
    puntuacion = 0
    max_puntuacion = 100
    
    # Verificar que la respuesta no sea la pregunta repetida
    if respuesta.lower().strip() == pregunta.lower().strip():
        return 0
    
    # Verificar que la respuesta contenga información relevante
    palabras_pregunta = set(pregunta.lower().split())
    palabras_respuesta = set(respuesta.lower().split())
    
    # Al menos 30% de palabras de la pregunta deben estar en la respuesta
    palabras_comunes = palabras_pregunta.intersection(palabras_respuesta)
    if len(palabras_comunes) / len(palabras_pregunta) > 0.3:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    # Verificar que la respuesta no sea demasiado corta
    if len(respuesta.split()) >= 8:
        puntuacion += 50
    else:
        puntuacion -= 25
    
    return max(0, min(100, puntuacion))

def main():
    """Función principal"""
    print("🧠 TEST AVANZADO DE GRAMÁTICA Y CONSISTENCIA")
    print("=" * 60)
    
    # Cargar dataset gramatical
    dataset = cargar_dataset('../data/acuaponia_gramatical.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset gramatical cargado: {len(dataset)} líneas")
    print("📖 Características del dataset:")
    print("   - Estructura gramatical correcta")
    print("   - Respuestas completas y coherentes")
    print("   - Lenguaje claro y estructurado")
    print("   - Consistencia entre pregunta y respuesta")
    
    # Crear modelo optimizado
    print("\n🧠 Creando modelo optimizado...")
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
    
    # Pruebas avanzadas
    print("\n🧪 PRUEBAS AVANZADAS DE GRAMÁTICA Y CONSISTENCIA")
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
        
        respuesta = model.generate(prueba['pregunta'], max_length=50, temperature=0.2)
        print(f"🤖 {respuesta}")
        
        # Evaluar razonamiento
        puntuacion_razonamiento = evaluar_razonamiento(respuesta, prueba['palabras_clave'])
        total_razonamiento += puntuacion_razonamiento
        
        # Evaluar gramática
        puntuacion_gramatica = evaluar_gramatica(respuesta)
        total_gramatica += puntuacion_gramatica
        
        # Evaluar consistencia
        puntuacion_consistencia = evaluar_consistencia(respuesta, prueba['pregunta'])
        total_consistencia += puntuacion_consistencia
        
        print(f"📊 Razonamiento: {puntuacion_razonamiento:.1f}%")
        print(f"📝 Gramática: {puntuacion_gramatica:.1f}%")
        print(f"🔗 Consistencia: {puntuacion_consistencia:.1f}%")
        print(f"🎯 Esperado: {prueba['respuesta_esperada']}")
        
        # Evaluación cualitativa
        promedio_prueba = (puntuacion_razonamiento + puntuacion_gramatica + puntuacion_consistencia) / 3
        if promedio_prueba >= 75:
            print("✅ EXCELENTE: Respuesta completa y coherente")
        elif promedio_prueba >= 50:
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
    
    # Comparación con resultados anteriores
    puntuacion_anterior = 71.0
    mejora = promedio_general - puntuacion_anterior
    
    print(f"\n📈 COMPARACIÓN:")
    print(f"Puntuación anterior (solo razonamiento): {puntuacion_anterior}%")
    print(f"Puntuación actual (general): {promedio_general:.1f}%")
    print(f"Mejora: {mejora:+.1f}%")
    
    # Evaluación cualitativa
    print(f"\n🎯 EVALUACIÓN CUALITATIVA:")
    if promedio_general >= 80:
        print("🟢 EXCELENTE: El modelo muestra razonamiento, gramática y consistencia avanzados")
        print("✅ El modelo está RAZONANDO y RESPONDIENDO correctamente")
    elif promedio_general >= 60:
        print("🟡 BUENO: El modelo muestra razonamiento básico con buena estructura")
        print("✅ El modelo está RAZONANDO con estructura aceptable")
    elif promedio_general >= 40:
        print("🟠 REGULAR: El modelo muestra algo de razonamiento pero necesita mejorar estructura")
        print("⚠️  El modelo está en el límite entre razonar y autocompletar")
    else:
        print("🔴 DEFICIENTE: El modelo parece solo autocompletar sin estructura")
        print("❌ El modelo está AUTOCOMPLETANDO sin coherencia")
    
    # Guardar modelo mejorado
    print(f"\n💾 Guardando modelo mejorado...")
    model.save_model("../models/acuaponia_gramatica_consistencia.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_gramatica_consistencia.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES:")
    if mejora > 0:
        print(f"✅ El dataset gramatical ha mejorado la calidad general en {mejora:.1f}%")
        print(f"✅ Usar este modelo para aplicaciones que requieran respuestas coherentes")
        print(f"✅ El modelo puede manejar preguntas con estructura gramatical correcta")
    else:
        print(f"⚠️  El dataset necesita más mejoras para gramática y consistencia")
        print(f"💡 Considerar agregar más ejemplos de estructura gramatical")
        print(f"💡 El modelo necesita más entrenamiento en coherencia de respuestas")

if __name__ == "__main__":
    main() 