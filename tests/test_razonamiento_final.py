#!/usr/bin/env python3
"""
🧠 TEST FINAL DE RAZONAMIENTO - ULTRAEFFICIENTLLM
=================================================

Prueba final del razonamiento con dataset estructurado optimizado.
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
    print("🧠 TEST FINAL DE RAZONAMIENTO - ULTRAEFFICIENTLLM")
    print("=" * 60)
    
    # Cargar dataset estructurado
    dataset = cargar_dataset('data/acuaponia_estructurado.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset estructurado cargado: {len(dataset)} líneas")
    print("📖 Características del dataset:")
    print("   - Conceptos fundamentales detallados")
    print("   - Razonamiento causal específico")
    print("   - Razonamiento inferencial con diagnósticos")
    print("   - Procesos secuenciales paso a paso")
    print("   - Comparaciones específicas")
    print("   - Soluciones de problemas concretas")
    
    # Crear modelo optimizado
    print("\n🧠 Creando modelo optimizado...")
    model = UltraEfficientLLM(
        max_pattern_length=8,  # Patrones más largos para contexto
        min_frequency=1,
        max_patterns=15000     # Más patrones para cobertura completa
    )
    
    print("🔄 Entrenando modelo...")
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Pruebas finales de razonamiento
    print("\n🧪 PRUEBAS FINALES DE RAZONAMIENTO")
    print("=" * 60)
    
    pruebas = [
        {
            "categoria": "RAZONAMIENTO CAUSAL",
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "palabras_clave": ["nutrientes", "desechos", "peces", "oxigenada", "malezas"],
            "respuesta_esperada": "Las plantas crecen bien porque reciben nutrientes naturales de los desechos de los peces, el agua está constantemente oxigenada, y no hay competencia de malezas"
        },
        {
            "categoria": "RAZONAMIENTO INFERENCIAL",
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "palabras_clave": ["nutrientes", "pH", "peces", "hierro", "sistema"],
            "respuesta_esperada": "Si las plantas están amarillas, puede ser falta de nutrientes, pH incorrecto del agua, demasiados peces para el sistema, o falta de hierro en el agua"
        },
        {
            "categoria": "RAZONAMIENTO SECUENCIAL",
            "pregunta": "¿Cómo funciona el ciclo del agua en acuaponía?",
            "palabras_clave": ["peces", "desechos", "amonio", "bacterias", "nitratos", "plantas", "absorben", "limpia"],
            "respuesta_esperada": "El ciclo funciona así: los peces producen desechos con amonio, las bacterias convierten amonio en nitratos, las plantas absorben nitratos y limpian el agua, el agua oxigenada regresa a los peces"
        },
        {
            "categoria": "RAZONAMIENTO COMPARATIVO",
            "pregunta": "¿Cuál es la diferencia entre acuaponía y agricultura tradicional?",
            "palabras_clave": ["agua", "menos", "fertilizantes", "químicos", "productiva", "metro"],
            "respuesta_esperada": "La acuaponía usa 90% menos agua, no necesita fertilizantes químicos, produce tanto peces como plantas, y es más productiva por metro cuadrado"
        },
        {
            "categoria": "SOLUCIÓN DE PROBLEMAS",
            "pregunta": "¿Qué hago si las plantas están débiles?",
            "palabras_clave": ["nutrientes", "pH", "iluminación", "hierro", "verifica"],
            "respuesta_esperada": "Si las plantas están débiles, verifica los nutrientes en el agua, ajusta el pH a 6.0-7.0, revisa la iluminación, y considera añadir hierro si es necesario"
        }
    ]
    
    total_puntuacion = 0
    total_pruebas = len(pruebas)
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\n{i}. {prueba['categoria']}")
        print(f"❓ {prueba['pregunta']}")
        
        respuesta = model.generate(prueba['pregunta'], max_length=60, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        puntuacion = evaluar_razonamiento(respuesta, prueba['palabras_clave'])
        total_puntuacion += puntuacion
        
        print(f"📊 Puntuación: {puntuacion:.1f}%")
        print(f"🎯 Esperado: {prueba['respuesta_esperada']}")
        
        # Evaluación cualitativa
        if puntuacion >= 80:
            print("✅ EXCELENTE: Razonamiento avanzado")
        elif puntuacion >= 60:
            print("🟡 BUENO: Razonamiento claro")
        elif puntuacion >= 40:
            print("🟠 REGULAR: Algún razonamiento")
        else:
            print("❌ DEFICIENTE: Poco razonamiento")
    
    # Resultado final
    puntuacion_final = total_puntuacion / total_pruebas
    
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    print(f"Puntuación promedio: {puntuacion_final:.1f}%")
    
    # Comparación con resultados anteriores
    puntuacion_original = 51.7
    puntuacion_mejorada = 45.0
    mejora_vs_original = puntuacion_final - puntuacion_original
    mejora_vs_mejorada = puntuacion_final - puntuacion_mejorada
    
    print(f"Puntuación original: {puntuacion_original}%")
    print(f"Puntuación mejorada: {puntuacion_mejorada}%")
    print(f"Puntuación final: {puntuacion_final:.1f}%")
    print(f"Mejora vs original: {mejora_vs_original:+.1f}%")
    print(f"Mejora vs mejorada: {mejora_vs_mejorada:+.1f}%")
    
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
    
    # Guardar modelo final
    print(f"\n💾 Guardando modelo final...")
    model.save_model("models/acuaponia_razonamiento_final.pkl")
    print(f"✅ Modelo guardado como 'acuaponia_razonamiento_final.pkl'")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES FINALES:")
    if puntuacion_final >= 60:
        print(f"✅ El dataset estructurado ha mejorado significativamente el razonamiento")
        print(f"✅ Usar este modelo para aplicaciones que requieran razonamiento semántico")
        print(f"✅ El modelo puede manejar preguntas complejas y diagnósticos")
    elif puntuacion_final >= 40:
        print(f"🟡 El dataset estructurado muestra mejoras moderadas")
        print(f"💡 Considerar agregar más ejemplos específicos de razonamiento")
        print(f"💡 El modelo necesita más entrenamiento en inferencias complejas")
    else:
        print(f"⚠️  El dataset estructurado no ha mejorado significativamente")
        print(f"💡 Revisar la estructura del dataset y agregar más contexto")
        print(f"💡 Considerar diferentes enfoques de entrenamiento")

if __name__ == "__main__":
    main() 