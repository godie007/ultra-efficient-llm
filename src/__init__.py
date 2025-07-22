"""
UltraEfficientLLM - Modelo de Lenguaje Ultra-Eficiente
"""

from .ultra_efficient_llm import UltraEfficientLLM
from .data_processor import DataProcessor
from .utils import setup_logging, get_efficiency_metrics

__version__ = "1.0.0"
__author__ = "UltraEfficientLLM Team"

__all__ = [
    "UltraEfficientLLM",
    "DataProcessor", 
    "setup_logging",
    "get_efficiency_metrics"
] 