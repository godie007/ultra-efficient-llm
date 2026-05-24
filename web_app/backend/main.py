#!/usr/bin/env python3
"""
Entrypoint del backend del asistente RAG.

Estructura:
- config.py    parámetros (rutas, modelo, CORS)
- schemas.py   modelos de request
- service.py   RAGService: estado, persistencia del corpus y orquestación RAG
- routes.py    rutas HTTP (capa fina sobre el servicio)
- main.py      crea la app FastAPI, monta middleware y rutas, y arranca uvicorn
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_ORIGINS
from routes import router
from service import service

app = FastAPI(
    title="Asistente RAG",
    description="Chat sobre fuentes de conocimiento personalizables",
    version="2.0.0",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    service.ensure_ready()  # cargar modelos antes de servir (no dependemos del evento lifespan)
    print("🚀 Iniciando Asistente RAG en http://localhost:8000 (docs en /api/docs)")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
