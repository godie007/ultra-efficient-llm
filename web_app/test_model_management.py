#!/usr/bin/env python3
"""
Script de prueba para las funcionalidades de gestión de modelos
"""

import requests
import time
import json
from pathlib import Path

# Configuración
BASE_URL = "http://localhost:8001/api"
TEST_MODEL_NAME = "test_model_management"

def test_health_check():
    """Prueba el health check del backend"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check exitoso")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_model_status():
    """Prueba obtener el estado del modelo"""
    print("📊 Probando estado del modelo...")
    try:
        response = requests.get(f"{BASE_URL}/model/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado del modelo: {data.get('status', 'unknown')}")
            print(f"   Entrenado: {data.get('is_trained', False)}")
            return data
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error en estado del modelo: {e}")
        return None

def test_list_models():
    """Prueba listar modelos guardados"""
    print("📁 Probando lista de modelos...")
    try:
        response = requests.get(f"{BASE_URL}/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Modelos encontrados: {len(models)}")
            for model in models:
                print(f"   - {model.get('model_name', 'N/A')} ({model.get('filename', 'N/A')})")
            return models
        else:
            print(f"❌ Error listando modelos: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error en lista de modelos: {e}")
        return []

def test_save_model():
    """Prueba guardar un modelo"""
    print("💾 Probando guardar modelo...")
    try:
        # Primero verificar que hay un modelo entrenado
        status = test_model_status()
        if not status or not status.get('is_trained'):
            print("⚠️ No hay modelo entrenado para guardar")
            return False
        
        # Intentar guardar el modelo
        data = {'model_name': TEST_MODEL_NAME}
        response = requests.post(f"{BASE_URL}/models/save", data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Modelo guardado exitosamente: {result.get('filename', 'N/A')}")
            print(f"   Tamaño: {result.get('size_bytes', 0)} bytes")
            return True
        else:
            print(f"❌ Error guardando modelo: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en guardar modelo: {e}")
        return False

def test_load_model(model_filename):
    """Prueba cargar un modelo"""
    print(f"📂 Probando cargar modelo: {model_filename}")
    try:
        data = {'model_filename': model_filename}
        response = requests.post(f"{BASE_URL}/models/load", data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Modelo cargado exitosamente")
            print(f"   Patrones: {result.get('model_info', {}).get('patterns_count', 0)}")
            return True
        else:
            print(f"❌ Error cargando modelo: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en cargar modelo: {e}")
        return False

def test_delete_model(model_filename):
    """Prueba eliminar un modelo"""
    print(f"🗑️ Probando eliminar modelo: {model_filename}")
    try:
        response = requests.delete(f"{BASE_URL}/models/{model_filename}", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Modelo eliminado exitosamente")
            return True
        else:
            print(f"❌ Error eliminando modelo: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en eliminar modelo: {e}")
        return False

def test_generate_text():
    """Prueba generar texto con el modelo"""
    print("🎨 Probando generación de texto...")
    try:
        data = {
            'prompt': 'Hola, ¿cómo estás?',
            'max_length': '10',
            'temperature': '0.7'
        }
        response = requests.post(f"{BASE_URL}/generate", data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Texto generado: {result.get('generated_text', 'N/A')}")
            return True
        else:
            print(f"❌ Error generando texto: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en generación: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de gestión de modelos...")
    print("=" * 50)
    
    # Verificar que el backend esté funcionando
    if not test_health_check():
        print("❌ Backend no está disponible. Inicia el servidor primero.")
        return
    
    print("\n📋 Estado inicial:")
    initial_status = test_model_status()
    initial_models = test_list_models()
    
    print(f"\n🔧 Pruebas de funcionalidad:")
    
    # Prueba 1: Guardar modelo (si hay uno entrenado)
    if initial_status and initial_status.get('is_trained'):
        print("\n1️⃣ Prueba de guardar modelo:")
        save_success = test_save_model()
        
        if save_success:
            # Prueba 2: Listar modelos después de guardar
            print("\n2️⃣ Verificando lista actualizada:")
            updated_models = test_list_models()
            
            # Buscar el modelo que acabamos de guardar
            test_model = None
            for model in updated_models:
                if TEST_MODEL_NAME in model.get('model_name', ''):
                    test_model = model
                    break
            
            if test_model:
                # Prueba 3: Cargar el modelo guardado
                print("\n3️⃣ Prueba de cargar modelo:")
                load_success = test_load_model(test_model['filename'])
                
                if load_success:
                    # Prueba 4: Generar texto con el modelo cargado
                    print("\n4️⃣ Prueba de generación con modelo cargado:")
                    test_generate_text()
                    
                    # Prueba 5: Eliminar el modelo de prueba
                    print("\n5️⃣ Limpiando modelo de prueba:")
                    test_delete_model(test_model['filename'])
                else:
                    print("❌ Falló la carga del modelo")
            else:
                print("❌ No se encontró el modelo guardado")
        else:
            print("❌ Falló el guardado del modelo")
    else:
        print("⚠️ No hay modelo entrenado para probar guardado")
        print("   Entrena un modelo primero usando la interfaz web")
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("\n💡 Para usar las funcionalidades:")
    print("   1. Inicia el backend: cd web_app/backend && python main.py")
    print("   2. Inicia el frontend: cd web_app/frontend && npm run dev")
    print("   3. Ve a http://localhost:5173")
    print("   4. Entrena un modelo y guárdalo")
    print("   5. Usa la página 'Modelos' para gestionar tus modelos")

if __name__ == "__main__":
    main() 