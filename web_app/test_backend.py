#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del backend
"""

import requests
import json
import os
from pathlib import Path

# Configuración
BACKEND_URL = "http://localhost:8001"
TEST_FILES = [
    "test_data.txt",
    "test_data.json", 
    "test_data.csv"
]

def test_health():
    """Probar endpoint de health check"""
    print("🏥 Probando health check...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_status():
    """Probar endpoint de estado del modelo"""
    print("\n📊 Probando estado del modelo...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/model/status")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_upload_file(filename):
    """Probar subida de archivo"""
    print(f"\n📤 Probando subida de archivo: {filename}")
    
    if not os.path.exists(filename):
        print(f"❌ Archivo no encontrado: {filename}")
        return False
    
    try:
        with open(filename, 'rb') as f:
            files = {'file': (filename, f, 'text/plain')}
            response = requests.post(f"{BACKEND_URL}/api/upload", files=files)
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_list_files():
    """Probar listado de archivos"""
    print("\n📁 Probando listado de archivos...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/files")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_train_model():
    """Probar entrenamiento del modelo"""
    print("\n🎯 Probando entrenamiento del modelo...")
    try:
        # Primero obtener la lista de archivos
        response = requests.get(f"{BACKEND_URL}/api/files")
        files_data = response.json()
        
        if not files_data.get('files'):
            print("❌ No hay archivos para entrenar")
            return False
        
        # Tomar los primeros 2 archivos
        file_names = [f['filename'] for f in files_data['files'][:2]]
        print(f"📝 Archivos para entrenar: {file_names}")
        
        # Preparar datos para entrenamiento
        data = {
            'files': file_names,
            'max_patterns': '5000',
            'max_pattern_length': '6',
            'min_frequency': '1'
        }
        
        response = requests.post(f"{BACKEND_URL}/api/train", data=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_generate_text():
    """Probar generación de texto"""
    print("\n🎨 Probando generación de texto...")
    try:
        data = {
            'prompt': '¿Qué es la inteligencia artificial?',
            'max_length': '30',
            'temperature': '0.8'
        }
        
        response = requests.post(f"{BACKEND_URL}/api/generate", data=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🧪 Iniciando pruebas del backend...")
    print("=" * 50)
    
    # Verificar que el backend esté ejecutándose
    if not test_health():
        print("❌ Backend no está ejecutándose. Inicia el servidor primero.")
        return
    
    # Probar estado del modelo
    test_model_status()
    
    # Probar subida de archivos
    for filename in TEST_FILES:
        test_upload_file(filename)
    
    # Probar listado de archivos
    test_list_files()
    
    # Probar entrenamiento
    test_train_model()
    
    # Probar generación
    test_generate_text()
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    main() 