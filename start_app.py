#!/usr/bin/env python3
"""
🚀 ULTRAEFFICIENTLLM - ARCHIVO DE EJECUCIÓN DEFINITIVO
=======================================================

Este es el ÚNICO archivo que necesitas ejecutar para usar la aplicación.

OPCIONES:
1. python start_app.py --web     -> Inicia la aplicación web completa
2. python start_app.py --demo    -> Ejecuta demo con libro Frankenstein
3. python start_app.py --test    -> Prueba el modelo con dataset de acuaponía
4. python start_app.py --help    -> Muestra esta ayuda
"""

import sys
import os
import subprocess
import time
import requests
import argparse
from pathlib import Path

# Agregar src al path
sys.path.append('src')

def check_dependencies():
    """Verificar dependencias necesarias"""
    print("🔍 Verificando dependencias...")
    
    # Verificar Python
    try:
        import fastapi
        print("✅ fastapi instalado")
    except ImportError:
        print("❌ fastapi no está instalado. Ejecuta: pip install fastapi uvicorn")
        return False
    
    try:
        import uvicorn
        print("✅ uvicorn instalado")
    except ImportError:
        print("❌ uvicorn no está instalado. Ejecuta: pip install uvicorn")
        return False
    
    return True

def start_web_app():
    """Iniciar aplicación web completa"""
    print("🌐 INICIANDO APLICACIÓN WEB ULTRAEFFICIENTLLM")
    print("=" * 50)
    
    if not check_dependencies():
        return False
    
    # Verificar si el backend ya está corriendo
    try:
        response = requests.get("http://localhost:8001/api/health", timeout=2)
        if response.status_code == 200:
            print("✅ El backend ya está funcionando en http://localhost:8001")
            print("🌐 URLs disponibles:")
            print("   - API: http://localhost:8001")
            print("   - Documentación: http://localhost:8001/api/docs")
            return True
    except:
        pass
    
    # Iniciar backend
    print("🔄 Iniciando backend...")
    backend_dir = Path("web_app/backend")
    
    if not backend_dir.exists():
        print("❌ No se encontró el directorio backend")
        return False
    
    try:
        # Cambiar al directorio backend
        os.chdir(backend_dir)
        
        # Iniciar servidor
        process = subprocess.Popen([
            sys.executable, "main.py"
        ])
        
        print("⏳ Esperando a que el backend esté listo...")
        
        # Esperar hasta 30 segundos
        for i in range(30):
            time.sleep(1)
            try:
                response = requests.get("http://localhost:8001/api/health", timeout=2)
                if response.status_code == 200:
                    print("✅ ¡Backend iniciado exitosamente!")
                    print("\n🌐 URLs disponibles:")
                    print("   - API Principal: http://localhost:8001")
                    print("   - Health Check: http://localhost:8001/api/health")
                    print("   - Documentación: http://localhost:8001/api/docs")
                    print("   - Model Status: http://localhost:8001/api/model/status")
                    print("\n📝 Para probar:")
                    print("   1. Ve a http://localhost:8001/api/docs")
                    print("   2. Usa el endpoint /api/train para entrenar")
                    print("   3. Usa el endpoint /api/generate para generar texto")
                    print("\n🛑 Presiona Ctrl+C para detener")
                    
                    # Mantener el proceso corriendo
                    try:
                        process.wait()
                    except KeyboardInterrupt:
                        print("\n🛑 Deteniendo servidor...")
                        process.terminate()
                        process.wait()
                        print("✅ Servidor detenido")
                    return True
            except:
                continue
        
        print("❌ El backend no respondió en 30 segundos")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"❌ Error iniciando el backend: {e}")
        return False
    finally:
        # Volver al directorio original
        os.chdir(Path.cwd().parent)

def run_demo():
    """Ejecutar demo con libro Frankenstein"""
    print("📚 EJECUTANDO DEMO CON LIBRO FRANKENSTEIN")
    print("=" * 50)
    
    if not check_dependencies():
        return False
    
    try:
        # Ejecutar el demo principal
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Demo ejecutado exitosamente")
            print(result.stdout)
        else:
            print("❌ Error ejecutando demo")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def test_model():
    """Probar el modelo con dataset de acuaponía"""
    print("🧪 PROBANDO MODELO CON DATASET DE ACUAPONÍA")
    print("=" * 50)
    
    try:
        from ultra_efficient_llm import UltraEfficientLLM
        
        # Cargar dataset
        dataset_file = Path("data/acuaponia_minimal.txt")
        if not dataset_file.exists():
            print(f"❌ No se encontró el dataset: {dataset_file}")
            return False
        
        with open(dataset_file, 'r', encoding='utf-8') as f:
            dataset = [linea.strip() for linea in f if linea.strip()]
        
        print(f"📚 Dataset cargado: {len(dataset)} líneas")
        
        # Crear y entrenar modelo
        print("🧠 Creando modelo...")
        model = UltraEfficientLLM(
            max_pattern_length=6,
            min_frequency=1,
            max_patterns=6000
        )
        
        print("🔄 Entrenando modelo...")
        model.train(dataset)
        
        print("✅ Modelo entrenado exitosamente")
        
        # Probar generación
        print("\n✨ Probando generación de texto...")
        
        preguntas = [
            "¿Qué es la acuaponía?",
            "¿Qué peces puedo usar?",
            "¿Qué plantas crecen?",
            "¿Cuánta agua usa?",
            "¿Es orgánica?"
        ]
        
        for pregunta in preguntas:
            print(f"\n❓ {pregunta}")
            respuesta = model.generate(pregunta, max_length=30, temperature=0.3)
            print(f"🤖 {respuesta}")
        
        print("\n🎉 ¡Test completado!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_help():
    """Mostrar ayuda"""
    print(__doc__)
    print("\n📋 EJEMPLOS DE USO:")
    print("   python start_app.py --web     # Inicia aplicación web")
    print("   python start_app.py --demo    # Ejecuta demo con libro")
    print("   python start_app.py --test    # Prueba modelo acuaponía")
    print("   python start_app.py --help    # Muestra esta ayuda")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="UltraEfficientLLM - Archivo de ejecución definitivo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EJEMPLOS:
  python start_app.py --web     Inicia la aplicación web completa
  python start_app.py --demo    Ejecuta demo con libro Frankenstein
  python start_app.py --test    Prueba el modelo con dataset de acuaponía
  python start_app.py --help    Muestra esta ayuda
        """
    )
    
    parser.add_argument('--web', action='store_true', help='Iniciar aplicación web')
    parser.add_argument('--demo', action='store_true', help='Ejecutar demo con libro')
    parser.add_argument('--test', action='store_true', help='Probar modelo acuaponía')
    
    args = parser.parse_args()
    
    # Si no se especificó ninguna opción, mostrar ayuda
    if not any([args.web, args.demo, args.test]):
        show_help()
        return
    
    print("🚀 ULTRAEFFICIENTLLM - ARCHIVO DE EJECUCIÓN DEFINITIVO")
    print("=" * 60)
    
    success = False
    
    if args.web:
        success = start_web_app()
    elif args.demo:
        success = run_demo()
    elif args.test:
        success = test_model()
    
    if success:
        print("\n✅ Operación completada exitosamente")
    else:
        print("\n❌ La operación falló")
        sys.exit(1)

if __name__ == "__main__":
    main() 