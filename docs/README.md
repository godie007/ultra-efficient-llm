# Documentación

Documentación técnica del proyecto.

## Archivos

- **ARQUITECTURA.md** — documentación técnica de la arquitectura: las tres capas (motor n-grama,
  híbrido neuronal, recuperación semántica/RAG), flujos de datos y decisiones de diseño. **Punto
  de partida recomendado.**
- **llm_reasoning_explanation.md** — explicación de los 4 pasos del **motor n-grama**
  (extracción → índice → activación/backoff → predicción). ⚠️ Documento histórico:
  conserva el encuadre original ("razonamiento", comparaciones con GPT) que ya no es
  exacto. Para el estado actual, ver el [README principal](../README.md).

## Dónde está la documentación actual

- **Descripción y uso del proyecto**: [../README.md](../README.md)
- **Arquitectura para desarrollo** (motor n-grama, híbrido neuronal, RAG, gotchas):
  [../CLAUDE.md](../CLAUDE.md)
- **Estructura de archivos**: [../PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)

## Contexto importante

El proyecto evolucionó de un modelo de n-gramas autónomo (que no generaliza) a una
arquitectura híbrida: motor n-grama (recall barato) + modelo neuronal pequeño
(generalización) + recuperación semántica de ejemplos (RAG). Las métricas honestas
(perplejidad, velocidad) están en `src/evaluation.py`.
