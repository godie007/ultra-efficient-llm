"""Configuración del backend del asistente RAG."""

import os
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CORPUS_PATH = ROOT / "data" / "corpus" / "knowledge_base.json"

# Modelo de generación (configurable por variable de entorno).
DEFAULT_MODEL = os.environ.get("RAG_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")

# CORS: orígenes permitidos del frontend.
ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]

# Parámetros de recuperación y generación.
DEFAULT_TOP_K = 3
MAX_NEW_TOKENS = 200
TEMPERATURE = 0.3
