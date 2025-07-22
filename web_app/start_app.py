#!/usr/bin/env python3
"""
Script de inicio para la aplicación web UltraEfficientLLM
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_backend():
    """Iniciar el backend"""
    print("🚀 Iniciando Backend...")
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    try:
        # Ejecutar el backend
        process = subprocess.Popen([
            sys.executable, "simple_main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Backend iniciado en http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Error iniciando backend: {e}")
        return None

def start_frontend():
    """Iniciar el frontend"""
    print("🌐 Iniciando Frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        # Ejecutar el frontend
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Frontend iniciado en http://localhost:5173")
        return process
    except Exception as e:
        print(f"❌ Error iniciando frontend: {e}")
        return None

def main():
    print("=" * 60)
    print("🌐 UltraEfficientLLM Web Application")
    print("=" * 60)
    
    # Iniciar backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ No se pudo iniciar el backend")
        return
    
    # Esperar un poco
    time.sleep(3)
    
    # Iniciar frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ No se pudo iniciar el frontend")
        backend_process.terminate()
        return
    
    print("\n" + "=" * 60)
    print("🎉 ¡Aplicación iniciada exitosamente!")
    print("=" * 60)
    print("📍 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print("🌐 Frontend: http://localhost:5173")
    print("=" * 60)
    print("Presiona Ctrl+C para detener la aplicación")
    print("=" * 60)
    
    try:
        # Mantener los procesos ejecutándose
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo aplicación...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Aplicación detenida")

if __name__ == "__main__":
    main() 