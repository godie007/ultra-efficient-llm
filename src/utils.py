"""
Utilidades para UltraEfficientLLM
"""

import logging
import time
from typing import Dict, Any
from datetime import datetime


def setup_logging(level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    Configura el sistema de logging
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        log_file: Archivo de log (opcional)
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear logger
    logger = logging.getLogger("UltraEfficientLLM")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (si se especifica)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_efficiency_metrics(model_stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula métricas de eficiencia del modelo
    
    Args:
        model_stats: Estadísticas del modelo
        
    Returns:
        Dict[str, Any]: Métricas calculadas
    """
    # Memoria tradicional vs ultra-eficiente
    traditional_memory_gb = 14  # GPT-3.5
    ultra_efficient_memory_mb = model_stats.get('memory_kb', 0) / 1024
    
    memory_improvement = (traditional_memory_gb * 1024) / max(ultra_efficient_memory_mb, 0.001)
    
    # Velocidad estimada
    estimated_tokens_per_second = 500  # Estimación basada en el diseño
    
    # Sparsity
    total_patterns = model_stats.get('patterns_stored', 0)
    avg_activations = model_stats.get('activations_per_generation', 0)
    total_generations = model_stats.get('total_generations', 1)
    
    if total_generations > 0:
        avg_activations_per_gen = avg_activations / total_generations
        sparsity = 1 - (avg_activations_per_gen / max(total_patterns, 1))
    else:
        sparsity = 0
        avg_activations_per_gen = 0
    
    # Cache hit rate
    cache_hits = model_stats.get('cache_hits', 0)
    cache_hit_rate = cache_hits / max(total_generations, 1)
    
    return {
        'memory_usage_mb': ultra_efficient_memory_mb,
        'memory_improvement_vs_traditional': f"{memory_improvement:.0f}x",
        'estimated_tokens_per_second': estimated_tokens_per_second,
        'sparsity_achieved': f"{sparsity:.1%}",
        'cache_hit_rate': f"{cache_hit_rate:.1%}",
        'average_activations_per_generation': f"{avg_activations_per_gen:.2f}",
        'total_patterns_stored': total_patterns,
        'total_generations': total_generations
    }


def format_time(seconds: float) -> str:
    """
    Formatea tiempo en formato legible
    
    Args:
        seconds: Tiempo en segundos
        
    Returns:
        str: Tiempo formateado
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_memory(bytes_value: float) -> str:
    """
    Formatea memoria en formato legible
    
    Args:
        bytes_value: Memoria en bytes
        
    Returns:
        str: Memoria formateada
    """
    if bytes_value < 1024:
        return f"{bytes_value:.0f}B"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.1f}KB"
    elif bytes_value < 1024 * 1024 * 1024:
        return f"{bytes_value / (1024 * 1024):.1f}MB"
    else:
        return f"{bytes_value / (1024 * 1024 * 1024):.1f}GB"


def print_efficiency_report(metrics: Dict[str, Any]) -> None:
    """
    Imprime un reporte de RECURSOS del motor n-grama (memoria, velocidad, sparsity).

    No es una métrica de CALIDAD: la calidad real se mide con perplejidad
    (ver src/evaluation.py). Acepta tanto la salida de get_efficiency_report()
    como la de get_efficiency_metrics().

    Args:
        metrics: Métricas de recursos del modelo
    """
    print("\n" + "="*60)
    print("📊 RECURSOS DEL MOTOR N-GRAMA")
    print("="*60)

    if 'memory_usage_mb' in metrics:
        print(f"💾 Memoria: {metrics['memory_usage_mb']:.2f} MB")
    elif 'memory_kb' in metrics:
        print(f"💾 Memoria: {metrics['memory_kb']:.2f} KB")

    patterns = metrics.get('patterns_stored', metrics.get('total_patterns_stored'))
    if patterns is not None:
        print(f"🧮 Patrones almacenados: {patterns}")

    if 'sparsity_achieved' in metrics:
        print(f"🎯 Sparsity: {metrics['sparsity_achieved']}")
    if 'cache_hit_rate' in metrics:
        print(f"🔥 Cache hit rate: {metrics['cache_hit_rate']}")

    print("\nℹ️  Métricas de recursos, no de calidad. Perplejidad: src/evaluation.py")
    print("="*60)


def create_timestamp() -> str:
    """
    Crea timestamp para archivos
    
    Returns:
        str: Timestamp formateado
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def validate_model_parameters(max_pattern_length: int, min_frequency: int, max_patterns: int) -> bool:
    """
    Valida parámetros del modelo
    
    Args:
        max_pattern_length: Longitud máxima de patrones
        min_frequency: Frecuencia mínima
        max_patterns: Número máximo de patrones
        
    Returns:
        bool: True si los parámetros son válidos
    """
    if max_pattern_length < 1 or max_pattern_length > 20:
        print("❌ max_pattern_length debe estar entre 1 y 20")
        return False
    
    if min_frequency < 1:
        print("❌ min_frequency debe ser al menos 1")
        return False
    
    if max_patterns < 100 or max_patterns > 100000:
        print("❌ max_patterns debe estar entre 100 y 100000")
        return False
    
    return True


class Timer:
    """Context manager para medir tiempo de ejecución"""
    
    def __init__(self, description: str = "Operación"):
        self.description = description
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        print(f"⏱️ Iniciando: {self.description}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"✅ Completado: {self.description} en {format_time(elapsed)}")
    
    def get_elapsed(self) -> float:
        """Retorna tiempo transcurrido en segundos"""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        return 0.0 