# UltraEfficientLLM — Asistente RAG

Asistente de chat **local y eficiente en datos** sobre fuentes de conocimiento personalizables.
La idea: le das ejemplos/documentos y el sistema *conecta conceptos* para responder, **sin
entrenar nada**. Añadir o quitar conocimiento es añadir o quitar fuentes.

## Cómo funciona

1. **Recuperación semántica** — tus fuentes se guardan como embeddings; ante una pregunta se
   recuperan las conceptualmente relevantes (aunque no compartan palabras).
2. **Generación condicionada** — un modelo neuronal pequeño (Qwen2.5-0.5B-Instruct por defecto)
   responde usando esas fuentes como contexto (RAG / few-shot).

Corre en local sobre tu GPU (p. ej. RTX 4060 Ti). Cambiar el conocimiento no requiere reentrenar.

## Calidad medida

Sobre el corpus de ejemplo (`data/corpus/`) y su set de evaluación:

| Métrica | Valor |
|---|---|
| Recuperación — hit rate | 1.00 |
| Recuperación — recall@3 | 0.80 |
| Respuesta — tasa de aprobados (Qwen2.5-0.5B-Instruct) | 80 % |

La recuperación (conectar conceptos) es sólida e independiente del modelo; la calidad de
respuesta sube con un modelo instruido. Todo con ~24 documentos y cero entrenamiento.

## Instalación

```bash
pip install -r requirements.txt
# Para GPU instala el build de torch con CUDA desde https://pytorch.org
```

El modelo de generación se descarga la primera vez (~1 GB para Qwen2.5-0.5B-Instruct).

> En Windows ejecuta con `PYTHONUTF8=1` (la consola cp1252 no imprime los emojis del log).

## Uso

**Backend** (API FastAPI):

```bash
RAG_MODEL=Qwen/Qwen2.5-0.5B-Instruct PYTHONUTF8=1 python web_app/backend/main.py
# http://localhost:8000  (docs en /api/docs)
```

**Frontend** (React + Vite):

```bash
cd web_app/frontend && npm install && npm run dev
# http://localhost:5173
```

En la UI: pestaña **Chat** para consultar y **Fuentes de conocimiento** para añadir, editar,
eliminar o subir documentos (`.txt`, `.md`, `.csv`, `.json`).

**Validación de calidad** (recuperación + similitud de respuesta vs referencia):

```bash
RAG_MODEL=Qwen/Qwen2.5-0.5B-Instruct PYTHONUTF8=1 python src/quality.py
```

**Tests** (opt-in, descargan modelos pequeños):

```bash
RUN_NEURAL_TESTS=1 PYTHONUTF8=1 python -m unittest discover -s tests
```

## Estructura

| Ruta | Rol |
|---|---|
| `src/semantic_memory.py` | Memoria de fuentes por embeddings (all-MiniLM-L6-v2) + recuperación por coseno. |
| `src/neural_backbone.py` | Modelo de generación pequeño (instruido); plantilla de chat autodetectada. |
| `src/rag.py` | `RAGGenerator`: recupera fuentes relevantes y genera condicionado a ellas. |
| `src/quality.py` | Validación: recuperación (precision/recall/MRR) y respuesta (similitud vs referencia). |
| `data/corpus/` | Corpus (`knowledge_base.json`) y set de evaluación (`qa_eval.json`). |
| `web_app/backend/main.py` | API FastAPI: CRUD de fuentes + chat. |
| `web_app/frontend/` | UI React: Chat y Fuentes de conocimiento. |

El modelo de generación se elige con `RAG_MODEL` (por defecto `Qwen/Qwen2.5-0.5B-Instruct`).
Detalle técnico en **[docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)**.

## Licencia

MIT. Ver [LICENSE](LICENSE).
