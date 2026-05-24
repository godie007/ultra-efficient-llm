# Demos

Demostraciones del **motor n-grama**. Ejecútalas desde la raíz del repo con `PYTHONUTF8=1`
en Windows.

## Archivos

- **reasoning_demo.py** — visualiza el proceso interno del motor n-grama (extracción de
  patrones, patrones activos, predicción paso a paso). `python demos/reasoning_demo.py --full`
- **large_training_demo.py** — entrenamiento con más datos y comparación entre tamaños de modelo.
- **simple_email_generator.py** — generador de correos basado en plantillas + el motor n-grama.

## Demos de la arquitectura actual (híbrido + RAG)

Estas viven en `src/` porque dependen del backbone neuronal opcional
(`pip install -r requirements-neural.txt`):

```bash
PYTHONUTF8=1 python src/evaluation.py   # perplejidad + comparación n-grama vs neuronal vs híbrido
PYTHONUTF8=1 python src/rag.py          # recuperación semántica + generación few-shot
```

## Nota

Los demos del motor n-grama muestran sus límites reales: genera recombinando lo visto y **no
generaliza**. La generación coherente requiere el componente neuronal (ver `src/hybrid.py`,
`src/rag.py`). Ver el [README principal](../README.md).
