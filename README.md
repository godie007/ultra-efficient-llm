# UltraEfficientLLM

Proyecto de investigación sobre **generación de lenguaje eficiente y con pocos datos**.
La idea central: darle ejemplos al sistema y que *conecte conceptos* sin entrenar un modelo
gigante, optimizando tres ejes a la vez — **entrenamiento, velocidad de respuesta y cantidad
de datos necesarios**.

## Concepto

En lugar de un único modelo enorme, se combinan tres componentes, de lo barato a lo potente,
cada uno aportando lo que mejor hace:

1. **Motor n-grama** (`src/ultra_efficient_llm.py`) — índice de continuaciones con *backoff*
   de n variable (estilo Infini-gram). Recall exacto y barato sobre lo visto, en tiempo
   sublineal.
2. **Híbrido n-grama + neuronal** (`src/hybrid.py`, `src/neural_backbone.py`) — interpola la
   distribución del n-grama con la de un modelo neuronal pequeño (distilgpt2 por defecto):
   `P(w) = λ·P_ngrama(w) + (1−λ)·P_neuronal(w)`. El n-grama aporta recall exacto; el neuronal,
   generalización.
3. **Recuperación semántica + RAG** (`src/semantic_memory.py`, `src/rag.py`) — guarda ejemplos
   como embeddings y recupera los conceptualmente relevantes a una consulta (aunque no compartan
   palabras); se los pasa al modelo en contexto (*few-shot*). Añadir o quitar conocimiento =
   añadir o quitar ejemplos, **sin reentrenar** — la clave de la eficiencia en datos.

## Resultados medidos

Perplejidad sobre **texto no visto** (más baja = mejor):

| Modelo | Perplejidad |
|---|---|
| N-grama solo | ~413 000 |
| Neuronal solo (distilgpt2) | ~194 |
| **Híbrido n-grama + neuronal** | **~99** ✅ |

El híbrido supera a cualquiera de sus componentes por separado, reproduciendo el resultado de
Infini-gram (2024): interpolar n-gramas con un LM neuronal reduce la perplejidad. La
recuperación semántica conecta consultas con ejemplos relevantes **sin solapamiento léxico**
(p. ej. "How do machines learn?" → ejemplos de redes neuronales).

### Validación de calidad (asistente RAG)

Sobre un corpus profesional (`data/corpus/`) y su set de evaluación, midiendo recuperación y
calidad de respuesta (similitud semántica vs respuesta de referencia):

| Métrica | distilgpt2 | Qwen2.5-0.5B-Instruct |
|---|---|---|
| Recuperación — hit rate | 1.00 | 1.00 |
| Recuperación — recall@3 | 0.80 | 0.80 |
| Respuestas — similitud media | 0.41 | **0.59** |
| Respuestas — tasa de aprobados | 30 % | **80 %** |

La recuperación (la parte de "conectar conceptos") es sólida e independiente del modelo. La
calidad de respuesta sube mucho con un modelo instruido pequeño — todo **con 24 documentos y
sin entrenar**. Las respuestas con Qwen son profesionales y coherentes.

📐 Para el detalle técnico de cómo funciona y se conecta cada capa, ver
**[docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)**.

## Instalación

```bash
pip install -r requirements.txt            # base: solo el motor n-grama
pip install -r requirements-neural.txt     # opcional: híbrido + RAG (torch + transformers)
```

El motor n-grama funciona sin las dependencias neuronales. Para GPU (p. ej. RTX 4060 Ti),
instala el build de `torch` con CUDA desde https://pytorch.org. El backbone neuronal y la
memoria semántica detectan la GPU automáticamente.

> En Windows, ejecuta con `PYTHONUTF8=1` (la consola cp1252 no imprime los emojis del log):
> `PYTHONUTF8=1 python main.py --test`

## Uso

```bash
# Tests (los tests neuronales se omiten salvo RUN_NEURAL_TESTS=1)
PYTHONUTF8=1 python main.py --test
RUN_NEURAL_TESTS=1 PYTHONUTF8=1 python main.py --test   # incluye híbrido + RAG

# Evaluación: perplejidad, velocidad y comparación n-grama vs neuronal vs híbrido
PYTHONUTF8=1 python src/evaluation.py

# Demo de recuperación semántica + generación few-shot (RAG)
PYTHONUTF8=1 python src/rag.py

# Validación de calidad sobre el corpus profesional (recuperación + calidad de respuesta)
PYTHONUTF8=1 python src/quality.py
# Calidad profesional con un modelo instruido pequeño (se descarga la primera vez):
RAG_MODEL=Qwen/Qwen2.5-0.5B-Instruct PYTHONUTF8=1 python src/quality.py

# Demos del motor n-grama
python main.py                 # demo con libro (descarga Frankenstein)
python main.py --basic         # demo con textos de ejemplo
python main.py --interactive   # modo interactivo
```

Aplicación web (FastAPI + React) para entrenar/evaluar el motor n-grama:

```bash
cd web_app/backend && python start.py     # http://localhost:8000  (docs en /api/docs)
cd web_app/frontend && npm install && npm run dev   # http://localhost:5173
```

## Arquitectura del código

| Módulo | Rol |
|---|---|
| `src/ultra_efficient_llm.py` | Motor n-grama: extracción de patrones, índice de continuaciones, backoff, generación. |
| `src/evaluation.py` | Métricas: perplejidad, velocidad, comparación de modelos. |
| `src/neural_backbone.py` | Modelo neuronal pequeño (distilgpt2) — distribución del siguiente token y generación. |
| `src/hybrid.py` | `HybridLLM`: interpola n-grama + neuronal. |
| `src/semantic_memory.py` | Memoria de ejemplos por embeddings (all-MiniLM-L6-v2) + recuperación por coseno. |
| `src/rag.py` | `RAGGenerator`: recupera ejemplos relevantes y genera condicionado a ellos. |
| `src/quality.py` | Validación de calidad: recuperación (precision/recall/MRR) y respuesta (similitud vs referencia). |
| `data/corpus/` | Corpus profesional (`knowledge_base.json`) y set de evaluación (`qa_eval.json`). |
| `src/data_processor.py`, `src/utils.py` | Descarga/limpieza de corpus y utilidades. |
| `web_app/` | API FastAPI + frontend React sobre el motor n-grama. |

## Modelo de generación configurable

El backbone neuronal se elige con la variable `RAG_MODEL` (por defecto `distilgpt2`, ligero).
Para calidad profesional, usa un modelo instruido pequeño que corre en una GPU de consumo:

```bash
RAG_MODEL=Qwen/Qwen2.5-0.5B-Instruct PYTHONUTF8=1 python src/quality.py
```

Los modelos instruidos (nombre con `instruct`/`chat`/`-it`) se detectan automáticamente y usan
su plantilla de chat.

## Próximos pasos

- LoRA para adaptación a dominio en GPU (eficiencia de entrenamiento).
- Ampliar el corpus y el set de evaluación; benchmark con dominios adicionales.
- Probar modelos instruidos algo mayores (Qwen2.5-1.5B, Gemma) según el presupuesto de GPU.

## Licencia

MIT. Ver [LICENSE](LICENSE).
