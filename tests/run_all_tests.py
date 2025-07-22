#!/usr/bin/env python3
"""
Script principal para ejecutar todos los tests del proyecto UltraEfficientLLM
"""

import sys
import os
import subprocess
import time

def run_test(test_file, description):
    """Ejecuta un test específico"""
    print(f"\n🧪 EJECUTANDO: {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ TEST EXITOSO")
            print(result.stdout)
        else:
            print("❌ TEST FALLÓ")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ TEST TIMEOUT - Tardó más de 2 minutos")
        return False
    except Exception as e:
        print(f"❌ ERROR EJECUTANDO TEST: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 ULTRAEFFICIENTLLM - SUITE DE TESTS COMPLETA")
    print("=" * 60)
    print("Ejecutando todos los tests importantes del proyecto...")
    
    # Lista de tests a ejecutar
    tests = [
        ("test_acuaponia_final.py", "Test Final de Acuaponía"),
        ("test_performance.py", "Test de Rendimiento"),
        ("test_web_api.py", "Test de API Web")
    ]
    
    # Cambiar al directorio de tests
    os.chdir(os.path.join(os.path.dirname(__file__), 'tests'))
    
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        if run_test(test_file, description):
            passed += 1
        else:
            print(f"⚠️  {description} falló")
        
        # Pausa entre tests
        time.sleep(1)
    
    # Resultados finales
    print(f"\n📊 RESULTADOS FINALES DE LA SUITE DE TESTS:")
    print("=" * 60)
    print(f"   Tests pasados: {passed}/{total}")
    print(f"   Tasa de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON! El proyecto está funcionando correctamente")
        print("✅ El modelo UltraEfficientLLM está listo para producción")
    elif passed >= total * 0.7:
        print("👍 LA MAYORÍA DE TESTS PASARON: El proyecto funciona bien")
        print("⚠️  Algunas funcionalidades pueden necesitar ajustes")
    else:
        print("❌ MUCHOS TESTS FALLARON: El proyecto necesita mejoras")
        print("🔧 Revisa los errores y corrige los problemas identificados")

if __name__ == "__main__":
    main() 