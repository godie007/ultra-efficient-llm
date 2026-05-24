# Estructura del Proyecto UltraEfficientLLM

Visión general de los directorios y archivos, reflejando el estado actual del proyecto
(motor n-grama + híbrido neuronal + recuperación semántica/RAG). Para la descripción
funcional, ver [README.md](README.md); para guía de desarrollo, ver [CLAUDE.md](CLAUDE.md).

```
ultra-efficient-llm/
├── README.md                       # Descripción y uso (actual)
├── CLAUDE.md                       # Guía para Claude Code
├── PROJECT_STRUCTURE.md            # Este archivo
├── WEB_APP_STRUCTURE.md            # Estructura de la app web
├── requirements.txt                # Dependencias base (motor n-grama)
├── requirements-neural.txt         # Dependencias OPCIONALES (híbrido + RAG: torch, transformers)
├── setup.py                        # Empaquetado; extras: neural, dev, docs
├── main.py                         # Punto de entrada (demos, tests, inferencia)
│
├── src/                            # Código fuente principal
│   ├── ultra_efficient_llm.py      # Motor n-grama: índice de continuaciones + backoff
│   ├── evaluation.py               # Perplejidad, velocidad, comparación de modelos
│   ├── neural_backbone.py          # Modelo neuronal pequeño (distilgpt2), carga perezosa
│   ├── hybrid.py                   # HybridLLM: interpola n-grama + neuronal
│   ├── semantic_memory.py          # Memoria de ejemplos por embeddings (all-MiniLM-L6-v2)
│   ├── rag.py                      # RAGGenerator: recuperación + generación few-shot
│   ├── data_processor.py           # Descarga/limpieza de corpus (Project Gutenberg)
│   └── utils.py                    # Logging, timers, validación de parámetros
│
├── tests/
│   └── test_ultra_efficient_llm.py # Suite unittest (tests neuronales opt-in: RUN_NEURAL_TESTS=1)
│
├── demos/                          # Demostraciones del motor n-grama
│   ├── reasoning_demo.py
│   ├── large_training_demo.py
│   └── simple_email_generator.py
│
├── examples/                       # Ejemplos básicos (basic_demo.py, book_demo.py)
├── data/                           # Datos de prueba y notas (algunas históricas)
├── docs/                           # Documentación técnica (incluye reportes históricos)
├── analysis/                       # Reportes de análisis (históricos, ver banners)
├── outputs/                        # Salidas generadas por los demos
├── evaluation_reports/             # Métricas JSON de corridas pasadas (históricas)
│
└── web_app/                        # Aplicación web sobre el motor n-grama
    ├── start_app.py                # Lanza backend (simple_main) + frontend
    ├── backend/                    # FastAPI: main.py y simple_main.py (NO sincronizados)
    └── frontend/                   # React 18 + Vite + TypeScript + Tailwind
```

## Notas

- **Dependencias neuronales opcionales**: el motor n-grama base no requiere torch/transformers;
  solo el híbrido (`hybrid.py`, `neural_backbone.py`) y RAG (`semantic_memory.py`, `rag.py`) los usan,
  con importación perezosa.
- **Dos backends web divergentes**: `web_app/backend/main.py` (split por línea, lanzado por
  `start.py`) y `simple_main.py` (split por párrafo + CSV, lanzado por `start_app.py`). Ver CLAUDE.md.
- **Reportes históricos**: los archivos en `analysis/`, `evaluation_reports/`, parte de `docs/` y
  `data/INSTRUCCIONES_FINALES.md` describen corridas/decisiones pasadas con el encuadre antiguo
  (comparaciones con GPT). Llevan un aviso al inicio y se conservan como registro.
