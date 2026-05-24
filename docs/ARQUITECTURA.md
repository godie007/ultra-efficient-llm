# Arquitectura

Descripción técnica de cómo funciona y se conecta el sistema. Para uso e instalación, ver el
[README principal](../README.md).

## Visión general

Tres capas que se apoyan unas en otras, de lo barato a lo potente. Cada capa expone la misma
interfaz mínima (`_smart_tokenize`, `next_token_distribution`, `generate`), de modo que el
evaluador y las capas superiores las pueden tratar de forma intercambiable.

```
                        consulta / prompt
                               │
        ┌──────────────────────┼───────────────────────┐
        │           Capa 3: Recuperación + RAG          │
        │  SemanticMemory  ──recupera ejemplos──►  prompt│
        │  (embeddings)        relevantes        few-shot│
        └──────────────────────┬───────────────────────┘
                               │ contexto enriquecido
        ┌──────────────────────┼───────────────────────┐
        │        Capa 2: Híbrido n-grama + neuronal      │
        │   P(w) = λ·P_ngrama(w) + (1−λ)·P_neuronal(w)   │
        └───────────┬───────────────────────┬───────────┘
                    │                        │
        ┌───────────┴──────────┐   ┌─────────┴───────────┐
        │ Capa 1: Motor n-grama│   │  NeuralBackbone      │
        │ índice + backoff      │   │  (distilgpt2, GPU)   │
        └──────────────────────┘   └─────────────────────┘
```

---

## Capa 1 — Motor n-grama (`src/ultra_efficient_llm.py`)

Modelo estadístico de n-gramas. Recall exacto y barato de lo visto; por sí solo **no generaliza**.

### Entrenamiento (`train`)
1. **Tokenización** (`_smart_tokenize`): minúsculas, preserva entidades, separa puntuación.
2. **Extracción de patrones en paralelo** (`_extract_smart_patterns_parallel`): cuenta n-gramas
   ponderados de longitud `1..max_pattern_length` usando `ProcessPoolExecutor`. La lógica de
   tokenización/peso está duplicada en la función a nivel de módulo `extract_patterns_chunk`
   porque los workers de Windows necesitan una función picklable de nivel superior.
3. **Filtrado por utilidad** (`_filter_by_utility`): conserva los `max_patterns` mejores por
   frecuencia × información mutua aproximada. Resultado en `self.patterns`.
4. **Índice de continuaciones** (`_build_ngram_index`): construye
   `self.ngram_index: contexto(tupla) → Counter(siguiente_token)` para longitudes de contexto
   `0..max_pattern_length-1`. El contexto vacío `()` es la distribución unigrama (nivel final de
   backoff). Coste **O(tokens × max_pattern_length)**, lineal.

### Inferencia (`_backoff_scores`, `generate`)
- **Backoff de n variable**: consulta el contexto más largo disponible y retrocede a contextos más
  cortos, ponderando cada nivel con un factor geométrico `_BACKOFF_FACTOR = 0.4`. El nivel unigrama
  garantiza cobertura. Coste **O(max_pattern_length)** por token (sublineal en nº de patrones).
- **`next_token_distribution(context)`**: normaliza los scores de backoff a una distribución de
  probabilidad. Es la interfaz que consumen el evaluador y la capa híbrida.
- **`generate`**: en cada paso obtiene los scores de backoff, aplica anti-repetición
  (`_penalize_and_sample`: penaliza tokens de las últimas 6/10 posiciones) y muestrea con
  temperatura (`_sample_with_temperature`, softmax con truco log-sum-exp).

### Estructuras y persistencia
- `self.patterns: dict[str, int]` — n-gramas útiles y su frecuencia (stats, display, save).
- `self.ngram_index: dict[tuple, Counter]` — el índice de continuaciones (núcleo de la inferencia).
- `save_model`/`load_model` — serializan `patterns` + `ngram_index` con pickle.

`_get_active_patterns` se mantiene **solo** para el panel de "patrones activos" de la app web y los
demos; la generación ya no lo usa.

---

## Capa 2 — Híbrido n-grama + neuronal (`src/hybrid.py`, `src/neural_backbone.py`)

Da generalización al motor n-grama interpolando su distribución con la de un modelo neuronal pequeño.

### `NeuralBackbone`
Envuelve un LM causal pequeño (distilgpt2 por defecto) con **importación perezosa** de
torch/transformers (el resto del proyecto funciona sin ellas). Detecta GPU automáticamente.
- `next_token_probs(context)` — softmax sobre el vocabulario BPE para el siguiente token (una pasada).
- `prob_of_word(probs, word)` — probabilidad aproximada de `word` como siguiente palabra (primer
  sub-token BPE de `" word"`); permite interpolar a nivel de palabra con el n-grama.
- `top_words(probs, k)` — top-k siguientes palabras (decodifica los tokens más probables).
- `generate_text(prompt, ...)` — continuación libre vía `model.generate` (usado por RAG).

### `HybridLLM`
Replica la interfaz de `UltraEfficientLLM`, así que entra directo en el evaluador.
- **Interpolación**: `P(w) = λ·P_ngrama(w) + (1−λ)·P_neuronal(w)` (λ por defecto 0.5).
- **Pool de candidatos**: palabras del n-grama ∪ top-k del neuronal (k≈40). El neuronal puede
  introducir palabras que el n-grama nunca vio (generalización); el n-grama refuerza las que sí vio.

---

## Capa 3 — Recuperación semántica + RAG (`src/semantic_memory.py`, `src/rag.py`)

Materializa "dar ejemplos y conectar conceptos con pocos datos".

### `SemanticMemory`
- Embeddings con **all-MiniLM-L6-v2 vía `transformers` + mean-pooling** (sin dependencia
  `sentence-transformers`), normalizados a norma 1.
- `add(textos)` — embebe y almacena.
- `retrieve(consulta, top_k)` — similitud coseno (producto punto, por estar normalizados) y
  devuelve los `top_k` ejemplos más cercanos. Recupera por **significado**, no por palabras.

### `RAGGenerator`
1. `retrieve` los ejemplos relevantes a la consulta.
2. `build_prompt` arma un prompt few-shot (`Knowledge: … / Question: … / Answer:`) con un
   system prompt profesional que pide responder solo con el conocimiento dado.
3. `backbone.generate_text` genera condicionado a esos ejemplos.

El conocimiento vive en la memoria, no en los pesos: añadir/quitar ejemplos no requiere reentrenar.

### Modelo de generación (calidad profesional)
`NeuralBackbone` autodetecta modelos instruidos (nombre con `instruct`/`chat`/`-it`) y usa su
plantilla de chat, lo que mejora mucho la calidad. Se elige con la variable de entorno `RAG_MODEL`
(por defecto `distilgpt2`; `Qwen/Qwen2.5-0.5B-Instruct` para respuestas profesionales en GPU de
consumo).

---

## Flujos de datos

**Generación híbrida (un token):**
```
contexto → n-grama: _backoff_scores ─┐
        → neuronal: next_token_probs ─┤→ interpolar λ → normalizar → muestrear → token
```

**RAG (una respuesta):**
```
consulta → SemanticMemory.retrieve → ejemplos → build_prompt → NeuralBackbone.generate_text → respuesta
```

---

## Evaluación (`src/evaluation.py`)

- `compute_perplexity(model, textos)` — funciona con cualquier modelo que exponga
  `_smart_tokenize` + `next_token_distribution` (cubre n-grama e híbrido).
- `measure_generation_speed(model, prompts)` — tokens/segundo reales.
- `compare_perplexities(ngram, backbone, textos, λ)` — perplejidad pointwise y justa de n-grama,
  neuronal e híbrido (una pasada neuronal por posición).

La **calidad** se mide con perplejidad, no con memoria ni "sparsity".

## Validación de calidad (`src/quality.py`, `data/corpus/`)

Sobre un corpus profesional (`knowledge_base.json`) y su set de evaluación (`qa_eval.json`, con
preguntas redactadas distinto a los documentos):
- `evaluate_retrieval` — precision@k, recall@k, hit rate y MRR: ¿la memoria trae los documentos
  correctos? Determinista, independiente del modelo de generación.
- `evaluate_answers` — similitud coseno entre la respuesta generada y una respuesta de referencia
  profesional (embeddings de MiniLM), con tasa de aprobados sobre un umbral.

La recuperación valida "conectar conceptos"; la similitud de respuesta es un proxy automatizable
de "calidad profesional". Esta última depende del modelo (`RAG_MODEL`).

---

## Decisiones de diseño

- **Backoff vs grafo de transiciones**: el índice de continuaciones + backoff es O(n) por token y
  produce una distribución de probabilidad válida; reemplazó a un grafo O(tokens×patrones) y a un
  escaneo lineal de todos los patrones por token.
- **Dependencias neuronales opcionales y perezosas**: el motor n-grama no requiere torch; el híbrido
  y RAG las importan solo al instanciarse (`requirements-neural.txt`).
- **Interfaz común**: `_smart_tokenize` + `next_token_distribution` + `generate` permite enchufar
  n-grama o híbrido al mismo evaluador sin cambios.
- **Conocimiento como datos**: RAG mantiene el conocimiento en ejemplos recuperables, no en pesos,
  para eficiencia en datos y actualización sin reentrenamiento.

---

## Aplicación web (`web_app/`)

FastAPI + React sobre el **motor n-grama** (no el híbrido ni RAG). Hay **dos backends divergentes**
(`main.py` y `simple_main.py`, no sincronizados); detalles en [CLAUDE.md](../CLAUDE.md).
