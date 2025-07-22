#!/usr/bin/env python3
"""
UltraEfficientLLM Web API
Backend principal usando FastAPI
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import List, Optional
import json
import asyncio
from datetime import datetime

# Add parent directory to path to import UltraEfficientLLM
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ultra_efficient_llm import UltraEfficientLLM

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

# Global model instance
model: Optional[UltraEfficientLLM] = None
training_status = {
    "is_training": False,
    "progress": 0,
    "status": "idle",
    "message": "Modelo no entrenado"
}

# Create uploads directory
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup"""
    global model
    model = UltraEfficientLLM(
        max_pattern_length=8,
        min_frequency=1,
        max_patterns=10000
    )
    print("🚀 UltraEfficientLLM Web API iniciado")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None
    }

@app.get("/api/model/status")
async def get_model_status():
    """Get current model status"""
    global model, training_status
    
    if model is None:
        return {
            "status": "not_initialized",
            "message": "Modelo no inicializado"
        }
    
    stats = model.get_efficiency_report() if hasattr(model, 'get_efficiency_report') else {}
    
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
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Validate file type
    allowed_extensions = {'.txt', '.md', '.csv', '.json'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed: {allowed_extensions}"
        )
    
    # Save file
    file_path = UPLOADS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "message": "Archivo subido exitosamente",
            "filename": file.filename,
            "file_path": str(file_path),
            "size_bytes": len(content)
        }
    except Exception as e:
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
    
    if training_status["is_training"]:
        raise HTTPException(status_code=400, detail="El modelo ya está entrenando")
    
    if not files:
        raise HTTPException(status_code=400, detail="No se proporcionaron archivos")
    
    # Validate files exist
    file_paths = []
    for file_path in files:
        full_path = UPLOADS_DIR / file_path
        if not full_path.exists():
            raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {file_path}")
        file_paths.append(full_path)
    
    # Start training
    training_status.update({
        "is_training": True,
        "progress": 0,
        "status": "training",
        "message": "Iniciando entrenamiento..."
    })
    
    try:
        # Read training data
        training_texts = []
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split into sentences/lines
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                training_texts.extend(lines)
        
        training_status.update({
            "progress": 20,
            "message": f"Leyendo {len(training_texts)} líneas de texto..."
        })
        
        # Initialize model with new parameters
        model = UltraEfficientLLM(
            max_pattern_length=max_pattern_length,
            min_frequency=min_frequency,
            max_patterns=max_patterns
        )
        
        training_status.update({
            "progress": 40,
            "message": "Modelo inicializado, comenzando entrenamiento..."
        })
        
        # Train model
        model.train(training_texts)
        
        training_status.update({
            "is_training": False,
            "progress": 100,
            "status": "trained",
            "message": f"Entrenamiento completado. {len(training_texts)} líneas procesadas."
        })
        
        # Get final stats
        stats = model.get_efficiency_report()
        
        return {
            "message": "Entrenamiento completado exitosamente",
            "training_data": {
                "files_processed": len(files),
                "lines_processed": len(training_texts),
                "patterns_extracted": stats.get("patterns_stored", 0),
                "memory_used_kb": stats.get("memory_kb", 0)
            },
            "model_stats": stats
        }
        
    except Exception as e:
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
    
    if model is None:
        raise HTTPException(status_code=400, detail="Modelo no inicializado")
    
    if training_status["status"] != "trained":
        raise HTTPException(status_code=400, detail="Modelo no entrenado. Entrene primero el modelo.")
    
    try:
        # Generate text
        generated_text = model.generate(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        # Get active patterns for analysis
        active_patterns = model._get_active_patterns(prompt) if hasattr(model, '_get_active_patterns') else []
        
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
        raise HTTPException(status_code=500, detail=f"Error en generación: {str(e)}")

@app.get("/api/files")
async def list_uploaded_files():
    """List all uploaded files"""
    files = []
    for file_path in UPLOADS_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                "filename": file_path.name,
                "size_bytes": file_path.stat().st_size,
                "uploaded_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
    
    return {"files": files}

@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """Delete uploaded file"""
    file_path = UPLOADS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    try:
        file_path.unlink()
        return {"message": f"Archivo {filename} eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar archivo: {str(e)}")

@app.post("/api/reset")
async def reset_model():
    """Reset the model to initial state"""
    global model, training_status
    
    model = UltraEfficientLLM(
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
    
    return {"message": "Modelo reiniciado exitosamente"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 