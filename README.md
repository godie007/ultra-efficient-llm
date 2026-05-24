# UltraEfficientLLM

Proyecto de investigación sobre **generación de lenguaje eficiente y con pocos datos**.
La meta: dar ejemplos al sistema y que *conecte conceptos* sin entrenar un modelo gigante,
optimizando entrenamiento, velocidad de respuesta y cantidad de datos necesarios.

> ⚠️ **Nota honesta sobre el origen del proyecto.** Empezó como un "LLM ultra-eficiente"
> basado en n-gramas con afirmaciones de marketing (13.6 MB vs 14 GB de GPT, 99.9 % de
> sparsity, "razonamiento transparente"). Tras una evaluación técnica, la conclusión fue
> clara: **un modelo de n-gramas no es un LLM y no generaliza** (es la tecnología dominante
> de los años 90, abandonada por sus límites: dispersión de datos, cero generalización
> semántica, sin dependencias de largo alcance). Las viejas comparaciones contra GPT eran
> inválidas porque comparaban una tabla de n-gramas con un transformer de 175 000 M de
> parámetros. El proyecto se reorientó hacia algo que **sí** tiene respaldo técnico.

## Qué es ahora

Una arquitectura híbrida en tres capas, de lo barato a lo potente:

1. **Motor n-grama** (`src/ultra_efficient_llm.py`) — índice de continuaciones con *backoff*
   de n variable (estilo Infini-gram). Recall exacto y barato sobre lo visto, en tiempo
   sublineal. Solo, no generaliza.
2. **Híbrido n-grama + neuronal** (`src/hybrid.py`, `src/neural_backbone.py`) — interpola la
   distribución del n-grama con la de un modelo neuronal pequeño (distilgpt2 por defecto).
   El n-grama aporta recall exacto; el neuronal, generalización.
3. **Recuperación semántica + RAG** (`src/semantic_memory.py`, `src/rag.py`) — guarda ejemplos
   como embeddings y recupera los conceptualmente relevantes a una consulta (aunque no
   compartan palabras); se los pasa al modelo en contexto (*few-shot*). Añadir o quitar
   conocimiento = añadir o quitar ejemplos, **sin reentrenar**.

## Resultados medidos (honestos)

Perplejidad sobre **texto no visto** (más baja = mejor):

| Modelo | Perplejidad |
|---|---|
| N-grama solo | ~413 000 (no generaliza) |
| Neuronal solo (distilgpt2) | ~194 |
| **Híbrido n-grama + neuronal** | **~99** ✅ mejor que cualquiera de los dos |

Esto reproduce el resultado de Infini-gram (2024): interpolar n-gramas con un LM neuronal
reduce la perplejidad. La recuperación semántica conecta consultas con ejemplos relevantes
**sin solapamiento léxico** (p. ej. "How do machines learn?" → ejemplos de redes neuronales).

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

# Evaluación honesta: perplejidad, velocidad y comparación n-grama vs neuronal vs híbrido
PYTHONUTF8=1 python src/evaluation.py

# Demo de recuperación semántica + generación few-shot (RAG)
PYTHONUTF8=1 python src/rag.py

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
| `src/evaluation.py` | Métricas reales: perplejidad, velocidad, comparación de modelos. |
| `src/neural_backbone.py` | Modelo neuronal pequeño (distilgpt2) — distribución del siguiente token y generación. |
| `src/hybrid.py` | `HybridLLM`: interpola n-grama + neuronal. |
| `src/semantic_memory.py` | Memoria de ejemplos por embeddings (all-MiniLM-L6-v2) + recuperación por coseno. |
| `src/rag.py` | `RAGGenerator`: recupera ejemplos relevantes y genera condicionado a ellos. |
| `src/data_processor.py`, `src/utils.py` | Descarga/limpieza de corpus y utilidades. |
| `web_app/` | API FastAPI + frontend React sobre el motor n-grama. |

## Estado y próximos pasos

- El cuello de botella de calidad es el modelo base (distilgpt2, mínimo). Cambiarlo por un
  modelo instruido pequeño (Qwen2.5-0.5B, Gemma) mejora mucho el *few-shot*.
- LoRA para adaptación a dominio en GPU (eficiencia de entrenamiento).
- Benchmark con corpus real y conjuntos de validación más grandes.

## Licencia

MIT. Ver [LICENSE](LICENSE).
