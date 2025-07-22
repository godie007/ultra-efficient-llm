#!/usr/bin/env python3
"""
🧠 TEST DE RAZONAMIENTO ÓPTIMO - ULTRAEFFICIENTLLM
==================================================

Test final con configuración optimizada para máximo razonamiento.
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
    print("🧠 TEST DE RAZONAMIENTO ÓPTIMO - ULTRAEFFICIENTLLM")
    print("=" * 60)
    
    # Cargar dataset simple
    dataset = cargar_dataset('data/acuaponia_simple_razonamiento.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset simple cargado: {len(dataset)} líneas")
    print("📖 Características del dataset optimizado:")
    print("   - Conceptos básicos claros")
    print("   - Razonamiento causal directo")
    print("   - Inferencias simples")
    print("   - Comparaciones básicas")
    print("   - Procesos secuenciales")
    print("   - Soluciones de problemas")
    
    # Crear modelo con configuración óptima
    print("\n🧠 Creando modelo con configuración óptima...")
    model = UltraEfficientLLM(
        max_pattern_length=6,  # Patrones moderados para evitar confusión
        min_frequency=1,
        max_patterns=8000      # Patrones suficientes sin sobrecarga
    )
    
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Pruebas de razonamiento optimizadas
    print("\n🧪 PRUEBAS DE RAZONAMIENTO ÓPTIMO")
    print("=" * 60)
    
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
            "palabras_clave": ["nutrientes", "peces", "falta", "demasiados"],
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
        
        respuesta = model.generate(prueba['pregunta'], max_length=40, temperature=0.2)
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
    
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    print(f"Puntuación promedio: {puntuacion_final:.1f}%")
    
    # Comparación con todos los resultados anteriores
    puntuacion_original = 51.7
    puntuacion_mejorada = 45.0
    puntuacion_estructurado = 10.7
    mejora_vs_original = puntuacion_final - puntuacion_original
    mejora_vs_mejorada = puntuacion_final - puntuacion_mejorada
    mejora_vs_estructurado = puntuacion_final - puntuacion_estructurado
    
    print(f"Puntuación original: {puntuacion_original}%")
    print(f"Puntuación mejorada: {puntuacion_mejorada}%")
    print(f"Puntuación estructurado: {puntuacion_estructurado}%")
    print(f"Puntuación óptima: {puntuacion_final:.1f}%")
    print(f"Mejora vs original: {mejora_vs_original:+.1f}%")
    print(f"Mejora vs mejorada: {mejora_vs_mejorada:+.1f}%")
    print(f"Mejora vs estructurado: {mejora_vs_estructurado:+.1f}%")
    
    # Evaluación cualitativa
    print(f"\n🎯 EVALUACIÓN CUALITATIVA:")
    if puntuacion_final >= 80:
        print("🟢 EXCELENTE: El modelo muestra razonamiento semántico avanzado")
        print("✅ El modelo está RAZONANDO correctamente")
    elif puntuacion_final >= 60:
        print("🟡 BUENO: El modelo muestra razonamiento básico")
        print("✅ El modelo está RAZONANDO")
    elif puntuacion_final >= 40:
        print("🟠 REGULAR: El modelo muestra algo de razonamiento")
        print("⚠️  El modelo está en el límite entre razonar y autocompletar")
    else:
        print("🔴 DEFICIENTE: El modelo parece solo autocompletar")
        print("❌ El modelo está AUTOCOMPLETANDO")
    
    # Guardar modelo óptimo
    print(f"\n💾 Guardando modelo óptimo...")
    model.save_model("models/acuaponia_razonamiento_optimo.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_razonamiento_optimo.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES:")
    if puntuacion_final >= 60:
        print(f"✅ La configuración óptima ha mejorado significativamente el razonamiento")
        print(f"✅ Usar esta configuración para aplicaciones que requieran razonamiento")
        print(f"✅ El modelo puede manejar preguntas de razonamiento básico")
    elif puntuacion_final >= 40:
        print(f"🟡 La configuración óptima muestra mejoras moderadas")
        print(f"💡 El modelo necesita más refinamiento para razonamiento complejo")
        print(f"💡 Considerar ajustes adicionales en los parámetros")
    else:
        print(f"⚠️  La configuración óptima no ha mejorado significativamente")
        print(f"💡 El modelo puede necesitar un enfoque diferente")
        print(f"💡 Considerar arquitecturas alternativas para razonamiento")

if __name__ == "__main__":
    main() 