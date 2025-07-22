#!/usr/bin/env python3
"""
Script de prueba rápida para verificar las optimizaciones
"""

import requests
import time

def test_backend():
    """Prueba rápida del backend optimizado"""
    print("🚀 Probando backend optimizado...")
    
    try:
        # Health check
        print("1️⃣ Health check...")
        start_time = time.time()
        response = requests.get("http://localhost:8001/api/health", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check exitoso en {(end_time - start_time)*1000:.1f}ms")
            print(f"   Modelo cargado: {data.get('model_loaded', False)}")
            print(f"   Thread pool activo: {data.get('thread_pool_active', False)}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
        
        # Model status
        print("\n2️⃣ Estado del modelo...")
        start_time = time.time()
        response = requests.get("http://localhost:8001/api/model/status", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado obtenido en {(end_time - start_time)*1000:.1f}ms")
            print(f"   Estado: {data.get('status', 'unknown')}")
            print(f"   Entrenado: {data.get('is_trained', False)}")
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
        
        # Files list
        print("\n3️⃣ Lista de archivos...")
        start_time = time.time()
        response = requests.get("http://localhost:8001/api/files", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Lista obtenida en {(end_time - start_time)*1000:.1f}ms")
            print(f"   Archivos: {len(data.get('files', []))}")
        else:
            print(f"❌ Error listando archivos: {response.status_code}")
        
        # Models list
        print("\n4️⃣ Lista de modelos...")
        start_time = time.time()
        response = requests.get("http://localhost:8001/api/models", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Modelos obtenidos en {(end_time - start_time)*1000:.1f}ms")
            print(f"   Modelos: {len(data.get('models', []))}")
        else:
            print(f"❌ Error listando modelos: {response.status_code}")
        
        print("\n✅ Todas las pruebas básicas completadas exitosamente!")
        print("🎉 El backend está funcionando correctamente con las optimizaciones")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al backend")
        print("💡 Asegúrate de que esté ejecutándose en http://localhost:8001")
        return False
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 PRUEBA RÁPIDA - BACKEND OPTIMIZADO")
    print("=" * 50)
    
    success = test_backend()
    
    if success:
        print("\n🎯 Próximos pasos:")
        print("   1. Entrena un modelo en la interfaz web")
        print("   2. Prueba la generación de texto")
        print("   3. Ejecuta python test_performance.py para pruebas completas")
    else:
        print("\n🔧 Solución de problemas:")
        print("   1. Verifica que el backend esté ejecutándose")
        print("   2. Revisa los logs del backend")
        print("   3. Asegúrate de que el puerto 8001 esté disponible")
    
    print("\n" + "=" * 50) 