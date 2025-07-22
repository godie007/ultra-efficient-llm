#!/usr/bin/env python3
"""
UltraEfficientLLM Web API - Versión Simplificada
Backend principal usando FastAPI
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn
from typing import List, Optional
import json
import asyncio
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="UltraEfficientLLM Web API",
    description="API para entrenar y evaluar el UltraEfficientLLM",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock model for demonstration
class MockUltraEfficientLLM:
    def __init__(self, max_pattern_length=8, min_frequency=1, max_patterns=10000):
        self.max_pattern_length = max_pattern_length
        self.min_frequency = min_frequency
        self.max_patterns = max_patterns
        self.patterns = {}
        self.is_trained = False
        logger.info(f"🔧 Modelo inicializado con parámetros: max_patterns={max_patterns}, max_pattern_length={max_pattern_length}, min_frequency={min_frequency}")
        
    def train(self, texts):
        """Mock training"""
        logger.info(f"🎯 Iniciando entrenamiento con {len(texts)} textos")
        logger.info("📊 Procesando patrones...")
        
        # Simular procesamiento de patrones
        self.patterns = {"hello": 5, "world": 3, "machine": 2, "learning": 4, "artificial": 3, "intelligence": 4}
        self.is_trained = True
        
        logger.info(f"✅ Entrenamiento completado. Patrones extraídos: {len(self.patterns)}")
        logger.info(f"📈 Patrones principales: {list(self.patterns.keys())[:3]}")
        
    def generate(self, prompt, max_length=20, temperature=0.7):
        """Mock text generation"""
        logger.info(f"🎨 Generando texto con prompt: '{prompt[:50]}...'")
        logger.info(f"⚙️ Parámetros: max_length={max_length}, temperature={temperature}")
        
        if not self.is_trained:
            logger.warning("⚠️ Modelo no entrenado")
            return "Modelo no entrenado"
        
        # Simple mock generation
        responses = [
            "Este es un texto generado por el UltraEfficientLLM basado en los patrones aprendidos durante el entrenamiento.",
            "El modelo ha procesado tu prompt y generado esta respuesta utilizando técnicas de procesamiento de lenguaje natural.",
            "Basado en los patrones aprendidos durante el entrenamiento, aquí tienes el resultado de la generación de texto.",
            "La generación de texto se completó exitosamente utilizando el modelo UltraEfficientLLM entrenado."
        ]
        import random
        response = random.choice(responses)
        logger.info(f"✅ Texto generado: '{response[:50]}...'")
        return response
        
    def get_efficiency_report(self):
        """Mock efficiency report"""
        report = {
            "patterns_stored": len(self.patterns),
            "memory_kb": 13.6,
            "sparsity": 0.999,
            "training_status": "completed" if self.is_trained else "not_trained"
        }
        logger.info(f"📊 Reporte de eficiencia: {report}")
        return report
        
    def _get_active_patterns(self, prompt):
        """Mock active patterns"""
        logger.info(f"🔍 Analizando patrones activos para: '{prompt[:30]}...'")
        patterns = [("hello", 0.8), ("world", 0.6), ("machine", 0.4), ("learning", 0.7), ("artificial", 0.5)]
        logger.info(f"🎯 Patrones activos encontrados: {len(patterns)}")
        return patterns

# Global model instance
model = MockUltraEfficientLLM()
training_status = {
    "is_training": False,
    "progress": 0,
    "status": "idle",
    "message": "Modelo no entrenado"
}

# Create uploads directory
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)
logger.info(f"📁 Directorio de uploads creado: {UPLOADS_DIR.absolute()}")

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup"""
    global model
    logger.info("🚀 Iniciando UltraEfficientLLM Web API...")
    model = MockUltraEfficientLLM(
        max_pattern_length=8,
        min_frequency=1,
        max_patterns=10000
    )
    logger.info("✅ UltraEfficientLLM Web API iniciado (versión mock)")

@app.get("/")
async def root():
    """Root endpoint - redirect to API docs"""
    logger.info("🌐 Acceso a ruta raíz")
    return {
        "message": "UltraEfficientLLM Web API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "model_status": "/api/model/status",
            "upload": "/api/upload",
            "train": "/api/train",
            "generate": "/api/generate",
            "files": "/api/files",
            "docs": "/api/docs",
            "redoc": "/api/redoc"
        },
        "frontend": "http://localhost:5173"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    logger.info("🏥 Health check solicitado")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "version": "mock"
    }

@app.get("/api/model/status")
async def get_model_status():
    """Get current model status"""
    global model, training_status
    
    logger.info("📊 Consulta de estado del modelo")
    
    if model is None:
        logger.warning("⚠️ Modelo no inicializado")
        return {
            "status": "not_initialized",
            "message": "Modelo no inicializado"
        }
    
    stats = model.get_efficiency_report()
    
    logger.info(f"📈 Estado actual: {training_status['status']}, Progreso: {training_status['progress']}%")
    
    return {
        "status": training_status["status"],
        "is_training": training_status["is_training"],
        "progress": training_status["progress"],
        "message": training_status["message"],
        "model_stats": stats,
        "patterns_stored": stats.get("patterns_stored", 0),
        "memory_kb": stats.get("memory_kb", 0)
    }

@app.post("/api/upload")
async def upload_training_file(file: UploadFile = File(...)):
    """Upload training file"""
    logger.info(f"📤 Iniciando subida de archivo: {file.filename}")
    
    if not file.filename:
        logger.error("❌ No se proporcionó nombre de archivo")
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Validate file type
    allowed_extensions = {'.txt', '.md', '.csv', '.json'}
    file_ext = Path(file.filename).suffix.lower()
    
    logger.info(f"🔍 Validando extensión: {file_ext}")
    
    if file_ext not in allowed_extensions:
        logger.error(f"❌ Tipo de archivo no permitido: {file_ext}")
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed: {allowed_extensions}"
        )
    
    # Save file
    file_path = UPLOADS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    
    try:
        logger.info(f"💾 Guardando archivo en: {file_path}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"✅ Archivo subido exitosamente: {len(content)} bytes")
        
        return {
            "message": "Archivo subido exitosamente",
            "filename": file.filename,
            "file_path": str(file_path),
            "size_bytes": len(content)
        }
    except Exception as e:
        logger.error(f"❌ Error al subir archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")

@app.post("/api/train")
async def train_model(
    files: List[str] = Form(...),
    max_patterns: int = Form(10000),
    max_pattern_length: int = Form(8),
    min_frequency: int = Form(1)
):
    """Train the model with uploaded files"""
    global model, training_status
    
    logger.info(f"🎯 Iniciando entrenamiento con {len(files)} archivos")
    logger.info(f"⚙️ Parámetros: max_patterns={max_patterns}, max_pattern_length={max_pattern_length}, min_frequency={min_frequency}")
    
    if training_status["is_training"]:
        logger.warning("⚠️ El modelo ya está entrenando")
        raise HTTPException(status_code=400, detail="El modelo ya está entrenando")
    
    if not files:
        logger.error("❌ No se proporcionaron archivos")
        raise HTTPException(status_code=400, detail="No se proporcionaron archivos")
    
    # Start training
    logger.info("🚀 Iniciando proceso de entrenamiento...")
    training_status.update({
        "is_training": True,
        "progress": 0,
        "status": "training",
        "message": "Iniciando entrenamiento..."
    })
    
    try:
        # Simulate training process
        logger.info("📖 Leyendo archivos de entrenamiento...")
        await asyncio.sleep(2)  # Simulate processing time
        
        training_status.update({
            "progress": 25,
            "message": "Leyendo archivos..."
        })
        logger.info("✅ Archivos leídos correctamente")
        
        logger.info("🔍 Extrayendo patrones...")
        await asyncio.sleep(2)  # Simulate more processing time
        
        training_status.update({
            "progress": 50,
            "message": "Extrayendo patrones..."
        })
        logger.info("✅ Patrones extraídos")
        
        logger.info("🧠 Inicializando modelo...")
        # Initialize model with new parameters
        model = MockUltraEfficientLLM(
            max_pattern_length=max_pattern_length,
            min_frequency=min_frequency,
            max_patterns=max_patterns
        )
        
        training_status.update({
            "progress": 75,
            "message": "Entrenando modelo..."
        })
        
        # Train model
        model.train([])  # Mock training
        
        training_status.update({
            "is_training": False,
            "progress": 100,
            "status": "trained",
            "message": f"Entrenamiento completado. {len(files)} archivos procesados."
        })
        
        logger.info("🎉 Entrenamiento completado exitosamente")
        
        # Get final stats
        stats = model.get_efficiency_report()
        
        return {
            "message": "Entrenamiento completado exitosamente",
            "training_data": {
                "files_processed": len(files),
                "lines_processed": 100,  # Mock data
                "patterns_extracted": stats.get("patterns_stored", 0),
                "memory_used_kb": stats.get("memory_kb", 0)
            },
            "model_stats": stats
        }
        
    except Exception as e:
        logger.error(f"❌ Error durante el entrenamiento: {str(e)}")
        training_status.update({
            "is_training": False,
            "status": "error",
            "message": f"Error en entrenamiento: {str(e)}"
        })
        raise HTTPException(status_code=500, detail=f"Error en entrenamiento: {str(e)}")

@app.post("/api/generate")
async def generate_text(
    prompt: str = Form(...),
    max_length: int = Form(20),
    temperature: float = Form(0.7)
):
    """Generate text using the trained model"""
    global model, training_status
    
    logger.info(f"🎨 Solicitud de generación de texto")
    logger.info(f"📝 Prompt: '{prompt[:50]}...'")
    logger.info(f"⚙️ Parámetros: max_length={max_length}, temperature={temperature}")
    
    if model is None:
        logger.error("❌ Modelo no inicializado")
        raise HTTPException(status_code=400, detail="Modelo no inicializado")
    
    if training_status["status"] != "trained":
        logger.warning("⚠️ Modelo no entrenado")
        raise HTTPException(status_code=400, detail="Modelo no entrenado. Entrene primero el modelo.")
    
    try:
        # Generate text
        generated_text = model.generate(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        # Get active patterns for analysis
        active_patterns = model._get_active_patterns(prompt)
        
        logger.info(f"✅ Generación completada: '{generated_text[:50]}...'")
        
        return {
            "prompt": prompt,
            "generated_text": generated_text,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature
            },
            "analysis": {
                "active_patterns": len(active_patterns),
                "patterns": [{"pattern": p[0], "score": p[1]} for p in active_patterns[:5]]
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error en generación: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en generación: {str(e)}")

@app.get("/api/files")
async def list_uploaded_files():
    """List all uploaded files"""
    logger.info("📁 Listando archivos subidos")
    
    files = []
    for file_path in UPLOADS_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                "filename": file_path.name,
                "size_bytes": file_path.stat().st_size,
                "uploaded_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
    
    logger.info(f"✅ Encontrados {len(files)} archivos")
    return {"files": files}

@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """Delete uploaded file"""
    logger.info(f"🗑️ Eliminando archivo: {filename}")
    
    file_path = UPLOADS_DIR / filename
    
    if not file_path.exists():
        logger.error(f"❌ Archivo no encontrado: {filename}")
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    try:
        file_path.unlink()
        logger.info(f"✅ Archivo eliminado: {filename}")
        return {"message": f"Archivo {filename} eliminado exitosamente"}
    except Exception as e:
        logger.error(f"❌ Error al eliminar archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar archivo: {str(e)}")

@app.post("/api/reset")
async def reset_model():
    """Reset the model to initial state"""
    global model, training_status
    
    logger.info("🔄 Reiniciando modelo")
    
    model = MockUltraEfficientLLM(
        max_pattern_length=8,
        min_frequency=1,
        max_patterns=10000
    )
    
    training_status.update({
        "is_training": False,
        "progress": 0,
        "status": "idle",
        "message": "Modelo reiniciado"
    })
    
    logger.info("✅ Modelo reiniciado exitosamente")
    return {"message": "Modelo reiniciado exitosamente"}

if __name__ == "__main__":
    print("🚀 Iniciando UltraEfficientLLM Web API (versión mock)...")
    print("📍 Backend: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/api/docs")
    print("=" * 50)
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 