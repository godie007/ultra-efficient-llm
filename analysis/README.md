# Análisis (reportes históricos)

> ⚠️ **Todos los reportes de este directorio son históricos.** Documentan corridas y
> decisiones pasadas con el encuadre original del proyecto (n-gramas presentados como un
> "LLM revolucionario", comparaciones con GPT del tipo "13.6 MB vs 14 GB", "99.9 % de
> sparsity"). **Ese encuadre ya no es válido**: un modelo de n-gramas no es un LLM y no
> generaliza. Se conservan como registro, no como descripción del estado actual.
>
> Para la evaluación honesta y vigente, ver `src/evaluation.py` y el
> [README principal](../README.md).

## Archivos

- **final_analysis_report.md** — reporte final de la etapa n-grama (histórico).
- **large_training_analysis.md** — análisis de entrenamiento a gran escala (histórico).
- **llm_reasoning_summary.md** — resumen del demo de "razonamiento" (histórico).
- **email_generator_summary.md** — análisis del generador de emails (histórico).

## Métricas actuales

La calidad ahora se mide con **perplejidad** sobre texto no visto (no con "memoria" ni
"sparsity", que no dicen nada sobre calidad). Comparación n-grama vs neuronal vs híbrido:

```bash
PYTHONUTF8=1 python src/evaluation.py
```
