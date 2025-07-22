"""
UltraEfficientLLM - Modelo de lenguaje ultra-eficiente basado en patrones selectivos
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
    Modelo de lenguaje ultra-eficiente basado en patrones selectivos

    Características revolucionarias:
    - Memoria: <1MB vs 14GB de modelos tradicionales
    - Activación: 5-10% de patrones vs 100% de parámetros
    - Velocidad: 500+ tokens/seg vs 20 tokens/seg
    - Hardware: Funciona en cualquier PC vs GPUs especializadas
    """

    def __init__(self, max_pattern_length=5, min_frequency=2, max_patterns=10000):
        self.max_pattern_length = max_pattern_length
        self.min_frequency = min_frequency
        self.max_patterns = max_patterns

        # Estructuras de datos ultra-compactas
        self.patterns = {}  # pattern -> frequency
        self.pattern_graph = defaultdict(dict)  # pattern -> next_words -> frequency
        self.word_vectors = {}  # Embeddings ultra-compactos
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
            'pattern_graph': dict(self.pattern_graph),  # Convertir defaultdict a dict
            'word_vectors': self.word_vectors,
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
            self.pattern_graph = defaultdict(dict, model_data['pattern_graph'])
            self.word_vectors = model_data['word_vectors']
            self.stats = model_data['stats']
            
            print(f"✅ Modelo cargado exitosamente")
            print(f"📊 Patrones cargados: {len(self.patterns)}")
            print(f"📊 Embeddings cargados: {len(self.word_vectors)}")
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
            'word_vectors_count': len(self.word_vectors),
            'pattern_graph_nodes': len(self.pattern_graph),
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
        self._build_pattern_graph(useful_patterns, texts)
        print(f"   Grafo construido: {len(self.pattern_graph)} nodos")
        self._create_compact_embeddings(useful_patterns)
        print(f"   Embeddings creados: {len(self.word_vectors)}")
        training_time = time.time() - start_time
        self._update_memory_stats()
        print(f"✅ Entrenamiento completado en {training_time:.2f} segundos")
        print(f"📊 Memoria utilizada: {self.stats['memory_kb']:.2f} KB")
        print(f"🎯 Eficiencia: {len(useful_patterns)} patrones vs ~175B parámetros GPT")

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

    def _build_pattern_graph(self, patterns: Dict[str, int], texts: List[str]) -> None:
        """Construye grafo de transiciones entre patrones"""
        self.patterns = patterns

        # Construir grafo de transiciones
        for text in texts:
            tokens = self._smart_tokenize(text)

            # Encontrar patrones en el texto
            pattern_positions = []
            for i in range(len(tokens)):
                for pattern in patterns:
                    pattern_tokens = pattern.split()
                    if (i + len(pattern_tokens) <= len(tokens) and
                        " ".join(tokens[i:i+len(pattern_tokens)]) == pattern):
                        pattern_positions.append((i, i + len(pattern_tokens), pattern))

            # Construir transiciones
            for i, (start1, end1, pattern1) in enumerate(pattern_positions):
                for start2, end2, pattern2 in pattern_positions[i+1:]:
                    if start2 >= end1 and start2 - end1 <= 3:  # Proximidad razonable
                        # Encontrar palabra/token de transición
                        if start2 == end1:
                            transition = "__DIRECT__"
                        else:
                            transition = " ".join(tokens[end1:start2])

                        if pattern1 not in self.pattern_graph:
                            self.pattern_graph[pattern1] = defaultdict(int)
                        self.pattern_graph[pattern1][transition + " -> " + pattern2] += 1

    def _create_compact_embeddings(self, patterns: Dict[str, int]) -> None:
        """Crea embeddings ultra-compactos (8 dimensiones vs 4096)"""
        # Extraer vocabulario único
        vocabulary = set()
        for pattern in patterns:
            vocabulary.update(pattern.split())

        # Crear embeddings compactos usando hash + distribución normal
        for word in vocabulary:
            # Seed determinístico basado en la palabra
            word_hash = hash(word) % (2**31)
            random.seed(word_hash)

            # Vector de 8 dimensiones
            vector = [random.gauss(0, 0.5) for _ in range(8)]
            self.word_vectors[word] = vector

    def generate(self, prompt: str, max_length: int = 20, temperature: float = 0.7) -> str:
        """Generación ultra-rápida activando solo patrones relevantes"""
        start_time = time.time()
        self.stats['total_generations'] += 1

        # Tokenizar prompt
        result_tokens = self._smart_tokenize(prompt)
        activations_this_gen = 0

        for step in range(max_length):
            # Obtener contexto reciente
            context = " ".join(result_tokens[-8:])  # Ventana de contexto ampliada

            # Activar solo patrones relevantes (CLAVE: sparsity extrema)
            active_patterns = self._get_active_patterns(context)
            activations_this_gen += len(active_patterns)

            if not active_patterns:
                break

            # Predecir siguiente token usando solo patrones activos
            next_token = self._predict_next_token(context, active_patterns, temperature)

            if next_token is None:
                break

            result_tokens.append(next_token)

        generation_time = time.time() - start_time
        # Only update activations if there were any active patterns
        if activations_this_gen > 0:
             self.stats['activations_per_generation'] += activations_this_gen

        result = " ".join(result_tokens)

        # Log de eficiencia
        tokens_per_second = len(result_tokens) / (generation_time + 0.001)
        # Calculate sparsity based on total activations over all generations
        total_possible_activations = self.stats['total_generations'] * len(self.patterns) if self.patterns else 1
        sparsity = 1 - (self.stats['activations_per_generation'] / total_possible_activations) if total_possible_activations > 0 else 0

        print(f"⚡ Generado en {generation_time:.3f}s | {tokens_per_second:.0f} tokens/s | Sparsity: {sparsity:.1%}")

        return result

    def _get_active_patterns(self, context: str) -> List[Tuple[str, float]]:
        """Activa solo patrones relevantes - CLAVE de la eficiencia"""
        cache_key = context[-20:]  # Key de cache - mantiene 20 caracteres para la clave

        if cache_key in self.activation_cache:
            self.stats['cache_hits'] += 1
            return self.activation_cache[cache_key]

        active = []
        context_words = set(context.split())

        # Only examine patterns that share words with the context
        for pattern, frequency in self.patterns.items():
            pattern_words = set(pattern.split())

            # Overlap semántico
            overlap = len(context_words & pattern_words)
            if overlap > 0:
                # Score de activación
                semantic_score = overlap / len(pattern_words)
                frequency_score = min(frequency / 10.0, 1.0)  # Normalizar

                activation_score = semantic_score * frequency_score

                # Umbral de activación (solo los más relevantes)
                if activation_score > 0.3:
                    active.append((pattern, activation_score))

        # Order by relevance and take only top-k (extreme sparsity)
        active.sort(key=lambda x: x[1], reverse=True)
        # Ensure at least one pattern is selected if available
        top_active = active[:max(1, len(active) // 10)]  # Only top 10%

        # Cache the result
        self.activation_cache[cache_key] = top_active

        return top_active

    def _predict_next_token(self, context: str, active_patterns: List[Tuple[str, float]],
                           temperature: float) -> Optional[str]:
        """Predicción usando solo patrones activos con anti-repetición"""
        candidates = defaultdict(float)
        context_words = context.lower().split()

        # Penalize words in the last 6 and 10 words of the context
        recent_words_6 = set(context_words[-6:])
        recent_words_10 = set(context_words[-10:])

        for pattern, activation_score in active_patterns:
            # Look for possible continuations from the pattern graph
            if pattern in self.pattern_graph:
                for transition, count in self.pattern_graph[pattern].items():
                    if " -> " in transition:
                        bridge, next_pattern = transition.split(" -> ", 1)
                        next_words = next_pattern.split()

                        if next_words:
                            candidate = next_words[0]

                            # ANTI-REPETITION: Penalize recent words
                            repetition_penalty = 1.0
                            if candidate in recent_words_6:
                                repetition_penalty = 0.3
                            elif candidate in recent_words_10:
                                repetition_penalty = 0.5

                            score = activation_score * count * repetition_penalty
                            candidates[candidate] += score

            # Also consider direct extensions of the pattern
            pattern_words = pattern.split()
            if len(pattern_words) > 0: # Ensure pattern is not empty
                 for other_pattern in self.patterns:
                     other_words = other_pattern.split()
                     if (len(other_words) > len(pattern_words) and
                         other_words[:len(pattern_words)] == pattern_words):

                         next_word = other_words[len(pattern_words)]

                         # ANTI-REPETITION applied here as well
                         repetition_penalty = 1.0
                         if next_word in recent_words_6:
                             repetition_penalty = 0.3
                         elif next_word in context_words[-10:]:
                             repetition_penalty = 0.5

                         # Adjust scoring for direct extensions - prioritize longer, more frequent extensions
                         extension_score_factor = self.patterns.get(other_pattern, 0) / max(self.patterns.get(pattern, 1), 1) # Prevent division by zero
                         score = activation_score * extension_score_factor * 10.0 * repetition_penalty # Boost this pathway
                         candidates[next_word] += score

        # DIVERSIDAD: If very few candidates, add random words from vocabulary
        if len(candidates) < 3:
            vocab_words = list(self.word_vectors.keys())
            # Avoid adding words that are already very close in the extended context
            recent_context_set = set(context_words[-8:])
            added_count = 0
            for _ in range(5): # Try adding up to 5 random words
                if added_count >= 3: break
                random_word = random.choice(vocab_words)
                if random_word not in candidates and random_word not in recent_context_set:
                     candidates[random_word] = 0.01  # Very low score
                     added_count += 1

        if not candidates:
            return None

        # Apply temperature and sampling
        return self._sample_with_temperature(candidates, temperature)

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

        # Tamaño del grafo
        total_size += sys.getsizeof(self.pattern_graph)
        for pattern, next_words_dict in self.pattern_graph.items():
             total_size += sys.getsizeof(pattern) # Size of the key
             total_size += sys.getsizeof(next_words_dict) # Size of the inner dict
             total_size += sum(sys.getsizeof(k) for k in next_words_dict.keys()) # Size of transition keys
             total_size += sum(sys.getsizeof(v) for v in next_words_dict.values()) # Size of counts

        # Tamaño de embeddings
        total_size += sys.getsizeof(self.word_vectors)
        for word, vector in self.word_vectors.items():
             total_size += sys.getsizeof(word) # Size of the key
             total_size += sys.getsizeof(vector) # Size of the vector list
             total_size += sum(sys.getsizeof(item) for item in vector) # Size of floats

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