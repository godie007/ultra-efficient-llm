#!/usr/bin/env python3
"""
Script de inicio para el backend de UltraEfficientLLM Web App
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add parent directory to path to import UltraEfficientLLM
sys.path.append(str(Path(__file__).parent.parent.parent))

if __name__ == "__main__":
    print("🚀 Iniciando UltraEfficientLLM Web API...")
    print("📍 Backend: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/api/docs")
    print("🔧 ReDoc: http://localhost:8000/api/redoc")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 