# Arquitectura

Asistente RAG: recuperación semántica + generación condicionada sobre fuentes de conocimiento.
Para uso e instalación, ver el [README principal](../README.md).

## Visión general

```
                 pregunta del usuario
                          │
        ┌─────────────────┴──────────────────┐
        │  SemanticMemory.retrieve(pregunta)  │   recupera las fuentes
        │  (embeddings MiniLM + coseno)       │   conceptualmente relevantes
        └─────────────────┬──────────────────┘
                          │ fuentes relevantes
        ┌─────────────────┴──────────────────┐
        │  RAGGenerator → NeuralBackbone      │   genera la respuesta
        │  prompt few-shot + system prompt    │   condicionada a esas fuentes
        └─────────────────┬──────────────────┘
                          │
                respuesta + fuentes usadas
```

El conocimiento vive en la memoria (fuentes), no en los pesos: añadir/quitar fuentes no requiere
reentrenar.

## Recuperación — `src/semantic_memory.py`

`SemanticMemory` embebe cada fuente con **all-MiniLM-L6-v2 vía `transformers` + mean-pooling**
(sin dependencia `sentence-transformers`), normaliza los vectores y recupera por **coseno**
(producto punto). Importación perezosa de torch/transformers; detecta GPU automáticamente.

- `add(textos)` — añade fuentes.
- `set_documents(textos)` / `clear()` — reconstruyen los embeddings **sin recargar el modelo**
  (lo usa el backend al editar o eliminar fuentes).
- `retrieve(consulta, top_k)` — devuelve las `top_k` fuentes más similares con su score.

## Generación — `src/neural_backbone.py`

`NeuralBackbone` envuelve un LM causal pequeño (Qwen2.5-0.5B-Instruct por defecto, configurable con
`RAG_MODEL`). Los modelos instruidos (nombre con `instruct`/`chat`/`-it`) se autodetectan y usan su
**plantilla de chat**, lo que produce respuestas profesionales. `generate_text(prompt, system=…)`
devuelve solo los tokens nuevos.

## Orquestación — `src/rag.py`

`RAGGenerator.generate(consulta)`:
1. `memory.retrieve` las fuentes relevantes.
2. `build_prompt` arma un prompt few-shot (`Knowledge: … / Question: … / Answer:`) con un system
   prompt profesional que pide responder solo con el conocimiento dado.
3. `backbone.generate_text` genera la respuesta. Devuelve `(respuesta, fuentes_recuperadas)`.

## Backend — `web_app/backend/main.py`

FastAPI. En el arranque carga el corpus y construye `SemanticMemory` + `NeuralBackbone` +
`RAGGenerator`. Estado en memoria, persistido en `data/corpus/knowledge_base.json` en cada cambio
(`rebuild_memory()` reembebe vía `set_documents`).

Endpoints:
- `GET /api/health` → modelo, dispositivo, nº de fuentes.
- `GET /api/sources` → lista de fuentes.
- `POST /api/sources` `{text}` → añade.
- `PUT /api/sources/{id}` `{text}` → edita.
- `DELETE /api/sources/{id}` → elimina.
- `POST /api/sources/upload` (multipart) → txt/md (por párrafos), csv/json.
- `POST /api/chat` `{message, top_k?}` → `{answer, sources:[{id,text,score}]}`.

## Frontend — `web_app/frontend/`

React 18 + Vite + TypeScript + Tailwind. Dos páginas: **Chat** (`pages/Chat.tsx`) y **Fuentes de
conocimiento** (`pages/KnowledgeSources.tsx`). Acceso a la API por `services/api.ts`
(`http://localhost:8000/api`, JSON; la subida usa multipart). Clases de estilo reutilizables en
`src/index.css`.

## Validación de calidad — `src/quality.py`, `data/corpus/`

Sobre `knowledge_base.json` y `qa_eval.json`:
- `evaluate_retrieval` — precision@k, recall@k, hit rate, MRR (determinista, independiente del modelo).
- `evaluate_answers` — similitud coseno entre la respuesta generada y una referencia profesional
  (depende del modelo `RAG_MODEL`).
