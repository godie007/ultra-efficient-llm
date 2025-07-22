#!/usr/bin/env python3
"""
🧠 PRUEBAS DE RAZONAMIENTO SEMÁNTICO - ULTRAEFFICIENTLLM
========================================================

Este script evalúa si el modelo está realmente razonando o solo autocompletando.
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

def evaluar_razonamiento(respuesta, pregunta, criterios):
    """Evaluar si la respuesta muestra razonamiento"""
    puntuacion = 0
    max_puntuacion = len(criterios)
    
    for criterio, palabras_clave in criterios.items():
        if any(palabra.lower() in respuesta.lower() for palabra in palabras_clave):
            puntuacion += 1
    
    return puntuacion, max_puntuacion, (puntuacion / max_puntuacion) * 100

def test_razonamiento_causal():
    """Prueba de razonamiento causal (causa-efecto)"""
    print("\n🔗 PRUEBA 1: RAZONAMIENTO CAUSAL")
    print("=" * 50)
    
    preguntas_causales = [
        {
            "pregunta": "¿Por qué las plantas crecen bien en acuaponía?",
            "criterios": {
                "nutrientes": ["nutrientes", "desechos", "alimento"],
                "agua": ["agua", "limpia", "oxigenada"],
                "sistema": ["sistema", "cerrado", "equilibrio"]
            }
        },
        {
            "pregunta": "¿Qué pasa si no hay peces en el sistema?",
            "criterios": {
                "nutrientes": ["nutrientes", "desechos", "alimento"],
                "plantas": ["plantas", "crecer", "morir"],
                "sistema": ["sistema", "funcionar", "equilibrio"]
            }
        },
        {
            "pregunta": "¿Por qué la acuaponía usa menos agua?",
            "criterios": {
                "reciclaje": ["recicla", "reutiliza", "ciclo"],
                "cerrado": ["cerrado", "sistema", "evaporación"],
                "eficiencia": ["eficiente", "menos", "ahorro"]
            }
        }
    ]
    
    total_puntuacion = 0
    total_max = 0
    
    for test in preguntas_causales:
        print(f"\n❓ {test['pregunta']}")
        respuesta = model.generate(test['pregunta'], max_length=40, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        puntuacion, max_punt, porcentaje = evaluar_razonamiento(
            respuesta, test['pregunta'], test['criterios']
        )
        
        print(f"📊 Puntuación: {puntuacion}/{max_punt} ({porcentaje:.1f}%)")
        total_puntuacion += puntuacion
        total_max += max_punt
    
    return total_puntuacion, total_max

def test_razonamiento_comparativo():
    """Prueba de razonamiento comparativo"""
    print("\n⚖️ PRUEBA 2: RAZONAMIENTO COMPARATIVO")
    print("=" * 50)
    
    preguntas_comparativas = [
        {
            "pregunta": "¿Cuál es la diferencia entre acuaponía y agricultura tradicional?",
            "criterios": {
                "agua": ["agua", "menos", "más"],
                "fertilizantes": ["fertilizantes", "químicos", "natural"],
                "sistema": ["sistema", "cerrado", "abierto"]
            }
        },
        {
            "pregunta": "¿Por qué la acuaponía es mejor que la hidroponía?",
            "criterios": {
                "nutrientes": ["nutrientes", "naturales", "orgánicos"],
                "peces": ["peces", "proteína", "alimento"],
                "sistema": ["sistema", "completo", "integrado"]
            }
        }
    ]
    
    total_puntuacion = 0
    total_max = 0
    
    for test in preguntas_comparativas:
        print(f"\n❓ {test['pregunta']}")
        respuesta = model.generate(test['pregunta'], max_length=50, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        puntuacion, max_punt, porcentaje = evaluar_razonamiento(
            respuesta, test['pregunta'], test['criterios']
        )
        
        print(f"📊 Puntuación: {puntuacion}/{max_punt} ({porcentaje:.1f}%)")
        total_puntuacion += puntuacion
        total_max += max_punt
    
    return total_puntuacion, total_max

def test_razonamiento_inferencial():
    """Prueba de razonamiento inferencial (conclusiones)"""
    print("\n🧩 PRUEBA 3: RAZONAMIENTO INFERENCIAL")
    print("=" * 50)
    
    preguntas_inferenciales = [
        {
            "pregunta": "Si las plantas están amarillas, ¿qué puede estar pasando?",
            "criterios": {
                "nutrientes": ["nutrientes", "deficiencia", "falta"],
                "peces": ["peces", "desechos", "alimento"],
                "diagnostico": ["problema", "síntoma", "causa"]
            }
        },
        {
            "pregunta": "¿Qué necesito para empezar un sistema de acuaponía?",
            "criterios": {
                "componentes": ["tanque", "peces", "plantas"],
                "agua": ["agua", "bomba", "filtro"],
                "conocimiento": ["conocimiento", "aprendizaje", "planificación"]
            }
        }
    ]
    
    total_puntuacion = 0
    total_max = 0
    
    for test in preguntas_inferenciales:
        print(f"\n❓ {test['pregunta']}")
        respuesta = model.generate(test['pregunta'], max_length=45, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        puntuacion, max_punt, porcentaje = evaluar_razonamiento(
            respuesta, test['pregunta'], test['criterios']
        )
        
        print(f"📊 Puntuación: {puntuacion}/{max_punt} ({porcentaje:.1f}%)")
        total_puntuacion += puntuacion
        total_max += max_punt
    
    return total_puntuacion, total_max

def test_razonamiento_secuencial():
    """Prueba de razonamiento secuencial (pasos)"""
    print("\n📋 PRUEBA 4: RAZONAMIENTO SECUENCIAL")
    print("=" * 50)
    
    preguntas_secuenciales = [
        {
            "pregunta": "¿Cuáles son los pasos para mantener un sistema de acuaponía?",
            "criterios": {
                "monitoreo": ["monitoreo", "revisar", "controlar"],
                "alimentacion": ["alimentar", "peces", "comida"],
                "mantenimiento": ["limpiar", "mantener", "cuidar"]
            }
        },
        {
            "pregunta": "¿Cómo funciona el ciclo del agua en acuaponía?",
            "criterios": {
                "peces": ["peces", "desechos", "producen"],
                "plantas": ["plantas", "absorben", "nutrientes"],
                "agua": ["agua", "limpia", "vuelve"]
            }
        }
    ]
    
    total_puntuacion = 0
    total_max = 0
    
    for test in preguntas_secuenciales:
        print(f"\n❓ {test['pregunta']}")
        respuesta = model.generate(test['pregunta'], max_length=50, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        puntuacion, max_punt, porcentaje = evaluar_razonamiento(
            respuesta, test['pregunta'], test['criterios']
        )
        
        print(f"📊 Puntuación: {puntuacion}/{max_punt} ({porcentaje:.1f}%)")
        total_puntuacion += puntuacion
        total_max += max_punt
    
    return total_puntuacion, total_max

def test_contradicciones():
    """Prueba para detectar contradicciones"""
    print("\n🚫 PRUEBA 5: DETECCIÓN DE CONTRADICCIONES")
    print("=" * 50)
    
    preguntas_contradictorias = [
        {
            "pregunta": "¿La acuaponía usa mucha agua o poca agua?",
            "criterios": {
                "poca_agua": ["poca", "menos", "eficiente"],
                "contradiccion": ["mucha", "gasta", "desperdicia"]
            },
            "esperado": "poca_agua"
        },
        {
            "pregunta": "¿Los peces necesitan fertilizantes químicos?",
            "criterios": {
                "no_quimicos": ["no", "natural", "orgánico"],
                "contradiccion": ["sí", "químicos", "artificial"]
            },
            "esperado": "no_quimicos"
        }
    ]
    
    total_correctas = 0
    total_preguntas = len(preguntas_contradictorias)
    
    for test in preguntas_contradictorias:
        print(f"\n❓ {test['pregunta']}")
        respuesta = model.generate(test['pregunta'], max_length=30, temperature=0.3)
        print(f"🤖 {respuesta}")
        
        # Verificar si la respuesta es coherente
        respuesta_coherente = False
        for criterio, palabras in test['criterios'].items():
            if criterio == test['esperado']:
                if any(palabra.lower() in respuesta.lower() for palabra in palabras):
                    respuesta_coherente = True
                    break
        
        if respuesta_coherente:
            print("✅ Respuesta coherente")
            total_correctas += 1
        else:
            print("❌ Posible contradicción detectada")
    
    return total_correctas, total_preguntas

def main():
    """Función principal"""
    print("🧠 PRUEBAS DE RAZONAMIENTO SEMÁNTICO - ULTRAEFFICIENTLLM")
    print("=" * 70)
    
    # Cargar y entrenar modelo
    dataset = cargar_dataset('data/acuaponia_minimal.txt')
    if not dataset:
        return
    
    print(f"📚 Dataset cargado: {len(dataset)} líneas")
    
    global model
    print("🧠 Creando y entrenando modelo...")
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=6000
    )
    
    start_time = time.time()
    model.train(dataset)
    training_time = time.time() - start_time
    
    print(f"✅ Modelo entrenado en {training_time:.2f} segundos")
    
    # Ejecutar pruebas
    resultados = {}
    
    # Prueba 1: Razonamiento causal
    punt_causal, max_causal = test_razonamiento_causal()
    resultados['causal'] = (punt_causal, max_causal, (punt_causal/max_causal)*100)
    
    # Prueba 2: Razonamiento comparativo
    punt_comp, max_comp = test_razonamiento_comparativo()
    resultados['comparativo'] = (punt_comp, max_comp, (punt_comp/max_comp)*100)
    
    # Prueba 3: Razonamiento inferencial
    punt_inf, max_inf = test_razonamiento_inferencial()
    resultados['inferencial'] = (punt_inf, max_inf, (punt_inf/max_inf)*100)
    
    # Prueba 4: Razonamiento secuencial
    punt_sec, max_sec = test_razonamiento_secuencial()
    resultados['secuencial'] = (punt_sec, max_sec, (punt_sec/max_sec)*100)
    
    # Prueba 5: Detección de contradicciones
    correctas, total = test_contradicciones()
    resultados['coherencia'] = (correctas, total, (correctas/total)*100)
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS DE RAZONAMIENTO")
    print("="*70)
    
    total_puntuacion = 0
    total_max = 0
    
    for tipo, (punt, max_punt, porcentaje) in resultados.items():
        print(f"{tipo.upper():12}: {punt:2}/{max_punt:2} ({porcentaje:5.1f}%)")
        total_puntuacion += punt
        total_max += max_punt
    
    puntuacion_final = (total_puntuacion / total_max) * 100
    
    print("-" * 70)
    print(f"PUNTUACIÓN FINAL: {total_puntuacion}/{total_max} ({puntuacion_final:.1f}%)")
    
    # Evaluación cualitativa
    print("\n🎯 EVALUACIÓN CUALITATIVA:")
    if puntuacion_final >= 80:
        print("🟢 EXCELENTE: El modelo muestra razonamiento semántico avanzado")
    elif puntuacion_final >= 60:
        print("🟡 BUENO: El modelo muestra razonamiento básico")
    elif puntuacion_final >= 40:
        print("🟠 REGULAR: El modelo muestra algo de razonamiento")
    else:
        print("🔴 DEFICIENTE: El modelo parece solo autocompletar")
    
    print(f"\n💡 CONCLUSIÓN: El modelo está {'RAZONANDO' if puntuacion_final >= 60 else 'AUTOCOMPLETANDO'}")

if __name__ == "__main__":
    main() 