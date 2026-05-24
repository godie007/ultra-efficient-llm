# Outputs

Archivos de salida generados por los demos.

## Archivos

- **demo_emails.txt** — correos de ejemplo generados por `demos/simple_email_generator.py`.
- **correos_simples.txt** — correos en español con distintos tonos.

## Regeneración

```bash
python demos/simple_email_generator.py
```

## Nota sobre métricas

Versiones antiguas de estos docs interpretaban "sparsity 99.9 %" como señal de calidad. **No
lo es**: un modelo que devuelve ruido también tiene baja activación. La calidad real se mide
con **perplejidad** (`src/evaluation.py`). Ver el [README principal](../README.md).
