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

# Agregar el directorio src al path para importar UltraEfficientLLM
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from ultra_efficient_llm import UltraEfficientLLM

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

# Wrapper para el modelo real UltraEfficientLLM
class UltraEfficientLLMWrapper:
    def __init__(self, max_pattern_length=8, min_frequency=1, max_patterns=10000):
        self.model = UltraEfficientLLM(
            max_pattern_length=max_pattern_length,
            min_frequency=min_frequency,
            max_patterns=max_patterns
        )
        logger.info(f"🔧 Modelo UltraEfficientLLM inicializado con parámetros: max_patterns={max_patterns}, max_pattern_length={max_pattern_length}, min_frequency={min_frequency}")
        
    def train(self, texts):
        """Entrenamiento real del modelo"""
        logger.info(f"🎯 Iniciando entrenamiento con {len(texts)} textos")
        logger.info("📊 Procesando patrones...")
        
        # Entrenar el modelo real
        self.model.train(texts)
        
        logger.info(f"✅ Entrenamiento completado. Patrones extraídos: {len(self.model.patterns)}")
        if self.model.patterns:
            logger.info(f"📈 Patrones principales: {list(self.model.patterns.keys())[:3]}")
        
    def generate(self, prompt, max_length=20, temperature=0.7):
        """Generación real de texto"""
        logger.info(f"🎨 Generando texto con prompt: '{prompt[:50]}...'")
        logger.info(f"⚙️ Parámetros: max_length={max_length}, temperature={temperature}")
        
        if not self.model.is_trained():
            logger.warning("⚠️ Modelo no entrenado")
            return "Modelo no entrenado. Por favor, entrena el modelo primero."
        
        # Generar texto real
        generated_text = self.model.generate(prompt, max_length, temperature)
        logger.info(f"✅ Texto generado: '{generated_text[:50]}...'")
        return generated_text
        
    def get_efficiency_report(self):
        """Reporte real de eficiencia"""
        if not self.model.is_trained():
            return {
                "patterns_stored": 0,
                "memory_kb": 0,
                "sparsity": 0,
                "training_status": "not_trained"
            }
        
        report = self.model.get_efficiency_report()
        logger.info(f"📊 Reporte de eficiencia: {report}")
        return report
        
    def _get_active_patterns(self, prompt):
        """Obtener patrones activos reales"""
        logger.info(f"🔍 Analizando patrones activos para: '{prompt[:30]}...'")
        if not self.model.is_trained():
            return []
        
        active_patterns = self.model._get_active_patterns(prompt)
        logger.info(f"🎯 Patrones activos encontrados: {len(active_patterns)}")
        return active_patterns

# Global model instance
model = UltraEfficientLLMWrapper()
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
    model = UltraEfficientLLMWrapper(
        max_pattern_length=8,
        min_frequency=1,
        max_patterns=10000
    )
    logger.info("✅ UltraEfficientLLM Web API iniciado con modelo real")

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
        "memory_kb": stats.get("memory_kb", 0),
        "is_trained": model.model.is_trained() if hasattr(model, 'model') else False
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
        # Leer archivos de entrenamiento
        logger.info("📖 Leyendo archivos de entrenamiento...")
        training_texts = []
        
        for filename in files:
            file_path = UPLOADS_DIR / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Procesar contenido según el tipo de archivo
                    if filename.endswith('.csv'):
                        # Procesar CSV
                        import csv
                        import io
                        csv_reader = csv.DictReader(io.StringIO(content))
                        for row in csv_reader:
                            if 'texto' in row:
                                training_texts.append(row['texto'])
                            elif 'text' in row:
                                training_texts.append(row['text'])
                    else:
                        # Procesar texto plano
                        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                        training_texts.extend(paragraphs)
                        
                    logger.info(f"✅ Archivo {filename} procesado: {len(training_texts)} textos")
                    
                except Exception as e:
                    logger.error(f"❌ Error procesando archivo {filename}: {str(e)}")
                    continue
        
        training_status.update({
            "progress": 25,
            "message": f"Leyendo archivos... {len(training_texts)} textos encontrados"
        })
        
        if not training_texts:
            raise Exception("No se pudieron extraer textos válidos de los archivos")
        
        logger.info("🔍 Extrayendo patrones...")
        training_status.update({
            "progress": 50,
            "message": "Extrayendo patrones..."
        })
        
        logger.info("🧠 Inicializando modelo...")
        # Initialize model with new parameters
        model = UltraEfficientLLMWrapper(
            max_pattern_length=max_pattern_length,
            min_frequency=min_frequency,
            max_patterns=max_patterns
        )
        
        training_status.update({
            "progress": 75,
            "message": "Entrenando modelo..."
        })
        
        # Train model with real data
        model.train(training_texts)
        
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
                "texts_processed": len(training_texts),
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
    
    if not model.model.is_trained():
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
    
    model = UltraEfficientLLMWrapper(
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