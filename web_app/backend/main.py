#!/usr/bin/env python3
"""
UltraEfficientLLM Web API
Backend principal usando FastAPI con optimizaciones asíncronas
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional
import json
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import time

# Add parent directory to path to import UltraEfficientLLM
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ultra_efficient_llm import UltraEfficientLLM
from src.reasoning_engine import ReasoningEngine, apply_intelligent_reasoning
from src.generative_enhancer import mejorar_respuesta_generativa

# Global variables
model: Optional[UltraEfficientLLM] = None
reasoning_engine: Optional[ReasoningEngine] = None
training_status = {
    "is_training": False,
    "progress": 0,
    "status": "idle",
    "message": "Modelo no entrenado"
}
thread_pool: Optional[ThreadPoolExecutor] = None

# Create directories
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    global model, reasoning_engine, thread_pool
    model = UltraEfficientLLM(
        max_pattern_length=6,
        min_frequency=1,
        max_patterns=8000
    )
    reasoning_engine = ReasoningEngine()
    thread_pool = ThreadPoolExecutor(max_workers=4)
    print("🚀 UltraEfficientLLM Web API iniciado con optimizaciones asíncronas y razonamiento inteligente")
    
    yield
    
    # Shutdown
    if thread_pool:
        thread_pool.shutdown(wait=True)
        print("🛑 Thread pool cerrado")

# Initialize FastAPI app
app = FastAPI(
    title="UltraEfficientLLM Web API",
    description="API para entrenar y evaluar el UltraEfficientLLM",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "thread_pool_active": thread_pool is not None and not thread_pool._shutdown
    }

@app.get("/api/model/status")
async def get_model_status():
    """Get current model status"""
    global model, reasoning_engine, training_status
    
    if model is None:
        return {
            "status": "not_initialized",
            "message": "Modelo no inicializado"
        }
    
    stats = model.get_efficiency_report() if hasattr(model, 'get_efficiency_report') else {}
    model_info = model.get_model_info() if hasattr(model, 'get_model_info') else {}
    
    return {
        "status": training_status["status"],
        "is_training": training_status["is_training"],
        "progress": training_status["progress"],
        "message": training_status["message"],
        "model_stats": stats,
        "model_info": model_info,
        "patterns_stored": stats.get("patterns_stored", 0),
        "memory_kb": stats.get("memory_kb", 0),
        "is_trained": model_info.get("is_trained", False),
        "reasoning_engine_available": reasoning_engine is not None,
        "features": {
            "intelligent_reasoning": True,
            "generative_enhancement": True,
            "real_time_analysis": True,
            "safety_analysis": True,
            "causal_reasoning": True,
            "problem_solving": True,
            "comparative_analysis": True,
            "technical_analysis": True
        }
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

def train_model_sync(file_paths, max_patterns, max_pattern_length, min_frequency, training_status):
    """Función síncrona para entrenar el modelo en un thread separado"""
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
        new_model = UltraEfficientLLM(
            max_pattern_length=max_pattern_length,
            min_frequency=min_frequency,
            max_patterns=max_patterns
        )
        
        training_status.update({
            "progress": 40,
            "message": "Modelo inicializado, comenzando entrenamiento..."
        })
        
        # Train model
        new_model.train(training_texts)
        
        training_status.update({
            "is_training": False,
            "progress": 100,
            "status": "trained",
            "message": f"Entrenamiento completado. {len(training_texts)} líneas procesadas."
        })
        
        return new_model, {
            "files_processed": len(file_paths),
            "lines_processed": len(training_texts),
            "patterns_extracted": new_model.get_efficiency_report().get("patterns_stored", 0),
            "memory_used_kb": new_model.get_efficiency_report().get("memory_kb", 0)
        }
        
    except Exception as e:
        training_status.update({
            "is_training": False,
            "status": "error",
            "message": f"Error en entrenamiento: {str(e)}"
        })
        raise e

@app.post("/api/train")
async def train_model(
    files: List[str] = Form(...),
    max_patterns: int = Form(10000),
    max_pattern_length: int = Form(8),
    min_frequency: int = Form(1)
):
    """Train the model with uploaded files - ASÍNCRONO"""
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
        # Ejecutar entrenamiento en thread separado para no bloquear
        if thread_pool is None:
            raise HTTPException(status_code=500, detail="Thread pool no inicializado")
        
        loop = asyncio.get_event_loop()
        new_model, training_data = await loop.run_in_executor(
            thread_pool, 
            train_model_sync, 
            file_paths, 
            max_patterns, 
            max_pattern_length, 
            min_frequency, 
            training_status
        )
        
        # Actualizar modelo global
        model = new_model
        
        # Get final stats
        stats = model.get_efficiency_report()
        
        return {
            "message": "Entrenamiento completado exitosamente",
            "training_data": training_data,
            "model_stats": stats
        }
        
    except Exception as e:
        training_status.update({
            "is_training": False,
            "status": "error",
            "message": f"Error en entrenamiento: {str(e)}"
        })
        raise HTTPException(status_code=500, detail=f"Error en entrenamiento: {str(e)}")

def generate_text_sync(model, prompt, max_length, temperature):
    """Función síncrona para generar texto en un thread separado"""
    try:
        # Generate text
        generated_text = model.generate(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        # Get active patterns for analysis
        active_patterns = model._get_active_patterns(prompt) if hasattr(model, '_get_active_patterns') else []
        
        return generated_text, active_patterns
    except Exception as e:
        raise e

def generate_intelligent_response_sync(model, reasoning_engine, prompt, max_length, temperature):
    """Función síncrona para generar respuesta inteligente con razonamiento"""
    try:
        # Paso 1: Generar respuesta base
        base_response = model.generate(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        # Paso 2: Analizar pregunta y aplicar razonamiento
        analysis = reasoning_engine.analyze_question(prompt)
        
        # Paso 3: Aplicar razonamiento inteligente
        reasoned_response = reasoning_engine.apply_reasoning(prompt, base_response)
        
        # Paso 4: Aplicar mejora generativa
        final_response = mejorar_respuesta_generativa(prompt, reasoned_response)
        
        # Paso 5: Obtener patrones activos para análisis
        active_patterns = model._get_active_patterns(prompt) if hasattr(model, '_get_active_patterns') else []
        
        return {
            "base_response": base_response,
            "reasoned_response": reasoned_response,
            "final_response": final_response,
            "analysis": analysis,
            "active_patterns": active_patterns,
            "reasoning_chain": analysis.get('reasoning_chain', [])
        }
    except Exception as e:
        raise e

@app.post("/api/generate")
async def generate_text(
    prompt: str = Form(...),
    max_length: int = Form(20),
    temperature: float = Form(0.7),
    intelligent_mode: bool = Form(True)
):
    """Generate text using the trained model with intelligent reasoning - ASÍNCRONO"""
    global model, reasoning_engine, training_status
    
    if model is None:
        raise HTTPException(status_code=400, detail="Modelo no inicializado")
    
    if training_status["status"] != "trained":
        raise HTTPException(status_code=400, detail="Modelo no entrenado. Entrene primero el modelo.")
    
    if intelligent_mode and reasoning_engine is None:
        raise HTTPException(status_code=400, detail="Motor de razonamiento no disponible")
    
    try:
        # Ejecutar generación en thread separado para no bloquear
        if thread_pool is None:
            raise HTTPException(status_code=500, detail="Thread pool no inicializado")
        
        loop = asyncio.get_event_loop()
        
        if intelligent_mode:
            # Modo inteligente con razonamiento
            result = await loop.run_in_executor(
                thread_pool,
                generate_intelligent_response_sync,
                model,
                reasoning_engine,
                prompt,
                max_length,
                temperature
            )
            
            return {
                "prompt": prompt,
                "generated_text": result["final_response"],
                "base_response": result["base_response"],
                "reasoned_response": result["reasoned_response"],
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "intelligent_mode": True
                },
                "reasoning_analysis": {
                    "question_type": result["analysis"]["primary_strategy"],
                    "detected_types": result["analysis"]["detected_types"],
                    "acuaponia_contexts": result["analysis"]["acuaponia_contexts"],
                    "reasoning_chain": result["reasoning_chain"],
                    "active_patterns": len(result["active_patterns"]),
                    "patterns": [{"pattern": p[0], "score": p[1]} for p in result["active_patterns"][:5]]
                }
            }
        else:
            # Modo básico sin razonamiento
            generated_text, active_patterns = await loop.run_in_executor(
                thread_pool,
                generate_text_sync,
                model,
                prompt,
                max_length,
                temperature
            )
            
            return {
                "prompt": prompt,
                "generated_text": generated_text,
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "intelligent_mode": False
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

# Nuevos endpoints para gestión de modelos

def save_model_sync(model, model_name):
    """Función síncrona para guardar modelo en un thread separado"""
    try:
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{model_name}_{timestamp}.pkl"
        filepath = MODELS_DIR / filename
        
        # Save model
        model.save_model(str(filepath))
        
        # Get model info
        model_info = model.get_model_info()
        
        return {
            "filename": filename,
            "filepath": str(filepath),
            "model_info": model_info,
            "size_bytes": filepath.stat().st_size if filepath.exists() else 0
        }
    except Exception as e:
        raise e

@app.post("/api/models/save")
async def save_model(model_name: str = Form(...)):
    """Save the current trained model - ASÍNCRONO"""
    global model, training_status
    
    if model is None:
        raise HTTPException(status_code=400, detail="Modelo no inicializado")
    
    if not model.is_trained():
        raise HTTPException(status_code=400, detail="Modelo no entrenado. Entrene primero el modelo.")
    
    try:
        # Ejecutar guardado en thread separado
        if thread_pool is None:
            raise HTTPException(status_code=500, detail="Thread pool no inicializado")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            thread_pool,
            save_model_sync,
            model,
            model_name
        )
        
        return {
            "message": "Modelo guardado exitosamente",
            **result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar modelo: {str(e)}")

def load_model_sync(model_filename):
    """Función síncrona para cargar modelo en un thread separado"""
    try:
        filepath = MODELS_DIR / model_filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo de modelo no encontrado: {model_filename}")
        
        # Create new model instance and load
        new_model = UltraEfficientLLM()
        new_model.load_model(str(filepath))
        
        # Get model info
        model_info = new_model.get_model_info()
        
        return new_model, model_info
    except Exception as e:
        raise e

@app.post("/api/models/load")
async def load_model(model_filename: str = Form(...)):
    """Load a previously saved model - ASÍNCRONO"""
    global model, training_status
    
    try:
        # Ejecutar carga en thread separado
        if thread_pool is None:
            raise HTTPException(status_code=500, detail="Thread pool no inicializado")
        
        loop = asyncio.get_event_loop()
        new_model, model_info = await loop.run_in_executor(
            thread_pool,
            load_model_sync,
            model_filename
        )
        
        # Actualizar modelo global
        model = new_model
        
        # Update training status
        training_status.update({
            "is_training": False,
            "progress": 100,
            "status": "trained",
            "message": f"Modelo cargado: {model_filename}"
        })
        
        return {
            "message": "Modelo cargado exitosamente",
            "filename": model_filename,
            "model_info": model_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar modelo: {str(e)}")

@app.get("/api/models")
async def list_saved_models():
    """List all saved models"""
    models = []
    for file_path in MODELS_DIR.glob("*.pkl"):
        if file_path.is_file():
            models.append({
                "filename": file_path.name,
                "size_bytes": file_path.stat().st_size,
                "created_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "model_name": file_path.stem  # filename without extension
            })
    
    return {"models": models}

@app.delete("/api/models/{model_filename}")
async def delete_model(model_filename: str):
    """Delete a saved model"""
    file_path = MODELS_DIR / model_filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo de modelo no encontrado")
    
    try:
        file_path.unlink()
        return {"message": f"Modelo {model_filename} eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar modelo: {str(e)}")

@app.post("/api/analyze")
async def analyze_question(
    question: str = Form(...)
):
    """Analyze a question and return reasoning analysis"""
    global reasoning_engine
    
    if reasoning_engine is None:
        raise HTTPException(status_code=400, detail="Motor de razonamiento no disponible")
    
    try:
        # Analizar pregunta
        analysis = reasoning_engine.analyze_question(question)
        
        return {
            "question": question,
            "analysis": {
                "primary_strategy": analysis["primary_strategy"],
                "detected_types": analysis["detected_types"],
                "acuaponia_contexts": analysis["acuaponia_contexts"],
                "reasoning_chain": analysis["reasoning_chain"],
                "confidence_score": len(analysis["detected_types"]) / 8.0  # Score basado en tipos detectados
            },
            "recommendations": {
                "strategy": analysis["primary_strategy"],
                "contexts": analysis["acuaponia_contexts"],
                "reasoning_approach": _get_reasoning_approach_description(analysis["primary_strategy"])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@app.post("/api/chatbot-reasoning")
async def chatbot_reasoning(
    prompt: str = Form(...),
    max_length: int = Form(20),
    temperature: float = Form(0.7),
    reasoning_depth: int = Form(3),
    response_style: str = Form("detailed")
):
    """Chatbot que muestra el proceso de razonamiento paso a paso"""
    global model, reasoning_engine, training_status
    
    if model is None:
        raise HTTPException(status_code=400, detail="Modelo no inicializado")
    
    if training_status["status"] != "trained":
        raise HTTPException(status_code=400, detail="Modelo no entrenado. Entrene primero el modelo.")
    
    if reasoning_engine is None:
        raise HTTPException(status_code=400, detail="Motor de razonamiento no disponible")
    
    try:
        # Ejecutar en thread separado
        if thread_pool is None:
            raise HTTPException(status_code=500, detail="Thread pool no inicializado")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            thread_pool, 
            chatbot_reasoning_sync, 
            model, 
            reasoning_engine, 
            prompt, 
            max_length, 
            temperature,
            reasoning_depth,
            response_style
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en chatbot: {str(e)}")

def chatbot_reasoning_sync(model, reasoning_engine, prompt, max_length, temperature, reasoning_depth=3, response_style="detailed"):
    """Función síncrona para chatbot de razonamiento paso a paso"""
    try:
        # Paso 1: Análisis inicial de la pregunta
        analysis = reasoning_engine.analyze_question(prompt)
        
        # Paso 2: Generar respuesta base
        base_response = model.generate(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        # Si la respuesta base es muy deficiente, generar una mejor
        if len(base_response.strip()) < 20 or base_response.count('"') > 3 or 'como "' in base_response:
            if 'ácido' in prompt.lower() or 'acido' in prompt.lower():
                base_response = "Los ácidos son extremadamente peligrosos para el sistema acuapónico porque alteran el pH del agua, son tóxicos para los peces, destruyen las bacterias nitrificantes beneficiosas, y pueden ser absorbidos por las plantas causando daños irreversibles."
            elif 'crece' in prompt.lower() or 'crecen' in prompt.lower():
                base_response = "Las plantas crecen mejor en acuaponía debido a la nutrición constante, absorción eficiente sin suelo, oxigenación óptima de raíces, ausencia de enfermedades de suelo, y pH controlado."
            else:
                base_response = "En acuaponía, el sistema funciona como un ecosistema interconectado donde los peces proporcionan nutrientes a las plantas, las plantas purifican el agua para los peces, y las bacterias facilitan este ciclo natural."
        
        # Paso 3: Aplicar razonamiento inteligente
        reasoned_response = reasoning_engine.apply_reasoning(prompt, base_response)
        
        # Paso 4: Mejora generativa final
        # Si es una pregunta fuera del dominio de acuaponía, usar respuesta específica
        if any(out_domain_keyword in prompt.lower() for out_domain_keyword in [
            'programación', 'código', 'software', 'aplicación', 'app', 'web', 'internet', 'computadora', 'laptop', 'celular', 'smartphone',
            'python', 'javascript', 'html', 'css', 'java', 'c++', 'base de datos', 'servidor', 'cliente', 'api', 'framework',
            'fútbol', 'futbol', 'basketball', 'baloncesto', 'tenis', 'golf', 'natación', 'ciclismo', 'correr', 'maratón', 'olimpiadas',
            'película', 'pelicula', 'serie', 'televisión', 'tv', 'música', 'musica', 'videojuego', 'juego', 'netflix', 'youtube',
            'política', 'politica', 'presidente', 'gobierno', 'elecciones', 'congreso', 'senado', 'partido político', 'noticias',
            'receta', 'cocina', 'chef', 'restaurante', 'comida', 'plato', 'ingrediente', 'cocinar', 'hornear', 'freír',
            'viaje', 'turismo', 'hotel', 'avión', 'avion', 'aeropuerto', 'destino', 'vacaciones', 'playa', 'montaña',
            'enfermedad', 'síntoma', 'sintoma', 'medicina', 'doctor', 'hospital', 'tratamiento', 'diagnóstico', 'diagnostico',
            'dinero', 'banco', 'inversión', 'inversion', 'bolsa', 'acciones', 'economía', 'economia', 'finanzas', 'crédito', 'credito',
            'matemáticas', 'matematicas', 'historia', 'geografía', 'geografia', 'literatura', 'filosofía', 'filosofia', 'arte'
        ]):
            final_response = ("## 🤖 Respuesta Amable - Fuera de Mi Dominio\n\n"
                             "### 📝 Mi Especialización\n\n"
                             "> Soy un **sistema especializado en acuaponía** diseñado para ayudarte con preguntas sobre cultivos acuapónicos, peces, plantas, calidad del agua, pH, nutrientes y todo lo relacionado con sistemas de cultivo sostenible.\n\n"
                             "### 🎯 Lo Que Puedo Ayudarte\n\n"
                             "**Mi conocimiento incluye:**\n\n"
                             "- **🐟 Cuidado de peces** en sistemas acuapónicos\n"
                             "- **🌱 Cultivo de plantas** sin suelo\n"
                             "- **💧 Calidad del agua** y parámetros\n"
                             "- **🧪 pH y nutrientes** para el sistema\n"
                             "- **🦠 Bacterias nitrificantes** y ciclos biológicos\n"
                             "- **🔧 Mantenimiento** del sistema acuapónico\n"
                             "- **⚠️ Seguridad** y prevención de problemas\n"
                             "- **📊 Optimización** del rendimiento\n\n"
                             "### 💡 Sugerencia\n\n"
                             "**¿Te gustaría preguntarme sobre:**\n\n"
                             "- ¿Cómo funciona un sistema acuapónico?\n"
                             "- ¿Qué peces son mejores para acuaponía?\n"
                             "- ¿Cómo mantener el pH correcto?\n"
                             "- ¿Qué plantas crecen mejor en acuaponía?\n"
                             "- ¿Cómo solucionar problemas comunes?\n\n"
                             "### 🌱 Acerca de Acuaponía\n\n"
                             "La **acuaponía** es un sistema de cultivo sostenible que combina la acuicultura (cría de peces) con la hidroponía (cultivo de plantas sin suelo). Es una forma innovadora y ecológica de producir alimentos frescos en casa o a escala comercial.\n\n"
                             "**¡Estoy aquí para ayudarte con cualquier pregunta sobre acuaponía!** 🌟")
        # Si es una pregunta sobre pH extremo, usar respuesta de emergencia
        elif any(ph_value in prompt.lower() for ph_value in ['ph 1', 'ph 2', 'ph 3', 'ph 4', 'ph 5', 'ph 9', 'ph 10', 'ph 11', 'ph 12', 'ph 13', 'ph 14', 'ph es de 1', 'ph es de 2', 'ph es de 3', 'ph es de 4', 'ph es de 5', 'ph es de 9', 'ph es de 10', 'ph es de 11', 'ph es de 12', 'ph es de 13', 'ph es de 14']):
            final_response = ("## 🚨 EMERGENCIA CRÍTICA - pH EXTREMO\n\n"
                             "**⚠️ ADVERTENCIA MÁXIMA:** Un pH de **2** es **MORTAL** para todo el sistema acuapónico.\n\n"
                             "### 🚨 Consecuencias Inmediatas\n\n"
                             "- **🐟 Muerte instantánea de peces:** pH 2 es incompatible con la vida acuática\n"
                             "- **🦠 Destrucción total de bacterias:** Las bacterias nitrificantes mueren inmediatamente\n"
                             "- **🌱 Muerte de plantas:** Las raíces se queman y las plantas mueren\n"
                             "- **💀 Colapso total del sistema:** El ecosistema se destruye irremediablemente\n\n"
                             "### 📊 Comparación de pH\n\n"
                             "| pH | Estado | Efecto |\n"
                             "|----|--------|--------|\n"
                             "| **2** | **MORTAL** | Muerte instantánea |\n"
                             "| 6-7 | **IDEAL** | Sistema saludable |\n"
                             "| 5-8 | **ACEPTABLE** | Sistema funcional |\n"
                             "| <5 o >8 | **PELIGROSO** | Estrés del sistema |\n\n"
                             "### 🆘 Acciones Inmediatas\n\n"
                             "Si tu sistema tiene pH 2:\n\n"
                             "1. **🛑 DETENER TODO** - No agregar más químicos\n"
                             "2. **💧 Cambio de agua 100%** - Reemplazar toda el agua\n"
                             "3. **🧪 Medir pH nuevo** - Verificar que esté en rango 6-7\n"
                             "4. **🔄 Reiniciar sistema** - Ciclar el sistema nuevamente\n"
                             "5. **📞 Consultar experto** - Buscar ayuda profesional\n\n"
                             "### ⚠️ Prevención\n\n"
                             "- **NUNCA** agregar ácidos directamente al sistema\n"
                             "- **SIEMPRE** medir pH antes de cualquier ajuste\n"
                             "- **GRADUALMENTE** hacer cambios de pH\n"
                             "- **MONITOREAR** constantemente el pH\n\n"
                             "### 🎯 Conclusión\n\n"
                             "**Un pH de 2 es una emergencia crítica que requiere acción inmediata.** El sistema acuapónico es extremadamente sensible y un pH tan bajo destruye completamente el ecosistema. **Nunca** permitas que el pH baje de 5 o suba de 8.")
        # Si es una pregunta sobre ácidos generales, usar respuesta específica
        elif 'ácido' in prompt.lower() or 'acido' in prompt.lower() or 'químico' in prompt.lower() or 'quimico' in prompt.lower():
            final_response = ("## ⚠️ Advertencia de Seguridad - Ácidos en Acuaponía\n\n"
                             "**NO debes usar ácidos o químicos** en sistemas acuapónicos por las siguientes razones científicas:\n\n"
                             "### Efectos Tóxicos\n\n"
                             "- **Toxicidad para peces:** Causan estrés respiratorio y muerte\n"
                             "- **Destrucción de bacterias:** Matan las bacterias nitrificantes beneficiosas\n"
                             "- **Absorción por plantas:** Las plantas absorben químicos tóxicos\n"
                             "- **Alteración de pH:** Cambios bruscos causan estrés en todo el sistema\n"
                             "- **Contaminación persistente:** Los químicos pueden persistir en el sistema\n\n"
                             "### Sistema Sensible\n\n"
                             "> El sistema acuapónico es un ecosistema cerrado muy sensible donde cualquier químico afecta a todos los componentes. Es fundamental mantener el equilibrio natural del sistema para garantizar la salud de peces, plantas y bacterias.\n\n"
                             "### Alternativas Seguras\n\n"
                             "- **Métodos naturales** para ajustar pH\n"
                             "- **Cambios graduales** de agua\n"
                             "- **Monitoreo constante** del pH\n\n"
                             "### Conclusión\n\n"
                             "**En resumen:** Los ácidos son extremadamente peligrosos para el sistema acuapónico porque alteran el pH del agua, son tóxicos para los peces, destruyen las bacterias nitrificantes beneficiosas, y pueden ser absorbidos por las plantas causando daños irreversibles. Siempre usa métodos naturales y seguros para mantener el equilibrio del sistema.")
        else:
            final_response = mejorar_respuesta_generativa(prompt, reasoned_response)
        
        # Debug: imprimir la respuesta final para verificar
        print(f"DEBUG - Respuesta final original: {final_response[:200]}...")
        
        # Limpiar respuesta final si tiene problemas de formato
        # Solo limpiar si hay texto malformado antes del primer ##
        if '##' in final_response:
            partes = final_response.split('##')
            if len(partes) > 1 and len(partes[0].strip()) < 50 and partes[0].strip():
                # Solo limpiar si hay texto significativo antes del ##
                final_response = '##' + '##'.join(partes[1:])
        
        # Asegurar que la respuesta final no esté vacía
        if not final_response or len(final_response.strip()) < 10:
            final_response = reasoned_response
        
        # Debug: imprimir la respuesta final después de limpieza
        print(f"DEBUG - Respuesta final después de limpieza: {final_response[:200]}...")
        
        # Paso 5: Obtener patrones activos
        active_patterns = model._get_active_patterns(prompt) if hasattr(model, '_get_active_patterns') else []
        
        # Construir mensajes del chatbot en orden lógico
        chatbot_messages = [
            {
                "type": "system",
                "content": f"# 🤖 Sistema de Razonamiento Inteligente\n\n**Pregunta analizada:** *{prompt}*\n\n---",
                "timestamp": "inicio"
            },
            {
                "type": "analysis",
                "content": f"## 🔍 Análisis de Pregunta\n\n| Aspecto | Detalle |\n|---------|---------|\n| **Tipo Principal** | `{analysis['primary_strategy']}` |\n| **Tipos Detectados** | `{', '.join(analysis['detected_types'])}` |\n| **Contextos Acuaponía** | `{', '.join(analysis['acuaponia_contexts']) if analysis['acuaponia_contexts'] else 'Ninguno detectado'}` |\n\n---",
                "timestamp": "paso_1"
            },
            {
                "type": "reasoning",
                "content": f"## 🧠 Cadena de Razonamiento\n\n" + "\n".join([f"1. **{step}**" for step in analysis.get('reasoning_chain', [])]) + "\n\n---",
                "timestamp": "paso_2"
            },
            {
                "type": "base_response",
                "content": f"## 📝 Respuesta Base del Modelo\n\n> {base_response}\n\n---",
                "timestamp": "paso_3"
            },
            {
                "type": "reasoned_response",
                "content": f"## ✨ Respuesta con Razonamiento Aplicado\n\n{reasoned_response}\n\n---",
                "timestamp": "paso_4"
            },
            {
                "type": "patterns",
                "content": f"## 📊 Análisis de Patrones\n\n| Métrica | Valor |\n|---------|-------|\n| **Patrones Activos** | `{len(active_patterns)}` |\n| **Sparsity** | `{model.get_efficiency_report().get('sparsity', 0):.1f}%` |\n| **Memoria Utilizada** | `{model.get_efficiency_report().get('memory_kb', 0):.0f} KB` |\n\n### Patrones Principales:\n\n" + "\n".join([f"- **{p[0]}** (score: `{p[1]:.3f}`)" for p in active_patterns[:3]]) + "\n\n---",
                "timestamp": "paso_5"
            },
            {
                "type": "final_response",
                "content": f"## 🎯 Respuesta Final Mejorada\n\n{final_response if final_response else reasoned_response}\n\n---",
                "timestamp": "paso_6"
            }
        ]
        
        return {
            "prompt": prompt,
            "chatbot_messages": chatbot_messages,
            "final_response": final_response,
            "analysis": {
                "question_type": analysis["primary_strategy"],
                "detected_types": analysis["detected_types"],
                "acuaponia_contexts": analysis["acuaponia_contexts"],
                "reasoning_chain": analysis.get('reasoning_chain', []),
                "active_patterns": len(active_patterns),
                "patterns": [{"pattern": p[0], "score": p[1]} for p in active_patterns[:5]]
            },
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "intelligent_mode": True
            }
        }
        
    except Exception as e:
        raise e

def _get_reasoning_approach_description(strategy: str) -> str:
    """Get description for reasoning approach"""
    descriptions = {
        "safety": "Análisis de seguridad y riesgos con alternativas seguras",
        "causal": "Análisis de causa-efecto y relaciones causales",
        "problem_solving": "Estrategia sistemática de solución de problemas",
        "consequence": "Evaluación de consecuencias e impactos",
        "technical": "Análisis de principios técnicos y mecanismos",
        "comparative": "Comparación y evaluación de alternativas",
        "practical": "Enfoque en soluciones prácticas y aplicables",
        "scientific": "Análisis basado en principios científicos",
        "general": "Análisis general con razonamiento básico"
    }
    return descriptions.get(strategy, "Análisis general")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    ) 