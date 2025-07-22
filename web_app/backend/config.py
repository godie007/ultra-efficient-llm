#!/usr/bin/env python3
"""
Configuración centralizada para optimizaciones de rendimiento
"""

import os
from typing import Dict, Any

class PerformanceConfig:
    """Configuración de rendimiento para el UltraEfficientLLM Web API"""
    
    # Configuración del Thread Pool
    THREAD_POOL_MAX_WORKERS = int(os.getenv('THREAD_POOL_MAX_WORKERS', '4'))
    THREAD_POOL_TIMEOUT = int(os.getenv('THREAD_POOL_TIMEOUT', '30'))
    
    # Configuración de generación de texto
    MAX_PATTERNS_PER_QUERY = int(os.getenv('MAX_PATTERNS_PER_QUERY', '1000'))
    MAX_BACKUP_PATTERNS = int(os.getenv('MAX_BACKUP_PATTERNS', '100'))
    CONTEXT_WINDOW_SIZE = int(os.getenv('CONTEXT_WINDOW_SIZE', '6'))
    MIN_GENERATED_TOKENS_RATIO = float(os.getenv('MIN_GENERATED_TOKENS_RATIO', '0.33'))
    
    # Configuración de cache
    ACTIVATION_CACHE_SIZE = int(os.getenv('ACTIVATION_CACHE_SIZE', '1000'))
    CACHE_KEY_LENGTH = int(os.getenv('CACHE_KEY_LENGTH', '20'))
    
    # Configuración de umbrales
    ACTIVATION_THRESHOLD = float(os.getenv('ACTIVATION_THRESHOLD', '0.1'))
    FREQUENCY_NORMALIZATION = float(os.getenv('FREQUENCY_NORMALIZATION', '5.0'))
    
    # Configuración de timeouts
    GENERATION_TIMEOUT = int(os.getenv('GENERATION_TIMEOUT', '30'))
    TRAINING_TIMEOUT = int(os.getenv('TRAINING_TIMEOUT', '300'))
    SAVE_LOAD_TIMEOUT = int(os.getenv('SAVE_LOAD_TIMEOUT', '30'))
    
    # Configuración de logging
    ENABLE_PERFORMANCE_LOGGING = os.getenv('ENABLE_PERFORMANCE_LOGGING', 'true').lower() == 'true'
    LOG_SLOW_OPERATIONS_MS = int(os.getenv('LOG_SLOW_OPERATIONS_MS', '100'))
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Obtiene toda la configuración como diccionario"""
        return {
            'thread_pool': {
                'max_workers': cls.THREAD_POOL_MAX_WORKERS,
                'timeout': cls.THREAD_POOL_TIMEOUT
            },
            'generation': {
                'max_patterns_per_query': cls.MAX_PATTERNS_PER_QUERY,
                'max_backup_patterns': cls.MAX_BACKUP_PATTERNS,
                'context_window_size': cls.CONTEXT_WINDOW_SIZE,
                'min_generated_tokens_ratio': cls.MIN_GENERATED_TOKENS_RATIO
            },
            'cache': {
                'activation_cache_size': cls.ACTIVATION_CACHE_SIZE,
                'cache_key_length': cls.CACHE_KEY_LENGTH
            },
            'thresholds': {
                'activation_threshold': cls.ACTIVATION_THRESHOLD,
                'frequency_normalization': cls.FREQUENCY_NORMALIZATION
            },
            'timeouts': {
                'generation': cls.GENERATION_TIMEOUT,
                'training': cls.TRAINING_TIMEOUT,
                'save_load': cls.SAVE_LOAD_TIMEOUT
            },
            'logging': {
                'enable_performance_logging': cls.ENABLE_PERFORMANCE_LOGGING,
                'log_slow_operations_ms': cls.LOG_SLOW_OPERATIONS_MS
            }
        }
    
    @classmethod
    def print_config(cls):
        """Imprime la configuración actual"""
        print("⚙️ Configuración de Rendimiento:")
        print("=" * 40)
        
        config = cls.get_config()
        for category, settings in config.items():
            print(f"\n📁 {category.upper()}:")
            for key, value in settings.items():
                print(f"   {key}: {value}")
        
        print("\n💡 Para cambiar configuración, usa variables de entorno:")
        print("   export THREAD_POOL_MAX_WORKERS=8")
        print("   export MAX_PATTERNS_PER_QUERY=2000")
        print("   export ENABLE_PERFORMANCE_LOGGING=true")

# Configuración para diferentes entornos
class DevelopmentConfig(PerformanceConfig):
    """Configuración optimizada para desarrollo"""
    THREAD_POOL_MAX_WORKERS = 2
    MAX_PATTERNS_PER_QUERY = 500
    ENABLE_PERFORMANCE_LOGGING = True
    LOG_SLOW_OPERATIONS_MS = 50

class ProductionConfig(PerformanceConfig):
    """Configuración optimizada para producción"""
    THREAD_POOL_MAX_WORKERS = 8
    MAX_PATTERNS_PER_QUERY = 2000
    ENABLE_PERFORMANCE_LOGGING = False
    LOG_SLOW_OPERATIONS_MS = 200

class HighPerformanceConfig(PerformanceConfig):
    """Configuración para máximo rendimiento"""
    THREAD_POOL_MAX_WORKERS = 16
    MAX_PATTERNS_PER_QUERY = 5000
    CONTEXT_WINDOW_SIZE = 8
    ACTIVATION_CACHE_SIZE = 5000
    ENABLE_PERFORMANCE_LOGGING = True
    LOG_SLOW_OPERATIONS_MS = 10

# Función para obtener la configuración según el entorno
def get_performance_config() -> PerformanceConfig:
    """Obtiene la configuración según el entorno"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'high_performance':
        return HighPerformanceConfig()
    else:
        return DevelopmentConfig()

if __name__ == "__main__":
    # Imprimir configuración actual
    config = get_performance_config()
    config.print_config() 