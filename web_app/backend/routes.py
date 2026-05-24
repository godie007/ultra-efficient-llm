"""Rutas HTTP del asistente RAG (capa fina sobre RAGService)."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from schemas import ChatIn, SourceIn
from service import service

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    service.ensure_ready()
    return service.health()


@router.get("/sources")
def list_sources():
    service.ensure_ready()
    return service.list_sources()


@router.post("/sources")
def add_source(body: SourceIn):
    service.ensure_ready()
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    return service.add_source(body.text)


@router.put("/sources/{source_id}")
def update_source(source_id: str, body: SourceIn):
    service.ensure_ready()
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    document = service.update_source(source_id, body.text)
    if document is None:
        raise HTTPException(status_code=404, detail="Fuente no encontrada")
    return document


@router.delete("/sources/{source_id}")
def delete_source(source_id: str):
    service.ensure_ready()
    if not service.delete_source(source_id):
        raise HTTPException(status_code=404, detail="Fuente no encontrada")
    return {"deleted": source_id}


@router.post("/sources/upload")
async def upload_sources(file: UploadFile = File(...)):
    service.ensure_ready()
    content = (await file.read()).decode("utf-8", errors="ignore")
    texts = service.parse_upload(file.filename, content)
    added = service.add_many(texts)
    return {"added": len(added), "sources": added}


@router.post("/chat")
def chat(body: ChatIn):
    service.ensure_ready()
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    return service.chat(body.message, body.top_k)
