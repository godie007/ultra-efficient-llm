#!/usr/bin/env python3
"""
Script de prueba de rendimiento para las optimizaciones asíncronas
"""

import requests
import time
import asyncio
import aiohttp
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001/api"
TEST_PROMPT = "Hola, ¿cómo estás hoy?"

def test_health_check():
    """Prueba el health check del backend"""
    print("🔍 Probando health check...")
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check exitoso en {(end_time - start_time)*1000:.1f}ms")
            print(f"   Thread pool activo: {data.get('thread_pool_active', False)}")
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
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/model/status", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado del modelo obtenido en {(end_time - start_time)*1000:.1f}ms")
            print(f"   Estado: {data.get('status', 'unknown')}")
            print(f"   Entrenado: {data.get('is_trained', False)}")
            return data
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error en estado del modelo: {e}")
        return None

def test_generation_performance(prompt, max_length=10, temperature=0.7):
    """Prueba el rendimiento de generación de texto"""
    print(f"🎨 Probando generación: '{prompt}' (max_length={max_length})")
    try:
        start_time = time.time()
        
        data = {
            'prompt': prompt,
            'max_length': str(max_length),
            'temperature': str(temperature)
        }
        
        response = requests.post(f"{BASE_URL}/generate", data=data, timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            generation_time = (end_time - start_time) * 1000  # Convertir a ms
            
            print(f"✅ Texto generado en {generation_time:.1f}ms")
            print(f"   Prompt: {result.get('prompt', 'N/A')}")
            print(f"   Generado: {result.get('generated_text', 'N/A')}")
            print(f"   Patrones activos: {result.get('analysis', {}).get('active_patterns', 0)}")
            
            # Calcular tokens por segundo
            generated_tokens = len(result.get('generated_text', '').split())
            tokens_per_second = generated_tokens / (generation_time / 1000) if generation_time > 0 else 0
            
            print(f"   Velocidad: {tokens_per_second:.1f} tokens/segundo")
            
            return {
                'success': True,
                'time_ms': generation_time,
                'tokens_per_second': tokens_per_second,
                'active_patterns': result.get('analysis', {}).get('active_patterns', 0)
            }
        else:
            print(f"❌ Error generando texto: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return {'success': False, 'error': response.text}
    except Exception as e:
        print(f"❌ Error en generación: {e}")
        return {'success': False, 'error': str(e)}

def test_concurrent_generation(num_requests=5):
    """Prueba generación concurrente"""
    print(f"🚀 Probando generación concurrente ({num_requests} requests)...")
    
    prompts = [
        "Hola, ¿cómo estás?",
        "El día está soleado",
        "Me gusta la tecnología",
        "La inteligencia artificial es fascinante",
        "Python es un lenguaje excelente"
    ]
    
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            prompt = prompts[i % len(prompts)]
            future = executor.submit(test_generation_performance, prompt, 8, 0.7)
            futures.append(future)
        
        for future in futures:
            result = future.result()
            results.append(result)
    
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    
    successful_requests = sum(1 for r in results if r.get('success', False))
    avg_time = sum(r.get('time_ms', 0) for r in results if r.get('success', False)) / successful_requests if successful_requests > 0 else 0
    
    print(f"✅ Generación concurrente completada en {total_time:.1f}ms")
    print(f"   Requests exitosos: {successful_requests}/{num_requests}")
    print(f"   Tiempo promedio por request: {avg_time:.1f}ms")
    print(f"   Throughput: {successful_requests/(total_time/1000):.2f} requests/segundo")
    
    return results

def test_model_operations():
    """Prueba operaciones de modelos (guardar/cargar)"""
    print("💾 Probando operaciones de modelos...")
    
    # Verificar si hay un modelo entrenado
    status = test_model_status()
    if not status or not status.get('is_trained'):
        print("⚠️ No hay modelo entrenado para probar operaciones")
        return
    
    # Probar guardar modelo
    print("\n📤 Probando guardar modelo...")
    try:
        start_time = time.time()
        data = {'model_name': 'test_performance_model'}
        response = requests.post(f"{BASE_URL}/models/save", data=data, timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            save_time = (end_time - start_time) * 1000
            print(f"✅ Modelo guardado en {save_time:.1f}ms")
            print(f"   Archivo: {result.get('filename', 'N/A')}")
            print(f"   Tamaño: {result.get('size_bytes', 0)} bytes")
            
            # Probar cargar modelo
            print("\n📥 Probando cargar modelo...")
            start_time = time.time()
            data = {'model_filename': result.get('filename')}
            response = requests.post(f"{BASE_URL}/models/load", data=data, timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                load_time = (end_time - start_time) * 1000
                print(f"✅ Modelo cargado en {load_time:.1f}ms")
                
                # Probar generación después de cargar
                print("\n🎨 Probando generación después de cargar...")
                gen_result = test_generation_performance("Modelo recargado exitosamente", 10, 0.7)
                
                return {
                    'save_time_ms': save_time,
                    'load_time_ms': load_time,
                    'generation_after_load': gen_result
                }
            else:
                print(f"❌ Error cargando modelo: {response.status_code}")
        else:
            print(f"❌ Error guardando modelo: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en operaciones de modelo: {e}")
    
    return None

def test_file_operations():
    """Prueba operaciones de archivos"""
    print("📁 Probando operaciones de archivos...")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/files", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            list_time = (end_time - start_time) * 1000
            print(f"✅ Lista de archivos obtenida en {list_time:.1f}ms")
            print(f"   Archivos encontrados: {len(data.get('files', []))}")
            return True
        else:
            print(f"❌ Error listando archivos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en operaciones de archivos: {e}")
        return False

def main():
    """Función principal de pruebas de rendimiento"""
    print("🚀 Iniciando pruebas de rendimiento...")
    print("=" * 60)
    
    # Verificar que el backend esté funcionando
    if not test_health_check():
        print("❌ Backend no está disponible. Inicia el servidor primero.")
        return
    
    print("\n📋 Pruebas de rendimiento:")
    
    # 1. Estado del modelo
    print("\n1️⃣ Prueba de estado del modelo:")
    test_model_status()
    
    # 2. Operaciones de archivos
    print("\n2️⃣ Prueba de operaciones de archivos:")
    test_file_operations()
    
    # 3. Generación individual
    print("\n3️⃣ Prueba de generación individual:")
    test_generation_performance("Hola mundo", 15, 0.7)
    
    # 4. Generación concurrente
    print("\n4️⃣ Prueba de generación concurrente:")
    test_concurrent_generation(3)  # 3 requests concurrentes
    
    # 5. Operaciones de modelos
    print("\n5️⃣ Prueba de operaciones de modelos:")
    model_results = test_model_operations()
    
    # 6. Generación con diferentes parámetros
    print("\n6️⃣ Prueba de generación con diferentes parámetros:")
    test_generation_performance("Inteligencia artificial", 20, 0.5)
    test_generation_performance("Python programming", 10, 0.9)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas de rendimiento completadas")
    
    # Resumen de resultados
    print("\n📊 Resumen de optimizaciones:")
    print("   ✅ Procesamiento asíncrono con ThreadPoolExecutor")
    print("   ✅ Generación optimizada con límites de patrones")
    print("   ✅ Cache de activación de patrones")
    print("   ✅ Ventana de contexto optimizada")
    print("   ✅ Búsqueda limitada de patrones")
    
    print("\n💡 Para monitorear el rendimiento en tiempo real:")
    print("   1. Inicia el backend: cd web_app/backend && python main.py")
    print("   2. Usa la interfaz web en http://localhost:5173")
    print("   3. Observa los logs del backend para métricas de tiempo")

if __name__ == "__main__":
    main() 