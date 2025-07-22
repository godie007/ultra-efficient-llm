#!/usr/bin/env python3
"""
Test de la API web del UltraEfficientLLM
"""

import requests
import json
import time
import sys
import os

# Configuración
API_BASE_URL = "http://localhost:8001/api"
TEST_TIMEOUT = 30

def test_health_check():
    """Test del endpoint de health check"""
    print("🏥 TESTING HEALTH CHECK...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Health check exitoso")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_model_status():
    """Test del endpoint de estado del modelo"""
    print("📊 TESTING MODEL STATUS...")
    try:
        response = requests.get(f"{API_BASE_URL}/model/status", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado del modelo: {data}")
            return True
        else:
            print(f"❌ Model status falló: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en model status: {e}")
        return False

def test_list_models():
    """Test del endpoint de listar modelos"""
    print("📋 TESTING LIST MODELS...")
    try:
        response = requests.get(f"{API_BASE_URL}/models", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Modelos disponibles: {data}")
            return True
        else:
            print(f"❌ List models falló: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en list models: {e}")
        return False

def test_train_model():
    """Test del endpoint de entrenamiento"""
    print("🔄 TESTING MODEL TRAINING...")
    
    # Datos de prueba
    training_data = [
        "La acuaponía combina peces y plantas.",
        "Los peces producen desechos que las plantas usan como nutrientes.",
        "Las plantas limpian el agua para los peces.",
        "Es un sistema cerrado y eficiente."
    ]
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/train",
            json={"texts": training_data},
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Entrenamiento exitoso: {data}")
            return True
        else:
            print(f"❌ Training falló: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en training: {e}")
        return False

def test_generate_text():
    """Test del endpoint de generación de texto"""
    print("✨ TESTING TEXT GENERATION...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate",
            json={
                "prompt": "¿Qué es la acuaponía?",
                "max_length": 20,
                "temperature": 0.3
            },
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generación exitosa: {data}")
            return True
        else:
            print(f"❌ Generation falló: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en generation: {e}")
        return False

def test_save_model():
    """Test del endpoint de guardar modelo"""
    print("💾 TESTING MODEL SAVE...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/models/save",
            json={"filename": "test_model.pkl"},
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Guardado exitoso: {data}")
            return True
        else:
            print(f"❌ Save falló: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en save: {e}")
        return False

def test_load_model():
    """Test del endpoint de cargar modelo"""
    print("📂 TESTING MODEL LOAD...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/models/load",
            json={"filename": "test_model.pkl"},
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Carga exitosa: {data}")
            return True
        else:
            print(f"❌ Load falló: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en load: {e}")
        return False

def run_all_tests():
    """Ejecuta todos los tests de la API"""
    print("🧪 TESTING WEB API - ULTRAEFFICIENTLLM")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Model Status", test_model_status),
        ("List Models", test_list_models),
        ("Train Model", test_train_model),
        ("Generate Text", test_generate_text),
        ("Save Model", test_save_model),
        ("Load Model", test_load_model)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        print("-" * 30)
        
        if test_func():
            passed += 1
        else:
            print(f"⚠️  {test_name} falló")
    
    print(f"\n📊 RESULTADOS FINALES:")
    print(f"   Tests pasados: {passed}/{total}")
    print(f"   Tasa de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON! La API funciona correctamente")
    elif passed >= total * 0.7:
        print("👍 LA MAYORÍA DE TESTS PASARON: La API funciona bien")
    else:
        print("❌ MUCHOS TESTS FALLARON: La API necesita mejoras")

if __name__ == "__main__":
    run_all_tests() 