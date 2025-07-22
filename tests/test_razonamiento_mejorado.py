#!/usr/bin/env python3
"""
🧠 TEST DE RAZONAMIENTO MEJORADO - ULTRAEFFICIENTLLM
====================================================

Prueba el razonamiento con el dataset mejorado de acuaponía.
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

def evaluar_razonamiento(respuesta, palabras_clave):
    """Evaluar si la respuesta muestra razonamiento"""
    puntuacion = 0
    for palabra in palabras_clave:
        if palabra.lower() in respuesta.lower():
            puntuacion += 1
    return (puntuacion / len(palabras_clave)) * 100

def main():
    """Función principal"""
    print("🧠 TEST DE RAZONAMIENTO MEJORADO")
    print("=" * 50)
    
    # Cargar dataset mejorado
    dataset = cargar_dataset('data/acuaponia_razonamiento.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset cargado: {len(dataset)} líneas")
    print("📖 Primeras 5 líneas del dataset mejorado:")
    for i, linea in enumerate(dataset[:5]):
        print(f"   {i+1}. {linea}")
    
    # Crear y entrenar modelo optimizado
    print("\n🧠 Creando modelo optimizado...")
    model = UltraEfficientLLM(
        max_pattern_length=8,  # Patrones más largos para mejor contexto
        min_frequency=1,
        max_patterns=12000     # Más patrones para mejor cobertura
    )
    
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Pruebas de razonamiento mejoradas
    print("\n🧪 PRUEBAS DE RAZONAMIENTO MEJORADO")
    print("=" * 50)
    
    pruebas = [
        {
            "categoria": "RAZONAMIENTO CAUSAL",
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "palabras_clave": ["nutrientes", "desechos", "peces", "naturales"],
            "respuesta_esperada": "Porque reciben nutrientes naturales de los desechos de los peces"
        },
        {
            "categoria": "RAZONAMIENTO CAUSAL",
            "pregunta": "¿Qué pasa si no hay peces en el sistema?",
            "palabras_clave": ["nutrientes", "plantas", "morir", "sistema"],
            "respuesta_esperada": "Las plantas no reciben nutrientes y pueden morir"
        },
        {
            "categoria": "RAZONAMIENTO INFERENCIAL",
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "palabras_clave": ["nutrientes", "deficiencia", "problema", "causa"],
            "respuesta_esperada": "Puede ser falta de nutrientes o demasiados peces"
        },
        {
            "categoria": "RAZONAMIENTO COMPARATIVO",
            "pregunta": "¿Cuál es la diferencia entre acuaponía y agricultura tradicional?",
            "palabras_clave": ["agua", "menos", "fertilizantes", "químicos"],
            "respuesta_esperada": "La acuaponía usa menos agua y no necesita fertilizantes químicos"
        },
        {
            "categoria": "RAZONAMIENTO SECUENCIAL",
            "pregunta": "¿Cómo funciona el ciclo del agua en acuaponía?",
            "palabras_clave": ["peces", "desechos", "plantas", "absorben", "limpia"],
            "respuesta_esperada": "Los peces producen desechos, las plantas absorben nutrientes, el agua se limpia y vuelve a los peces"
        }
    ]
    
    total_puntuacion = 0
    total_pruebas = len(pruebas)
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\n{i}. {prueba['categoria']}")
        print(f"❓ {prueba['pregunta']}")
        
        respuesta = model.generate(prueba['pregunta'], max_length=50, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        puntuacion = evaluar_razonamiento(respuesta, prueba['palabras_clave'])
        total_puntuacion += puntuacion
        
        print(f"📊 Puntuación: {puntuacion:.1f}%")
        print(f"🎯 Esperado: {prueba['respuesta_esperada']}")
        
        # Evaluación cualitativa
        if puntuacion >= 75:
            print("✅ EXCELENTE: Razonamiento claro")
        elif puntuacion >= 50:
            print("🟡 BUENO: Algún razonamiento")
        else:
            print("❌ DEFICIENTE: Poco razonamiento")
    
    # Resultado final
    puntuacion_final = total_puntuacion / total_pruebas
    
    print("\n" + "="*50)
    print("📊 RESULTADO FINAL")
    print("="*50)
    print(f"Puntuación promedio: {puntuacion_final:.1f}%")
    
    # Comparación con resultado anterior
    puntuacion_anterior = 51.7
    mejora = puntuacion_final - puntuacion_anterior
    
    print(f"Puntuación anterior: {puntuacion_anterior}%")
    print(f"Mejora: {mejora:+.1f}%")
    
    # Evaluación cualitativa
    print(f"\n🎯 EVALUACIÓN CUALITATIVA:")
    if puntuacion_final >= 80:
        print("🟢 EXCELENTE: El modelo muestra razonamiento semántico avanzado")
    elif puntuacion_final >= 60:
        print("🟡 BUENO: El modelo muestra razonamiento básico")
    elif puntuacion_final >= 40:
        print("🟠 REGULAR: El modelo muestra algo de razonamiento")
    else:
        print("🔴 DEFICIENTE: El modelo parece solo autocompletar")
    
    # Guardar modelo mejorado
    print(f"\n💾 Guardando modelo mejorado...")
    model.save_model("models/acuaponia_razonamiento_mejorado.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_razonamiento_mejorado.pkl'")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    if mejora > 0:
        print(f"✅ El dataset mejorado ha mejorado el razonamiento en {mejora:.1f}%")
        print(f"✅ Usar este modelo para aplicaciones que requieran razonamiento")
    else:
        print(f"⚠️  El dataset necesita más mejoras")
        print(f"💡 Considerar agregar más ejemplos de razonamiento causal")

if __name__ == "__main__":
    main() 