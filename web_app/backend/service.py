"""
Servicio del asistente RAG: encapsula el estado, la persistencia del corpus y la
orquestación de recuperación + generación. El backend HTTP (routes.py) es una capa fina
sobre este servicio.
"""

import csv
import io
import json
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from config import CORPUS_PATH, DEFAULT_MODEL, DEFAULT_TOP_K, MAX_NEW_TOKENS, ROOT, TEMPERATURE

sys.path.append(str(ROOT))

from src.neural_backbone import NeuralBackbone
from src.rag import RAGGenerator
from src.semantic_memory import SemanticMemory


class RAGService:
    """Mantiene las fuentes de conocimiento y responde consultas con RAG."""

    def __init__(self):
        self.documents: List[Dict[str, str]] = []
        self.domain: str = ""
        self.description: str = ""
        self.memory: Optional[SemanticMemory] = None
        self.rag: Optional[RAGGenerator] = None
        self.device: Optional[str] = None
        self.instruct: bool = False
        self._ready: bool = False

    # ------------------------- ciclo de vida -------------------------

    def ensure_ready(self) -> None:
        """Inicialización perezosa e idempotente (no depende del evento lifespan de ASGI)."""
        if self._ready:
            return
        self._load_corpus()
        print(f"🔌 Cargando modelo de embeddings y generación ({DEFAULT_MODEL})...")
        self.memory = SemanticMemory()
        self.memory.set_documents([doc["text"] for doc in self.documents])
        backbone = NeuralBackbone(DEFAULT_MODEL)
        self.rag = RAGGenerator(self.memory, backbone, top_k=DEFAULT_TOP_K)
        self.device = self.memory.device
        self.instruct = backbone.instruct
        self._ready = True
        print(f"✅ Asistente RAG listo | dispositivo: {self.device} | fuentes: {len(self.documents)}")

    # ------------------------- persistencia -------------------------

    def _load_corpus(self) -> None:
        if CORPUS_PATH.exists():
            data = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
            self.documents = data.get("documents", [])
            self.domain = data.get("domain", "")
            self.description = data.get("description", "")

    def _save_corpus(self) -> None:
        CORPUS_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {"domain": self.domain, "description": self.description, "documents": self.documents}
        CORPUS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _rebuild_memory(self) -> None:
        self.memory.set_documents([doc["text"] for doc in self.documents])

    def _find(self, source_id: str) -> Optional[Dict[str, str]]:
        return next((doc for doc in self.documents if doc["id"] == source_id), None)

    @staticmethod
    def _new_id() -> str:
        return f"doc-{uuid.uuid4().hex[:8]}"

    # ------------------------- operaciones -------------------------

    def health(self) -> Dict:
        return {
            "status": "ok",
            "model": DEFAULT_MODEL,
            "instruct": self.instruct,
            "device": self.device,
            "num_sources": len(self.documents),
        }

    def list_sources(self) -> Dict:
        return {"sources": self.documents, "domain": self.domain}

    def add_source(self, text: str) -> Dict[str, str]:
        document = {"id": self._new_id(), "text": text.strip()}
        self.documents.append(document)
        self._rebuild_memory()
        self._save_corpus()
        return document

    def update_source(self, source_id: str, text: str) -> Optional[Dict[str, str]]:
        document = self._find(source_id)
        if document is None:
            return None
        document["text"] = text.strip()
        self._rebuild_memory()
        self._save_corpus()
        return document

    def delete_source(self, source_id: str) -> bool:
        if self._find(source_id) is None:
            return False
        self.documents = [doc for doc in self.documents if doc["id"] != source_id]
        self._rebuild_memory()
        self._save_corpus()
        return True

    def add_many(self, texts: List[str]) -> List[Dict[str, str]]:
        added = [{"id": self._new_id(), "text": t} for t in texts]
        if added:
            self.documents.extend(added)
            self._rebuild_memory()
            self._save_corpus()
        return added

    @staticmethod
    def parse_upload(filename: str, content: str) -> List[str]:
        """Extrae documentos de un archivo subido (.json / .csv / .txt / .md)."""
        ext = Path(filename or "").suffix.lower()
        texts: List[str] = []
        if ext == ".json":
            data = json.loads(content)
            items = data.get("documents", []) if isinstance(data, dict) else data
            for item in items:
                text = item.get("text") if isinstance(item, dict) else str(item)
                if text and text.strip():
                    texts.append(text.strip())
        elif ext == ".csv":
            for row in csv.DictReader(io.StringIO(content)):
                text = row.get("text") or row.get("texto")
                if text and text.strip():
                    texts.append(text.strip())
        else:  # .txt / .md → un documento por párrafo
            texts = [p.strip() for p in content.split("\n\n") if p.strip()]
        return texts

    def chat(self, message: str, top_k: int = DEFAULT_TOP_K) -> Dict:
        self.rag.top_k = max(1, top_k)
        answer, retrieved = self.rag.generate(message, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE)
        id_by_text = {doc["text"]: doc["id"] for doc in self.documents}
        sources = [
            {"id": id_by_text.get(text), "text": text, "score": round(score, 4)}
            for text, score in retrieved
        ]
        return {"answer": answer, "sources": sources}


# Instancia única usada por las rutas.
service = RAGService()
