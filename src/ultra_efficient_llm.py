"""
UltraEfficientLLM - Motor de lenguaje basado en n-gramas con backoff de n variable.

NO es una red neuronal ni un LLM: es un modelo estadístico de n-gramas (índice de
continuaciones + backoff estilo Infini-gram). Recall exacto y barato sobre lo visto, pero
no generaliza. La generalización la aporta el componente neuronal del híbrido (ver
`hybrid.py`, `neural_backbone.py`) y los ejemplos recuperados por RAG (`semantic_memory.py`,
`rag.py`). La calidad se mide con perplejidad en `evaluation.py`.
"""

import re
import random
import time
import math
import sys
import pickle
import os
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
import concurrent.futures
import multiprocessing

# --- FUNCIONES AUXILIARES PARA PARALELISMO ---
def extract_patterns_chunk(chunk, max_pattern_length, min_frequency):
    import re
    from collections import defaultdict
    def smart_tokenize(text):
        text = re.sub(r'\b([A-Z][a-z]+(?:_[A-Z][a-z]+)*(?:\s+[A-Z][a-z]+(?:_[A-Z][a-z]+)*)*)\b', r'ENTITY_\1', text)
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())
        tokens = [token.replace('entity_', '').replace('_', ' ') for token in tokens]
        return [token for token in tokens if len(token) > 0]
    def has_semantic_value(pattern):
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = pattern.split()
        if len(words) == 1 and words[0] in stop_words:
            return False
        if re.match(r'^[^\w\s]+$', pattern):
            return False
        significant_words = [w for w in words if w not in stop_words and len(w) > 2]
        return len(significant_words) > 0
    def calculate_pattern_weight(tokens, start, length):
        base_weight = 1
        if start == 0 or start + length == len(tokens):
            base_weight += 1
        base_weight += length - 1
        context_start = max(0, start - 2)
        context_end = min(len(tokens), start + length + 2)
        context = " ".join(tokens[context_start:context_end])
        if any(keyword in context for keyword in ['machine', 'learning', 'artificial', 'intelligence']):
            base_weight += 2
        return base_weight
    patterns = defaultdict(int)
    for text in chunk:
        tokens = smart_tokenize(text)
        for n in range(1, max_pattern_length + 1):
            for i in range(len(tokens) - n + 1):
                pattern = " ".join(tokens[i:i+n])
                if has_semantic_value(pattern):
                    weight = calculate_pattern_weight(tokens, i, n)
                    patterns[pattern] += weight
    return dict(patterns)


class UltraEfficientLLM:
    """
    Motor de lenguaje basado en n-gramas con índice de continuaciones y backoff de n variable.

    Funcionamiento:
    - Entrenamiento: extrae n-gramas ponderados y construye un índice
      contexto -> Counter(siguiente_token) para longitudes 0..max_pattern_length-1.
    - Generación: backoff del contexto más largo visto al más corto, con descuento
      geométrico; el nivel unigrama garantiza cobertura. Consulta en tiempo sublineal.

    Límite fundamental: solo recombina lo visto; no generaliza a contextos nuevos. Úsalo como
    componente barato de un híbrido con un modelo neuronal (ver `hybrid.py`).
    """

    # Factor de descuento por nivel de backoff (estilo "stupid backoff", Brants et al. 2007):
    # los contextos más largos pesan más; los más cortos se descuentan geométricamente.
    _BACKOFF_FACTOR = 0.4

    def __init__(self, max_pattern_length=5, min_frequency=2, max_patterns=10000):
        self.max_pattern_length = max_pattern_length
        self.min_frequency = min_frequency
        self.max_patterns = max_patterns

        # Estructuras de datos ultra-compactas
        self.patterns = {}  # pattern -> frequency
        # Índice de continuaciones n-grama: contexto (tupla de tokens) -> Counter de siguientes tokens.
        # Permite predecir con backoff de n variable en tiempo sublineal, sin escanear todos los patrones.
        self.ngram_index = defaultdict(Counter)
        self.activation_cache = {}  # Cache inteligente

        # Estadísticas de eficiencia
        self.stats = {
            'patterns_stored': 0,
            'memory_kb': 0,
            'activations_per_generation': 0,
            'cache_hits': 0,
            'total_generations': 0
        }

    def save_model(self, filepath: str) -> None:
        """
        Guarda el modelo entrenado en un archivo
        
        Args:
            filepath: Ruta del archivo donde guardar el modelo
        """
        print(f"💾 Guardando modelo en: {filepath}")
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Datos del modelo a guardar
        model_data = {
            'max_pattern_length': self.max_pattern_length,
            'min_frequency': self.min_frequency,
            'max_patterns': self.max_patterns,
            'patterns': self.patterns,
            'ngram_index': {ctx: dict(counter) for ctx, counter in self.ngram_index.items()},
            'stats': self.stats
        }
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"✅ Modelo guardado exitosamente: {filepath}")
            
            # Mostrar tamaño del archivo
            file_size = os.path.getsize(filepath)
            print(f"📊 Tamaño del archivo: {file_size / 1024:.2f} KB")
            
        except Exception as e:
            print(f"❌ Error guardando modelo: {e}")
            raise

    def load_model(self, filepath: str) -> None:
        """
        Carga un modelo entrenado desde un archivo
        
        Args:
            filepath: Ruta del archivo del modelo a cargar
        """
        print(f"📂 Cargando modelo desde: {filepath}")
        
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restaurar datos del modelo
            self.max_pattern_length = model_data['max_pattern_length']
            self.min_frequency = model_data['min_frequency']
            self.max_patterns = model_data['max_patterns']
            self.patterns = model_data['patterns']
            self.ngram_index = defaultdict(
                Counter,
                {ctx: Counter(counter) for ctx, counter in model_data['ngram_index'].items()}
            )
            self.stats = model_data['stats']

            print(f"✅ Modelo cargado exitosamente")
            print(f"📊 Patrones cargados: {len(self.patterns)}")
            print(f"📊 Contextos n-grama: {len(self.ngram_index)}")
            print(f"📊 Memoria utilizada: {self.stats['memory_kb']:.2f} KB")
            
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {filepath}")
            raise
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise

    def is_trained(self) -> bool:
        """
        Verifica si el modelo está entrenado
        
        Returns:
            bool: True si el modelo tiene patrones entrenados
        """
        return len(self.patterns) > 0

    def get_model_info(self) -> Dict[str, any]:
        """
        Obtiene información del modelo
        
        Returns:
            Dict: Información del modelo
        """
        return {
            'is_trained': self.is_trained(),
            'patterns_count': len(self.patterns),
            'ngram_contexts': len(self.ngram_index),
            'memory_usage_kb': self.stats['memory_kb'],
            'max_pattern_length': self.max_pattern_length,
            'min_frequency': self.min_frequency,
            'max_patterns': self.max_patterns
        }

    def train(self, texts: List[str]) -> None:
        print("🚀 Iniciando entrenamiento ultra-eficiente (paralelizado real)...")
        start_time = time.time()
        all_patterns = self._extract_smart_patterns_parallel(texts)
        print(f"   Patrones extraídos: {len(all_patterns)}")
        useful_patterns = self._filter_by_utility(all_patterns)
        print(f"   Patrones útiles: {len(useful_patterns)}")
        self.patterns = useful_patterns
        self._build_ngram_index(texts)
        print(f"   Índice n-grama: {len(self.ngram_index)} contextos")
        training_time = time.time() - start_time
        self._update_memory_stats()
        print(f"✅ Entrenamiento completado en {training_time:.2f} segundos")
        print(f"📊 Memoria del índice: {self.stats['memory_kb']:.2f} KB")
        print(f"🎯 {len(useful_patterns)} patrones | {len(self.ngram_index)} contextos n-grama")

    def _extract_smart_patterns_parallel(self, texts: List[str]) -> Dict[str, int]:
        num_workers = min(multiprocessing.cpu_count(), 32)
        print(f"🧩 Extrayendo patrones usando {num_workers} núcleos...")
        chunk_size = max(1, len(texts) // num_workers)
        chunks = [texts[i:i+chunk_size] for i in range(0, len(texts), chunk_size)]
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(extract_patterns_chunk, chunk, self.max_pattern_length, self.min_frequency) for chunk in chunks]
            all_patterns = defaultdict(int)
            for future in concurrent.futures.as_completed(futures):
                partial = future.result()
                for k, v in partial.items():
                    all_patterns[k] += v
        return dict(all_patterns)

    def _smart_tokenize(self, text: str) -> List[str]:
        """Tokenización que preserva estructura semántica"""
        # Preservar entidades importantes
        text = re.sub(r'\b([A-Z][a-z]+(?:_[A-Z][a-z]+)*(?:\s+[A-Z][a-z]+(?:_[A-Z][a-z]+)*)*)\b', r'ENTITY_\1', text)

        # Tokenizar preservando patrones
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())

        # Restore entities, handling potential underscores
        tokens = [token.replace('entity_', '').replace('_', ' ') for token in tokens]

        return [token for token in tokens if len(token) > 0]

    def _has_semantic_value(self, pattern: str) -> bool:
        """Determina si un patrón tiene valor semántico real"""
        # Filtrar stop words aislados
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = pattern.split()

        if len(words) == 1 and words[0] in stop_words:
            return False

        # Filtrar solo puntuación
        if re.match(r'^[^\w\s]+$', pattern):
            return False

        # Debe tener al menos una palabra significativa
        significant_words = [w for w in words if w not in stop_words and len(w) > 2]
        return len(significant_words) > 0

    def _calculate_pattern_weight(self, tokens: List[str], start: int, length: int) -> int:
        """Calcula peso semántico de un patrón"""
        base_weight = 1

        # Peso por posición (inicio/final de oración más importante)
        if start == 0 or start + length == len(tokens):
            base_weight += 1

        # Peso por longitud (patrones más largos más valiosos)
        base_weight += length - 1

        # Peso por contexto (palabras importantes cerca)
        context_start = max(0, start - 2)
        context_end = min(len(tokens), start + length + 2)
        context = " ".join(tokens[context_start:context_end])

        if any(keyword in context for keyword in ['machine', 'learning', 'artificial', 'intelligence']):
            base_weight += 2

        return base_weight

    def _filter_by_utility(self, patterns: Dict[str, int]) -> Dict[str, int]:
        """Filtra patrones por utilidad predictiva"""
        # Filtro por frecuencia mínima
        frequent = {p: f for p, f in patterns.items() if f >= self.min_frequency}

        # Calcular utilidad (frecuencia * información mutua aproximada)
        utility_scores = {}
        for pattern, freq in frequent.items():
            words = pattern.split()

            # Información mutua aproximada
            if len(words) > 1:
                # P(último_palabra | contexto) vs P(última_palabra)
                context = " ".join(words[:-1])
                last_word = words[-1]

                context_patterns = [p for p in frequent.keys() if p.startswith(context)]
                context_freq = sum(frequent[p] for p in context_patterns)

                if context_freq > 0:
                    conditional_prob = freq / context_freq
                    utility = freq * conditional_prob
                else:
                    utility = freq
            else:
                utility = freq

            utility_scores[pattern] = utility

        # Seleccionar top patrones por utilidad
        sorted_patterns = sorted(utility_scores.items(), key=lambda x: x[1], reverse=True)
        selected = dict(sorted_patterns[:self.max_patterns])

        return selected

    def _build_ngram_index(self, texts: List[str]) -> None:
        """Construye el índice de continuaciones n-grama a partir del corpus completo.

        Para cada posición registra el siguiente token bajo cada contexto de longitud
        0..(max_pattern_length-1). El contexto vacío () es la distribución unigrama, que
        sirve como nivel final de backoff. Coste O(tokens × max_pattern_length): lineal,
        frente al O(tokens × patrones) del antiguo grafo de transiciones.
        """
        self.ngram_index = defaultdict(Counter)
        max_ctx = max(self.max_pattern_length - 1, 0)

        for text in texts:
            tokens = self._smart_tokenize(text)
            for i in range(len(tokens)):
                target = tokens[i]
                self.ngram_index[()][target] += 1  # unigrama (backoff final)
                for k in range(1, max_ctx + 1):
                    if i - k >= 0:
                        ctx = tuple(tokens[i - k:i])
                        self.ngram_index[ctx][target] += 1

    def _backoff_scores(self, context_tokens: List[str]) -> Dict[str, float]:
        """Distribución de continuaciones por backoff de n variable.

        Interpola los niveles de n disponibles dando más peso a los contextos más largos
        (factor geométrico `_BACKOFF_FACTOR`). El nivel unigrama garantiza cobertura
        siempre que algún token haya sido visto. Coste O(max_pattern_length) por consulta.
        """
        scores = defaultdict(float)
        upper = min(max(self.max_pattern_length - 1, 0), len(context_tokens))
        weight = 1.0
        for k in range(upper, -1, -1):
            ctx = tuple(context_tokens[len(context_tokens) - k:]) if k > 0 else ()
            counter = self.ngram_index.get(ctx)
            if counter:
                total = sum(counter.values())
                for token, count in counter.items():
                    scores[token] += weight * (count / total)
            weight *= self._BACKOFF_FACTOR
        return scores

    def _penalize_and_sample(self, scores: Dict[str, float], context_tokens: List[str],
                             temperature: float) -> Optional[str]:
        """Aplica anti-repetición y muestrea un token de la distribución dada."""
        if not scores:
            return None
        recent_6 = set(context_tokens[-6:])
        recent_10 = set(context_tokens[-10:])
        penalized = {}
        for candidate, score in scores.items():
            if candidate in recent_6:
                score *= 0.3
            elif candidate in recent_10:
                score *= 0.5
            penalized[candidate] = score
        return self._sample_with_temperature(penalized, temperature)

    def generate(self, prompt: str, max_length: int = 20, temperature: float = 0.7) -> str:
        """Generación ultra-rápida usando el índice n-grama con backoff de n variable."""
        start_time = time.time()
        self.stats['total_generations'] += 1

        result_tokens = self._smart_tokenize(prompt)
        activations_this_gen = 0

        # Asegurar que generamos al menos algunos tokens adicionales
        min_generated = max(3, max_length // 2)
        generated_count = 0
        max_ctx = max(self.max_pattern_length - 1, 1)

        for step in range(max_length):
            context_tokens = result_tokens[-max_ctx:]

            # Candidatos por backoff: solo se consideran los tokens realmente vistos
            # tras este contexto (activación dispersa real, no escaneo de todos los patrones).
            scores = self._backoff_scores(context_tokens)
            activations_this_gen += len(scores)

            if not scores:
                break

            next_token = self._penalize_and_sample(scores, context_tokens, temperature)
            if next_token is None:
                break

            result_tokens.append(next_token)
            generated_count += 1

        generation_time = time.time() - start_time
        if activations_this_gen > 0:
            self.stats['activations_per_generation'] += activations_this_gen

        result = " ".join(result_tokens)

        # Log de eficiencia: sparsity = fracción de candidatos NO considerados respecto al
        # total de tokens distintos del vocabulario (ahora es una medida real de la activación).
        tokens_per_second = len(result_tokens) / (generation_time + 0.001)
        vocab_size = len(self.ngram_index.get((), {})) or 1
        avg_candidates = activations_this_gen / max(generated_count, 1)
        sparsity = 1 - (avg_candidates / vocab_size)

        print(f"⚡ Generado en {generation_time:.3f}s | {tokens_per_second:.0f} tokens/s | Sparsity: {sparsity:.1%}")

        return result

    def _get_active_patterns(self, context: str) -> List[Tuple[str, float]]:
        """Activa solo patrones relevantes - CLAVE de la eficiencia"""
        cache_key = context[-20:]  # Key de cache - mantiene 20 caracteres para la clave

        if cache_key in self.activation_cache:
            self.stats['cache_hits'] += 1
            return self.activation_cache[cache_key]

        active = []
        context_words = set(context.lower().split())
        
        # Si no hay palabras en el contexto, usar el prompt completo
        if not context_words:
            context_words = set(context.lower().split())

        # Examinar patrones que comparten palabras con el contexto
        for pattern, frequency in self.patterns.items():
            pattern_words = set(pattern.lower().split())

            # Overlap semántico mejorado
            overlap = len(context_words & pattern_words)
            if overlap > 0:
                # Score de activación mejorado
                semantic_score = overlap / max(len(pattern_words), 1)
                frequency_score = min(frequency / 5.0, 1.0)  # Normalizar con umbral más bajo
                
                # Bonus para patrones que empiezan con palabras del contexto
                start_bonus = 1.0
                if pattern_words and context_words:
                    if list(pattern_words)[0] in context_words:
                        start_bonus = 2.0

                activation_score = semantic_score * frequency_score * start_bonus

                # Umbral de activación más bajo para mayor sensibilidad
                if activation_score > 0.1:  # Reducido de 0.3 a 0.1
                    active.append((pattern, activation_score))

        # Si no hay patrones activos, buscar patrones que contengan palabras similares
        if not active:
            for pattern, frequency in self.patterns.items():
                pattern_words = set(pattern.lower().split())
                
                # Buscar patrones que contengan palabras del contexto
                for context_word in context_words:
                    if any(context_word in pattern_word or pattern_word in context_word 
                           for pattern_word in pattern_words):
                        activation_score = min(frequency / 10.0, 1.0)
                        active.append((pattern, activation_score))
                        break

        # Ordenar por relevancia y tomar más patrones
        active.sort(key=lambda x: x[1], reverse=True)
        
        # Tomar más patrones para mejor generación
        top_active = active[:max(5, len(active) // 5)]  # Tomar más patrones

        # Cache the result
        self.activation_cache[cache_key] = top_active

        return top_active

    def next_token_distribution(self, context: str) -> Dict[str, float]:
        """Distribución de probabilidad normalizada del siguiente token dado el contexto.

        Usa el backoff de n variable sobre el índice n-grama. Sin penalizaciones ni
        aleatoriedad: representa lo que el modelo "cree" sobre la siguiente palabra.
        Devuelve {} si ningún token fue visto (el evaluador aplica un piso de probabilidad).
        """
        tokens = self._smart_tokenize(context)
        scores = self._backoff_scores(tokens)
        total = sum(scores.values())
        if total <= 0:
            return {}
        return {token: score / total for token, score in scores.items()}

    def _predict_next_token(self, context: str, temperature: float = 0.7) -> Optional[str]:
        """Predice el siguiente token (backoff + anti-repetición + muestreo)."""
        tokens = self._smart_tokenize(context)
        context_tokens = tokens[-max(self.max_pattern_length - 1, 1):]
        scores = self._backoff_scores(context_tokens)
        return self._penalize_and_sample(scores, context_tokens, temperature)

    def _sample_with_temperature(self, candidates: Dict[str, float], temperature: float) -> str:
        """Sampling con temperatura"""
        if not candidates:
            return None

        # Convert scores to probabilities
        scores = list(candidates.values())
        words = list(candidates.keys())

        # Apply temperature
        if temperature > 0:
            # Avoid overflow with very low temperatures or very high scores
            max_score = max(scores)
            # Use a more robust log-sum-exp trick for softmax to avoid overflow/underflow
            try:
                exp_scores = [math.exp((s - max_score) / temperature) for s in scores]
                sum_exp = sum(exp_scores)
                # Handle case where sum_exp is zero or very small due to extreme negative scores
                if sum_exp == 0:
                     # Fallback to picking the word with the highest score (after temperature scaling)
                     max_temp_score_index = scores.index(max(scores))
                     return words[max_temp_score_index]
                probabilities = [e / sum_exp for e in exp_scores]
            except OverflowError:
                # Handle cases where scores are too high after division by temperature
                print("Warning: Overflow during softmax calculation. Falling back to max probability.")
                # Fallback to simple max probability if softmax overflows
                max_score_val = max(scores)
                probabilities = [1.0 if s == max_score_val else 0.0 for s in scores]
                total = sum(probabilities)
                 # Normalize if multiple max scores exist
                if total > 0:
                    probabilities = [p / total for p in probabilities]
                else: # Should not happen if candidates is not empty, but as a safeguard
                     return random.choice(words)

        else: # Temperature 0 or less: argmax
            max_score = -float('inf')
            best_word = None
            for word, score in candidates.items():
                if score > max_score:
                    max_score = score
                    best_word = word
            # Fallback: If no positive score, return the first word (arbitrary) or handle appropriately
            return best_word if best_word is not None else list(candidates.keys())[0]

        # Sampling
        # Handle potential floating point issues with very small probabilities or sum not being exactly 1.0
        # Normalize probabilities to sum to 1.0 to avoid issues with random.choices
        total_prob = sum(probabilities)
        if total_prob > 0:
             probabilities = [p / total_prob for p in probabilities]
        else: # Should not happen if candidates is not empty, but as a safeguard
             return random.choice(words)

        # Use random.choices for more robust sampling
        chosen_word = random.choices(words, weights=probabilities, k=1)[0]
        return chosen_word

    def _update_memory_stats(self) -> None:
        """Actualiza estadísticas de memoria"""
        total_size = 0

        # Tamaño de patrones
        total_size += sys.getsizeof(self.patterns)
        total_size += sum(sys.getsizeof(p) for p in self.patterns.keys())
        total_size += sum(sys.getsizeof(f) for f in self.patterns.values())

        # Tamaño del índice n-grama
        total_size += sys.getsizeof(self.ngram_index)
        for ctx, counter in self.ngram_index.items():
             total_size += sys.getsizeof(ctx)
             total_size += sys.getsizeof(counter)
             total_size += sum(sys.getsizeof(k) for k in counter.keys())
             total_size += sum(sys.getsizeof(v) for v in counter.values())

        # Tamaño de cache (can be variable)
        total_size += sys.getsizeof(self.activation_cache)
        for key, value in self.activation_cache.items():
             total_size += sys.getsizeof(key)
             total_size += sys.getsizeof(value) # Size of the list of tuples
             total_size += sum(sys.getsizeof(t) + sys.getsizeof(t[0]) + sys.getsizeof(t[1]) for t in value) # Size of tuples and their contents

        self.stats['memory_kb'] = total_size / 1024
        self.stats['patterns_stored'] = len(self.patterns)

    def get_efficiency_report(self) -> Dict:
        """Genera reporte completo de eficiencia"""
        traditional_llm_memory = 14 * 1024 * 1024  # 14GB in KB
        memory_improvement = traditional_llm_memory / max(self.stats['memory_kb'], 1)

        # Calculate average activations per generation based on the accumulated total
        avg_activations = self.stats['activations_per_generation'] / self.stats['total_generations'] if self.stats['total_generations'] > 0 else 0
        sparsity = 1 - (avg_activations / max(len(self.patterns), 1)) if self.patterns else 0

        # Cache hit rate calculation
        cache_hit_rate = self.stats['cache_hits'] / self.stats['total_generations'] if self.stats['total_generations'] > 0 else 0

        return {
            'memory_kb': self.stats['memory_kb'],
            'memory_improvement_vs_traditional': f"{memory_improvement:.0f}x",
            'patterns_stored': self.stats['patterns_stored'],
            'sparsity_achieved': f"{sparsity:.1%}",
            'cache_hit_rate': f"{cache_hit_rate:.1%}",
            'activation_efficiency': f"{100 - (avg_activations/len(self.patterns)*100):.1f}%" if self.patterns and len(self.patterns) > 0 else "N/A",
            'average_activations_per_gen': f"{avg_activations:.2f}"
        } 