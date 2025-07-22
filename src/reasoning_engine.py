#!/usr/bin/env python3
"""
🧠 MOTOR DE RAZONAMIENTO ESTRATÉGICO - ULTRAEFFICIENTLLM
========================================================

Sistema que analiza preguntas y aplica estrategias de razonamiento específicas.
"""

import re
import random
from typing import Dict, List, Tuple, Optional

class ReasoningEngine:
    """Motor de razonamiento estratégico para análisis de preguntas"""
    
    def __init__(self):
        self.reasoning_strategies = {
            'causal': self._apply_causal_reasoning,
            'comparative': self._apply_comparative_reasoning,
            'problem_solving': self._apply_problem_solving_reasoning,
            'safety': self._apply_safety_reasoning,
            'technical': self._apply_technical_reasoning,
            'practical': self._apply_practical_reasoning,
            'scientific': self._apply_scientific_reasoning,
            'consequence': self._apply_consequence_reasoning,
            'out_of_domain': self._apply_out_of_domain_reasoning
        }
        
        # Patrones de detección de tipo de pregunta
        self.question_patterns = {
            'causal': [
                r'por qué', r'qué causa', r'cuál es la razón', r'por qué motivo',
                r'qué hace que', r'cómo es que', r'por qué razón'
            ],
            'comparative': [
                r'diferencia', r'comparar', r'mejor que', r'peor que',
                r'vs', r'versus', r'entre', r'cuál es mejor'
            ],
            'problem_solving': [
                r'qué hago', r'cómo soluciono', r'qué debo hacer', r'cómo arreglo',
                r'problema', r'error', r'falla', r'qué pasa si'
            ],
            'safety': [
                r'peligro', r'riesgo', r'seguro', r'no debo', r'no puedo',
                r'ácido', r'químico', r'tóxico', r'dañino', r'perjudicial',
                r'pH\s*[1-5]', r'pH\s*[9-9]', r'pH\s*1[0-4]', r'ph\s*[1-5]', r'ph\s*[9-9]', r'ph\s*1[0-4]'
            ],
            'technical': [
                r'cómo funciona', r'mecanismo', r'proceso', r'sistema',
                r'técnica', r'método', r'procedimiento'
            ],
            'practical': [
                r'cómo', r'pasos', r'proceso', r'instrucciones',
                r'manera', r'forma', r'modo'
            ],
            'scientific': [
                r'química', r'biológico', r'físico', r'reacción',
                r'pH', r'nutrientes', r'enzimas', r'bacterias'
            ],
            'consequence': [
                r'qué pasa si', r'consecuencia', r'resultado', r'efecto',
                r'impacto', r'resultado de', r'ocasiona'
            ]
        }
        
        # Estrategias de razonamiento específicas para acuaponía
        self.acuaponia_reasoning = {
            'pH_analysis': {
                'triggers': ['pH', 'ácido', 'básico', 'alcalino', 'acidez'],
                'reasoning': [
                    "El pH afecta la disponibilidad de nutrientes para las plantas",
                    "Los peces tienen rangos de pH específicos para sobrevivir",
                    "Las bacterias nitrificantes son sensibles al pH",
                    "El pH incorrecto puede causar estrés en el sistema"
                ]
            },
            'pH_extreme': {
                'triggers': ['pH 1', 'pH 2', 'pH 3', 'pH 4', 'pH 5', 'pH 9', 'pH 10', 'pH 11', 'pH 12', 'pH 13', 'pH 14', 'ph 1', 'ph 2', 'ph 3', 'ph 4', 'ph 5', 'ph 9', 'ph 10', 'ph 11', 'ph 12', 'ph 13', 'ph 14', 'ph es de 1', 'ph es de 2', 'ph es de 3', 'ph es de 4', 'ph es de 5', 'ph es de 9', 'ph es de 10', 'ph es de 11', 'ph es de 12', 'ph es de 13', 'ph es de 14'],
                'reasoning': [
                    "Un pH extremo es MORTAL para todo el sistema acuapónico",
                    "Los peces mueren instantáneamente con pH extremo",
                    "Las bacterias nitrificantes se destruyen completamente",
                    "Las plantas no pueden absorber nutrientes",
                    "El sistema colapsa irremediablemente"
                ]
            },
            'chemical_safety': {
                'triggers': ['ácido', 'acido', 'químico', 'quimico', 'cloro', 'detergente', 'pesticida', 'contaminante', 'toxico', 'tóxico'],
                'reasoning': [
                    "Los químicos pueden ser tóxicos para los peces",
                    "Las plantas pueden absorber químicos dañinos",
                    "Los químicos pueden matar las bacterias beneficiosas",
                    "El sistema es sensible a contaminantes"
                ]
            },
            'nutrient_balance': {
                'triggers': ['nutriente', 'fertilizante', 'alimento', 'desecho', 'crece', 'crecen', 'crecimiento'],
                'reasoning': [
                    "El exceso de nutrientes puede causar problemas",
                    "La falta de nutrientes afecta el crecimiento",
                    "El balance es crucial para el sistema",
                    "Los nutrientes deben ser biodisponibles"
                ]
            },
            'oxygen_management': {
                'triggers': ['oxígeno', 'aire', 'respiración', 'aireador', 'respirar'],
                'reasoning': [
                    "Los peces necesitan oxígeno disuelto para respirar",
                    "Las bacterias aeróbicas necesitan oxígeno",
                    "La falta de oxígeno puede causar muerte",
                    "El oxígeno se consume constantemente"
                ]
            },
            'temperature_control': {
                'triggers': ['temperatura', 'calor', 'frío', 'clima', 'ambiente'],
                'reasoning': [
                    "La temperatura afecta la actividad de las bacterias",
                    "Los peces tienen rangos de temperatura óptimos",
                    "La temperatura influye en la solubilidad del oxígeno",
                    "Los cambios bruscos causan estrés"
                ]
            },
            'plant_growth': {
                'triggers': ['planta', 'plantas', 'crece', 'crecen', 'crecimiento', 'mejor', 'mejores'],
                'reasoning': [
                    "Las plantas en acuaponía reciben nutrientes constantemente",
                    "El agua rica en nutrientes promueve el crecimiento rápido",
                    "La ausencia de suelo reduce enfermedades de raíz",
                    "El sistema proporciona condiciones óptimas de crecimiento"
                ]
            },
            'ecosystem_balance': {
                'triggers': ['sistema', 'ecosistema', 'balance', 'equilibrio', 'interconectado'],
                'reasoning': [
                    "El sistema acuapónico es un ecosistema cerrado",
                    "Todos los elementos están interconectados",
                    "El balance es crucial para el funcionamiento",
                    "La sinergia entre peces y plantas es beneficiosa"
                ]
            },
            'water_quality': {
                'triggers': ['agua', 'calidad', 'limpia', 'filtrada', 'purificada'],
                'reasoning': [
                    "El agua se recicla constantemente en el sistema",
                    "Los filtros biológicos mantienen la calidad del agua",
                    "Las plantas ayudan a purificar el agua",
                    "La calidad del agua es superior a otros sistemas"
                ]
            }
        }
        
        # Palabras clave que indican temas fuera del dominio de acuaponía
        self.out_of_domain_keywords = [
            # Tecnología y computación
            'programación', 'código', 'software', 'aplicación', 'app', 'web', 'internet', 'computadora', 'laptop', 'celular', 'smartphone',
            'python', 'javascript', 'html', 'css', 'java', 'c++', 'base de datos', 'servidor', 'cliente', 'api', 'framework',
            
            # Deportes
            'fútbol', 'futbol', 'basketball', 'baloncesto', 'tenis', 'golf', 'natación', 'ciclismo', 'correr', 'maratón', 'olimpiadas',
            
            # Entretenimiento
            'película', 'pelicula', 'serie', 'televisión', 'tv', 'música', 'musica', 'videojuego', 'juego', 'netflix', 'youtube',
            
            # Política y noticias
            'política', 'politica', 'presidente', 'gobierno', 'elecciones', 'congreso', 'senado', 'partido político', 'noticias',
            
            # Cocina y gastronomía
            'receta', 'cocina', 'chef', 'restaurante', 'comida', 'plato', 'ingrediente', 'cocinar', 'hornear', 'freír',
            
            # Viajes y turismo
            'viaje', 'turismo', 'hotel', 'avión', 'avion', 'aeropuerto', 'destino', 'vacaciones', 'playa', 'montaña',
            
            # Salud y medicina
            'enfermedad', 'síntoma', 'sintoma', 'medicina', 'doctor', 'hospital', 'tratamiento', 'diagnóstico', 'diagnostico',
            
            # Finanzas y economía
            'dinero', 'banco', 'inversión', 'inversion', 'bolsa', 'acciones', 'economía', 'economia', 'finanzas', 'crédito', 'credito',
            
            # Educación general
            'matemáticas', 'matematicas', 'historia', 'geografía', 'geografia', 'literatura', 'filosofía', 'filosofia', 'arte', 'música', 'musica'
        ]
    
    def _is_out_of_acuaponia_domain(self, question_lower: str) -> bool:
        """Determina si la pregunta está fuera del dominio de acuaponía"""
        # Si no hay contextos de acuaponía detectados, verificar palabras clave fuera del dominio
        if not any(context in question_lower for context in ['acuaponía', 'acuaponia', 'peces', 'plantas', 'agua', 'sistema', 'nutrientes', 'ph', 'bacterias']):
            # Verificar si contiene palabras clave fuera del dominio
            for keyword in self.out_of_domain_keywords:
                if keyword in question_lower:
                    return True
        return False
    
    def analyze_question(self, question: str) -> Dict:
        """Analiza una pregunta y determina la estrategia de razonamiento"""
        question_lower = question.lower()
        
        # Detectar tipo de pregunta
        detected_types = []
        for question_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, question_lower):
                    detected_types.append(question_type)
                    break
        
        # Detectar contexto específico de acuaponía
        acuaponia_contexts = []
        for context, data in self.acuaponia_reasoning.items():
            for trigger in data['triggers']:
                if trigger in question_lower:
                    acuaponia_contexts.append(context)
                    break
        
        # Detectar si está fuera del dominio de acuaponía
        is_out_of_domain = self._is_out_of_acuaponia_domain(question_lower)
        
        # Determinar estrategia principal
        primary_strategy = self._determine_primary_strategy(detected_types, acuaponia_contexts, is_out_of_domain)
        
        return {
            'question': question,
            'detected_types': detected_types,
            'acuaponia_contexts': acuaponia_contexts,
            'primary_strategy': primary_strategy,
            'reasoning_chain': self._generate_reasoning_chain(primary_strategy, acuaponia_contexts),
            'is_out_of_domain': is_out_of_domain
        }
    
    def _determine_primary_strategy(self, detected_types: List[str], acuaponia_contexts: List[str], is_out_of_domain: bool) -> str:
        """Determina la estrategia principal de razonamiento"""
        # Si está fuera del dominio, usar estrategia especial
        if is_out_of_domain:
            return 'out_of_domain'
        
        if 'safety' in detected_types:
            return 'safety'
        elif 'causal' in detected_types:
            return 'causal'
        elif 'problem_solving' in detected_types:
            return 'problem_solving'
        elif 'consequence' in detected_types:
            return 'consequence'
        elif 'technical' in detected_types:
            return 'technical'
        elif 'comparative' in detected_types:
            return 'comparative'
        elif 'practical' in detected_types:
            return 'practical'
        elif 'scientific' in detected_types:
            return 'scientific'
        else:
            return 'general'
    
    def _generate_reasoning_chain(self, strategy: str, contexts: List[str]) -> List[str]:
        """Genera una cadena de razonamiento basada en la estrategia y contextos"""
        reasoning_chain = []
        
        # Agregar razonamiento específico de acuaponía
        for context in contexts:
            if context in self.acuaponia_reasoning:
                reasoning_chain.extend(self.acuaponia_reasoning[context]['reasoning'])
        
        # Agregar razonamiento general de la estrategia
        if strategy in self.reasoning_strategies:
            strategy_reasoning = self.reasoning_strategies[strategy]()
            reasoning_chain.extend(strategy_reasoning)
        
        return reasoning_chain
    
    def apply_reasoning(self, question: str, base_response: str) -> str:
        """Aplica razonamiento estratégico a una respuesta base"""
        analysis = self.analyze_question(question)
        
        # Generar respuesta con razonamiento
        reasoned_response = self._build_reasoned_response(analysis, base_response)
        
        return reasoned_response
    
    def _build_reasoned_response(self, analysis: Dict, base_response: str) -> str:
        """Construye una respuesta con razonamiento aplicado"""
        question = analysis['question']
        strategy = analysis['primary_strategy']
        reasoning_chain = analysis['reasoning_chain']
        
        # Determinar el enfoque de la respuesta
        if strategy == 'out_of_domain':
            return self._build_out_of_domain_response(question, reasoning_chain, base_response)
        elif strategy == 'safety':
            return self._build_safety_response(question, reasoning_chain, base_response)
        elif strategy == 'causal':
            return self._build_causal_response(question, reasoning_chain, base_response)
        elif strategy == 'problem_solving':
            return self._build_problem_solving_response(question, reasoning_chain, base_response)
        elif strategy == 'consequence':
            return self._build_consequence_response(question, reasoning_chain, base_response)
        else:
            return self._build_general_response(question, reasoning_chain, base_response)
    
    def _build_out_of_domain_response(self, question: str, reasoning: List[str], base_response: str) -> str:
        """Construye respuesta amable para preguntas fuera del dominio de acuaponía"""
        response = "## 🤖 Respuesta Amable - Fuera de Mi Dominio\n\n"
        response += "### 📝 Mi Especialización\n\n"
        response += "> Soy un **sistema especializado en acuaponía** diseñado para ayudarte con preguntas sobre cultivos acuapónicos, peces, plantas, calidad del agua, pH, nutrientes y todo lo relacionado con sistemas de cultivo sostenible.\n\n"
        
        response += "### 🎯 Lo Que Puedo Ayudarte\n\n"
        response += "**Mi conocimiento incluye:**\n\n"
        response += "- **🐟 Cuidado de peces** en sistemas acuapónicos\n"
        response += "- **🌱 Cultivo de plantas** sin suelo\n"
        response += "- **💧 Calidad del agua** y parámetros\n"
        response += "- **🧪 pH y nutrientes** para el sistema\n"
        response += "- **🦠 Bacterias nitrificantes** y ciclos biológicos\n"
        response += "- **🔧 Mantenimiento** del sistema acuapónico\n"
        response += "- **⚠️ Seguridad** y prevención de problemas\n"
        response += "- **📊 Optimización** del rendimiento\n\n"
        
        response += "### 💡 Sugerencia\n\n"
        response += "**¿Te gustaría preguntarme sobre:**\n\n"
        response += "- ¿Cómo funciona un sistema acuapónico?\n"
        response += "- ¿Qué peces son mejores para acuaponía?\n"
        response += "- ¿Cómo mantener el pH correcto?\n"
        response += "- ¿Qué plantas crecen mejor en acuaponía?\n"
        response += "- ¿Cómo solucionar problemas comunes?\n\n"
        
        response += "### 🌱 Acerca de Acuaponía\n\n"
        response += "La **acuaponía** es un sistema de cultivo sostenible que combina la acuicultura (cría de peces) con la hidroponía (cultivo de plantas sin suelo). Es una forma innovadora y ecológica de producir alimentos frescos en casa o a escala comercial.\n\n"
        
        response += "**¡Estoy aquí para ayudarte con cualquier pregunta sobre acuaponía!** 🌟"
        
        return response
    
    def _build_safety_response(self, question: str, reasoning: List[str], base_response: str) -> str:
        """Construye respuesta enfocada en seguridad"""
        if 'ácido' in question.lower():
            response = "## ⚠️ Análisis de Seguridad - Ácidos\n\n"
            response += "### Riesgo Principal\n\n"
            response += "**NO debes agregar ácido** a un cultivo acuapónico por las siguientes razones científicas:\n\n"
            
            response += "### Análisis Químico\n\n"
            response += "| Aspecto | Efecto |\n"
            response += "|---------|--------|\n"
            response += "| **Alteración de pH** | Los ácidos alteran drásticamente el pH del agua |\n"
            response += "| **pH Ideal** | `6.0-7.0` para acuaponía |\n"
            response += "| **Niveles Peligrosos** | Los ácidos pueden bajar el pH a niveles peligrosos |\n\n"
            
            response += "### Impacto en los Peces\n\n"
            response += "- **Sensibilidad extrema** a cambios de pH\n"
            response += "- **Estrés respiratorio** por pH bajo\n"
            response += "- **Muerte por acidosis**\n\n"
            
            response += "### Efecto en las Plantas\n\n"
            response += "- **Bloqueo de absorción** de nutrientes\n"
            response += "- **Deficiencias** de hierro, fósforo y otros minerales\n"
            response += "- **Amarillamiento** y problemas nutricionales\n\n"
            
            response += "### Daño a las Bacterias\n\n"
            response += "- **Sensibilidad al pH** de bacterias nitrificantes\n"
            response += "- **Muerte de bacterias** beneficiosas\n"
            response += "- **Interrupción** del ciclo del nitrógeno\n\n"
            
            response += "### Alternativas Seguras\n\n"
            response += "- **Métodos naturales** para ajustar pH\n"
            response += "- **Cambios graduales** de agua\n"
            response += "- **Monitoreo constante** del pH\n"
            
            return response
        
        return f"## ⚠️ Análisis de Seguridad\n\n{random.choice(reasoning)}\n\n> {base_response}"
    
    def _build_causal_response(self, question: str, reasoning: List[str], base_response: str) -> str:
        """Construye respuesta enfocada en causalidad"""
        
        # Respuestas específicas para preguntas sobre crecimiento de plantas
        if 'crece' in question.lower() or 'crecen' in question.lower() or 'mejor' in question.lower():
            response = "## 🌱 Análisis Causal del Crecimiento\n\n"
            response += "### Causa Principal\n\n"
            response += "Las plantas crecen mejor en acuaponía debido a múltiples factores sinérgicos.\n\n"
            
            response += "### Mecanismos Causales\n\n"
            response += "| Factor | Descripción |\n"
            response += "|--------|-------------|\n"
            response += "| **1. Nutrición Constante** | Las plantas reciben nutrientes disueltos 24/7 |\n"
            response += "| **2. Absorción Eficiente** | Sin suelo, las raíces absorben nutrientes directamente |\n"
            response += "| **3. Oxigenación Óptima** | Las raíces tienen acceso constante al oxígeno |\n"
            response += "| **4. Sin Enfermedades** | La ausencia de suelo elimina patógenos de raíz |\n"
            response += "| **5. pH Controlado** | El sistema mantiene pH óptimo para absorción |\n\n"
            
            response += "### Evidencia Científica\n\n"
            response += "- **Crecimiento 30-50% más rápido** que en suelo\n"
            response += "- **Mayor densidad de nutrientes** en tejidos\n"
            response += "- **Mejor desarrollo radicular**\n"
            response += "- **Mayor producción por área**\n\n"
            
            response += "### Relación Causal\n\n"
            response += "> Este fenómeno ocurre porque la acuaponía crea un ecosistema donde cada elemento optimiza el crecimiento de las plantas."
        elif 'ácido' in question.lower() or 'acido' in question.lower() or 'químico' in question.lower() or 'quimico' in question.lower():
            response = "## ⚠️ Análisis Causal de Seguridad Química\n\n"
            response += "### Causa Principal\n\n"
            response += "Los ácidos y químicos son extremadamente peligrosos para el sistema acuapónico.\n\n"
            
            response += "### Mecanismos de Daño\n\n"
            response += "| Mecanismo | Efecto |\n"
            response += "|-----------|--------|\n"
            response += "| **1. Toxicidad para Peces** | Los ácidos causan estrés respiratorio y muerte |\n"
            response += "| **2. Daño a Bacterias** | Destruyen las bacterias nitrificantes beneficiosas |\n"
            response += "| **3. Absorción por Plantas** | Las plantas absorben químicos tóxicos |\n"
            response += "| **4. Alteración de pH** | Cambios bruscos causan estrés en todo el sistema |\n"
            response += "| **5. Contaminación Persistente** | Los químicos pueden persistir en el sistema |\n\n"
            
            response += "### Consecuencias Específicas\n\n"
            response += "- **Muerte de peces** por acidosis o toxicidad\n"
            response += "- **Interrupción del ciclo del nitrógeno**\n"
            response += "- **Deficiencias nutricionales** en plantas\n"
            response += "- **Pérdida del equilibrio** del ecosistema\n\n"
            
            response += "### Relación Causal\n\n"
            response += "> Este fenómeno ocurre porque el sistema acuapónico es un ecosistema cerrado donde cualquier contaminante afecta a todos los componentes."
        else:
            response = "## 🔍 Análisis Causal\n\n"
            response += "### Causa Principal\n\n"
            response += f"{random.choice(reasoning)}\n\n"
            response += "### Mecanismo\n\n"
            response += f"> {base_response}\n\n"
            response += "### Relación Causal\n\n"
            response += "> Este fenómeno ocurre porque en acuaponía todos los elementos están interconectados."
        
        return response
    
    def _build_problem_solving_response(self, question: str, reasoning: List[str], base_response: str) -> str:
        """Construye respuesta enfocada en solución de problemas"""
        response = "## 🛠️ Estrategia de Solución\n\n"
        response += "### Diagnóstico\n\n"
        response += f"> {random.choice(reasoning)}\n\n"
        response += "### Solución\n\n"
        response += f"{base_response}\n\n"
        response += "### Prevención\n\n"
        response += "> Monitorea regularmente los parámetros del sistema."
        
        return response
    
    def _build_consequence_response(self, question: str, reasoning: List[str], base_response: str) -> str:
        """Construye respuesta enfocada en consecuencias"""
        response = "## 📊 Análisis de Consecuencias\n\n"
        response += "### Si haces esto\n\n"
        response += f"> {random.choice(reasoning)}\n\n"
        response += "### Resultado\n\n"
        response += f"{base_response}\n\n"
        response += "### Impacto en el Sistema\n\n"
        response += "> Esto afectará todo el ecosistema acuapónico."
        
        return response
    
    def _build_general_response(self, question: str, reasoning: List[str], base_response: str) -> str:
        """Construye respuesta general con razonamiento"""
        response = "## 🧠 Análisis Inteligente\n\n"
        if reasoning:
            response += f"### Razonamiento\n\n"
            response += f"> {random.choice(reasoning)}\n\n"
        response += f"### Respuesta\n\n"
        response += f"{base_response}"
        
        return response
    
    # Estrategias de razonamiento específicas
    def _apply_causal_reasoning(self) -> List[str]:
        return [
            "Analicemos la relación causa-efecto en el sistema acuapónico",
            "El sistema acuapónico funciona como un ecosistema interconectado",
            "Cada acción tiene consecuencias en múltiples niveles del sistema",
            "Identifiquemos los factores que contribuyen al resultado observado",
            "Examinemos cómo los diferentes componentes interactúan entre sí",
            "Evaluemos la contribución de cada elemento al resultado final"
        ]
    
    def _apply_comparative_reasoning(self) -> List[str]:
        return [
            "Comparemos las diferentes opciones disponibles",
            "Evaluemos las ventajas y desventajas de cada método",
            "Consideremos las alternativas más seguras y efectivas"
        ]
    
    def _apply_problem_solving_reasoning(self) -> List[str]:
        return [
            "Identifiquemos la raíz del problema",
            "Desarrollemos una estrategia sistemática de solución",
            "Implementemos medidas preventivas para el futuro"
        ]
    
    def _apply_safety_reasoning(self) -> List[str]:
        return [
            "La seguridad del sistema es la prioridad máxima",
            "Cualquier acción debe considerar el impacto en todos los organismos",
            "Es mejor prevenir que curar en sistemas acuapónicos"
        ]
    
    def _apply_technical_reasoning(self) -> List[str]:
        return [
            "Analicemos los principios técnicos involucrados",
            "Comprendamos los mecanismos biológicos del sistema",
            "Consideremos los parámetros técnicos óptimos"
        ]
    
    def _apply_practical_reasoning(self) -> List[str]:
        return [
            "Enfoquémonos en soluciones prácticas y aplicables",
            "Consideremos la facilidad de implementación",
            "Evaluemos el costo-beneficio de las acciones"
        ]
    
    def _apply_scientific_reasoning(self) -> List[str]:
        return [
            "Basemos nuestras decisiones en principios científicos",
            "Analicemos la evidencia y los datos disponibles",
            "Apliquemos el método científico para resolver problemas"
        ]
    
    def _apply_consequence_reasoning(self) -> List[str]:
        return [
            "Evaluemos las consecuencias a corto y largo plazo",
            "Consideremos el impacto en todo el ecosistema",
            "Analicemos los efectos en cadena de nuestras acciones"
        ]

    def _apply_out_of_domain_reasoning(self) -> List[str]:
        """Aplica razonamiento para preguntas fuera del dominio"""
        return [
            "Esta pregunta está fuera de mi área de especialización",
            "Mi conocimiento se centra en sistemas acuapónicos",
            "Puedo ayudarte mejor con temas relacionados a acuaponía",
            "Te sugiero consultar fuentes especializadas en el tema"
        ]

# Función de conveniencia para uso directo
def apply_intelligent_reasoning(question: str, base_response: str) -> str:
    """Aplica razonamiento inteligente a una respuesta base"""
    engine = ReasoningEngine()
    return engine.apply_reasoning(question, base_response) 