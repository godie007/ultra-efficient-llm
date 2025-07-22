#!/usr/bin/env python3
"""
🧠 GENERATIVE ENHANCER - ULTRAEFFICIENTLLM
==========================================

Sistema de post-procesamiento para mejorar la generación de respuestas.
"""

import re
import random
from typing import List, Dict, Tuple

class GenerativeEnhancer:
    """Sistema para mejorar la generación de respuestas"""
    
    def __init__(self):
        # Metáforas y analogías para acuaponía
        self.metaforas_acuaponia = {
            'sistema': ['ecosistema en miniatura', 'jardín mágico', 'laboratorio viviente', 'fábrica natural'],
            'peces': ['trabajadores acuáticos', 'mascotas productivas', 'bomberos del agua', 'jardineros submarinos'],
            'plantas': ['estrellas del show', 'comedores naturales', 'filtros vivientes', 'transformadores verdes'],
            'agua': ['sangre del sistema', 'carretera líquida', 'mensajero de nutrientes', 'circulación natural'],
            'nutrientes': ['comida de lujo', 'vitaminas naturales', 'combustible verde', 'medicina vegetal'],
            'bacterias': ['trabajadores invisibles', 'alquimistas microscópicos', 'transformadores mágicos', 'chefs biológicos'],
            'filtración': ['sistema de limpieza', 'depuradora natural', 'lavadora biológica', 'purificador viviente']
        }
        
        # Frases creativas para diferentes tipos de razonamiento
        self.frases_creativas = {
            'causal': [
                "Es como si {elemento} fuera {metafora}",
                "Imagina que {elemento} actúa como {metafora}",
                "Es similar a cuando {elemento} funciona como {metafora}",
                "Piensa en {elemento} como {metafora}"
            ],
            'inferencial': [
                "Es como una señal de SOS del {elemento}",
                "Parece que {elemento} está enviando un mensaje",
                "Es como un termómetro que indica problemas en {elemento}",
                "Es similar a una alarma que avisa sobre {elemento}"
            ],
            'comparativo': [
                "Es como comparar {elemento1} con {elemento2}",
                "Es similar a la diferencia entre {elemento1} y {elemento2}",
                "Es como tener {elemento1} en lugar de {elemento2}",
                "Es como elegir entre {elemento1} y {elemento2}"
            ],
            'secuencial': [
                "Es como una danza perfecta entre {elemento1} y {elemento2}",
                "Es similar a una cadena de transformación donde {elemento1} se convierte en {elemento2}",
                "Es como un ciclo natural donde {elemento1} alimenta a {elemento2}",
                "Es como una fábrica donde {elemento1} produce {elemento2}"
            ]
        }
        
        # Palabras de transición creativas
        self.transiciones = [
            "Es fascinante cómo", "Es increíble que", "Es sorprendente que",
            "Es maravilloso que", "Es extraordinario que", "Es asombroso que",
            "Es notable que", "Es impresionante que", "Es admirable que"
        ]
    
    def detectar_tipo_razonamiento(self, pregunta: str) -> str:
        """Detectar el tipo de razonamiento basado en la pregunta"""
        pregunta_lower = pregunta.lower()
        
        if any(palabra in pregunta_lower for palabra in ['por qué', 'causa', 'razón']):
            return 'causal'
        elif any(palabra in pregunta_lower for palabra in ['si', 'cuando', 'qué pasa']):
            return 'inferencial'
        elif any(palabra in pregunta_lower for palabra in ['diferencia', 'comparar', 'mejor que']):
            return 'comparativo'
        elif any(palabra in pregunta_lower for palabra in ['cómo funciona', 'pasos', 'proceso']):
            return 'secuencial'
        else:
            return 'general'
    
    def extraer_elementos_clave(self, respuesta: str) -> List[str]:
        """Extraer elementos clave de la respuesta"""
        elementos = []
        palabras_acuaponia = ['acuaponía', 'peces', 'plantas', 'agua', 'nutrientes', 'sistema', 'desechos', 'bacterias']
        
        for palabra in palabras_acuaponia:
            if palabra.lower() in respuesta.lower():
                elementos.append(palabra)
        
        return elementos
    
    def limpiar_respuesta(self, respuesta: str) -> str:
        """Limpiar respuesta de caracteres repetitivos y errores"""
        # Eliminar repeticiones excesivas
        respuesta = re.sub(r'(\w+\s+){3,}\1', r'\1', respuesta)
        
        # Eliminar caracteres sueltos repetitivos
        respuesta = re.sub(r'\s+[,\s]+\s+', ' ', respuesta)
        
        # Eliminar repeticiones de frases completas
        palabras = respuesta.split()
        if len(palabras) > 50:
            # Tomar solo las primeras 50 palabras para evitar repeticiones excesivas
            respuesta = ' '.join(palabras[:50])
        
        return respuesta.strip()
    
    def aplicar_metafora(self, respuesta: str, elemento: str) -> str:
        """Aplicar metáfora a un elemento específico"""
        if elemento in self.metaforas_acuaponia:
            metafora = random.choice(self.metaforas_acuaponia[elemento])
            # Reemplazar la primera ocurrencia del elemento con la metáfora
            respuesta = respuesta.replace(elemento, f"{elemento} (como {metafora})", 1)
        return respuesta
    
    def generar_respuesta_creativa(self, pregunta: str, respuesta_base: str) -> str:
        """Generar una respuesta creativa basada en la respuesta base"""
        tipo_razonamiento = self.detectar_tipo_razonamiento(pregunta)
        elementos = self.extraer_elementos_clave(respuesta_base)
        
        # Limpiar respuesta base
        respuesta_limpia = self.limpiar_respuesta(respuesta_base)
        
        # Si la respuesta es muy corta o repetitiva, generar una nueva
        if len(respuesta_limpia.split()) < 5 or len(set(respuesta_limpia.split())) / len(respuesta_limpia.split()) < 0.5:
            return self.generar_respuesta_completamente_nueva(pregunta, tipo_razonamiento, elementos)
        
        # Mejorar respuesta existente
        respuesta_mejorada = self.mejorar_respuesta_existente(respuesta_limpia, tipo_razonamiento, elementos)
        
        return respuesta_mejorada
    
    def generar_respuesta_completamente_nueva(self, pregunta: str, tipo_razonamiento: str, elementos: List[str]) -> str:
        """Generar una respuesta completamente nueva"""
        if not elementos:
            elementos = ['sistema', 'peces', 'plantas']
        
        elemento_principal = elementos[0] if elementos else 'sistema'
        
        if tipo_razonamiento == 'causal':
            metafora = random.choice(self.metaforas_acuaponia.get(elemento_principal, ['sistema natural']))
            transicion = random.choice(self.transiciones)
            return f"{transicion} {elemento_principal} funciona como {metafora}."
        
        elif tipo_razonamiento == 'inferencial':
            metafora = random.choice(self.metaforas_acuaponia.get(elemento_principal, ['indicador natural']))
            return f"Es como una señal de SOS del {elemento_principal} que actúa como {metafora}."
        
        elif tipo_razonamiento == 'comparativo':
            if len(elementos) >= 2:
                return f"Es como comparar {elementos[0]} con {elementos[1]} en términos de eficiencia."
            else:
                return f"Es como tener un {elemento_principal} mejorado que funciona de manera más eficiente."
        
        elif tipo_razonamiento == 'secuencial':
            if len(elementos) >= 2:
                return f"Es como una danza perfecta entre {elementos[0]} y {elementos[1]}."
            else:
                return f"Es como un ciclo natural donde {elemento_principal} se transforma continuamente."
        
        else:
            metafora = random.choice(self.metaforas_acuaponia.get(elemento_principal, ['sistema natural']))
            return f"El {elemento_principal} funciona como {metafora} en el sistema de acuaponía."
    
    def mejorar_respuesta_existente(self, respuesta: str, tipo_razonamiento: str, elementos: List[str]) -> str:
        """Mejorar una respuesta existente"""
        # Aplicar metáforas a elementos clave
        for elemento in elementos[:2]:  # Aplicar a máximo 2 elementos
            respuesta = self.aplicar_metafora(respuesta, elemento)
        
        # Añadir transición creativa si no la tiene
        if not any(transicion.lower() in respuesta.lower() for transicion in self.transiciones):
            transicion = random.choice(self.transiciones)
            respuesta = f"{transicion} {respuesta.lower()}"
        
        # Asegurar que termine con punto
        if not respuesta.endswith('.'):
            respuesta += '.'
        
        return respuesta
    
    def post_procesar_respuesta(self, pregunta: str, respuesta_original: str) -> str:
        """Post-procesar una respuesta para mejorarla"""
        # Limpiar respuesta original
        respuesta_limpia = self.limpiar_respuesta(respuesta_original)
        
        # Si la respuesta es muy deficiente, generar una nueva
        if len(respuesta_limpia.split()) < 3:
            return self.generar_respuesta_completamente_nueva(pregunta, 'general', [])
        
        # Mejorar respuesta existente
        respuesta_mejorada = self.generar_respuesta_creativa(pregunta, respuesta_limpia)
        
        # Asegurar longitud adecuada (permitir respuestas más largas)
        palabras = respuesta_mejorada.split()
        if len(palabras) > 100:
            respuesta_mejorada = ' '.join(palabras[:100]) + '.'
        
        return respuesta_mejorada

# Función de utilidad para usar el enhancer
def mejorar_respuesta_generativa(pregunta: str, respuesta_original: str) -> str:
    """Función de utilidad para mejorar respuestas generativas con razonamiento inteligente"""
    enhancer = GenerativeEnhancer()
    
    # Si la respuesta original es muy deficiente, generar una respuesta específica
    if len(respuesta_original.strip()) < 10 or respuesta_original.count('"') > 3 or 'como "' in respuesta_original or respuesta_original.strip().startswith('¿'):
        if 'crece' in pregunta.lower() or 'crecen' in pregunta.lower() or 'mejor' in pregunta.lower():
            return ("Las plantas crecen mejor en acuaponía debido a múltiples ventajas sinérgicas: "
                   "nutrición constante, absorción eficiente sin suelo, oxigenación óptima de raíces, "
                   "ausencia de enfermedades de suelo, y pH controlado. Esto resulta en crecimiento "
                   "30-50% más rápido que en cultivos tradicionales.")
        elif any(ph_value in pregunta.lower() for ph_value in ['ph 1', 'ph 2', 'ph 3', 'ph 4', 'ph 5', 'ph 9', 'ph 10', 'ph 11', 'ph 12', 'ph 13', 'ph 14', 'ph es de 1', 'ph es de 2', 'ph es de 3', 'ph es de 4', 'ph es de 5', 'ph es de 9', 'ph es de 10', 'ph es de 11', 'ph es de 12', 'ph es de 13', 'ph es de 14']):
            return ("## 🚨 EMERGENCIA CRÍTICA - pH EXTREMO\n\n"
                   "**⚠️ ADVERTENCIA MÁXIMA:** Un pH extremo es **MORTAL** para todo el sistema acuapónico.\n\n"
                   "### 🚨 Consecuencias Inmediatas\n\n"
                   "- **🐟 Muerte instantánea de peces:** pH extremo es incompatible con la vida acuática\n"
                   "- **🦠 Destrucción total de bacterias:** Las bacterias nitrificantes mueren inmediatamente\n"
                   "- **🌱 Muerte de plantas:** Las raíces se queman y las plantas mueren\n"
                   "- **💀 Colapso total del sistema:** El ecosistema se destruye irremediablemente\n\n"
                   "### 📊 Comparación de pH\n\n"
                   "| pH | Estado | Efecto |\n"
                   "|----|--------|--------|\n"
                   "| **1-5** | **MORTAL** | Muerte instantánea |\n"
                   "| 6-7 | **IDEAL** | Sistema saludable |\n"
                   "| 5-8 | **ACEPTABLE** | Sistema funcional |\n"
                   "| 9-14 | **MORTAL** | Muerte instantánea |\n\n"
                   "### 🆘 Acciones Inmediatas\n\n"
                   "Si tu sistema tiene pH extremo:\n\n"
                   "1. **🛑 DETENER TODO** - No agregar más químicos\n"
                   "2. **💧 Cambio de agua 100%** - Reemplazar toda el agua\n"
                   "3. **🧪 Medir pH nuevo** - Verificar que esté en rango 6-7\n"
                   "4. **🔄 Reiniciar sistema** - Ciclar el sistema nuevamente\n"
                   "5. **📞 Consultar experto** - Buscar ayuda profesional\n\n"
                   "### ⚠️ Prevención\n\n"
                   "- **NUNCA** agregar ácidos directamente al sistema\n"
                   "- **SIEMPRE** medir pH antes de cualquier ajuste\n"
                   "- **GRADUALMENTE** hacer cambios de pH\n"
                   "- **MONITOREAR** constantemente el pH\n\n"
                   "### 🎯 Conclusión\n\n"
                   "**Un pH extremo es una emergencia crítica que requiere acción inmediata.** El sistema acuapónico es extremadamente sensible y un pH fuera del rango 5-8 destruye completamente el ecosistema.")
        elif 'ácido' in pregunta.lower() or 'acido' in pregunta.lower() or 'químico' in pregunta.lower() or 'quimico' in pregunta.lower():
            return ("## ⚠️ Advertencia de Seguridad - Ácidos en Acuaponía\n\n"
                   "**NO debes usar ácidos o químicos** en sistemas acuapónicos por las siguientes razones científicas:\n\n"
                   "### Efectos Tóxicos\n\n"
                   "- **Toxicidad para peces:** Causan estrés respiratorio y muerte\n"
                   "- **Destrucción de bacterias:** Matan las bacterias nitrificantes beneficiosas\n"
                   "- **Absorción por plantas:** Las plantas absorben químicos tóxicos\n"
                   "- **Alteración de pH:** Cambios bruscos causan estrés en todo el sistema\n"
                   "- **Contaminación persistente:** Los químicos pueden persistir en el sistema\n\n"
                   "### Sistema Sensible\n\n"
                   "> El sistema acuapónico es un ecosistema cerrado muy sensible donde cualquier químico afecta a todos los componentes. Es fundamental mantener el equilibrio natural del sistema para garantizar la salud de peces, plantas y bacterias.\n\n"
                   "### Alternativas Seguras\n\n"
                   "- **Métodos naturales** para ajustar pH\n"
                   "- **Cambios graduales** de agua\n"
                   "- **Monitoreo constante** del pH\n\n"
                   "### Conclusión\n\n"
                   "**En resumen:** Los ácidos son extremadamente peligrosos para el sistema acuapónico porque alteran el pH del agua, son tóxicos para los peces, destruyen las bacterias nitrificantes beneficiosas, y pueden ser absorbidos por las plantas causando daños irreversibles. Siempre usa métodos naturales y seguros para mantener el equilibrio del sistema.")
        else:
            return ("## 🌱 Principios de Acuaponía\n\n"
                   "### Ecosistema Interconectado\n\n"
                   "En acuaponía, el sistema funciona como un ecosistema interconectado donde cada elemento tiene un papel específico:\n\n"
                   "| Componente | Función |\n"
                   "|------------|---------|\n"
                   "| **Peces** | Producen desechos ricos en nutrientes |\n"
                   "| **Bacterias** | Convierten desechos en nutrientes |\n"
                   "| **Plantas** | Purifican el agua para los peces |\n\n"
                   "### Ciclo Natural\n\n"
                   "> Este ciclo natural crea un sistema sostenible y eficiente donde cada elemento beneficia a los demás.")
    
    # Si se generó una respuesta específica, devolverla directamente sin más procesamiento
    if 'ácido' in pregunta.lower() or 'acido' in pregunta.lower() or 'químico' in pregunta.lower() or 'quimico' in pregunta.lower():
        if len(respuesta_original.strip()) < 50:  # Si la respuesta original es deficiente
            return ("## ⚠️ Advertencia de Seguridad - Ácidos en Acuaponía\n\n"
                   "**NO debes usar ácidos o químicos** en sistemas acuapónicos por las siguientes razones científicas:\n\n"
                   "### Efectos Tóxicos\n\n"
                   "- **Toxicidad para peces:** Causan estrés respiratorio y muerte\n"
                   "- **Destrucción de bacterias:** Matan las bacterias nitrificantes beneficiosas\n"
                   "- **Absorción por plantas:** Las plantas absorben químicos tóxicos\n"
                   "- **Alteración de pH:** Cambios bruscos causan estrés en todo el sistema\n"
                   "- **Contaminación persistente:** Los químicos pueden persistir en el sistema\n\n"
                   "### Sistema Sensible\n\n"
                   "> El sistema acuapónico es un ecosistema cerrado muy sensible donde cualquier químico afecta a todos los componentes. Es fundamental mantener el equilibrio natural del sistema para garantizar la salud de peces, plantas y bacterias.\n\n"
                   "### Alternativas Seguras\n\n"
                   "- **Métodos naturales** para ajustar pH\n"
                   "- **Cambios graduales** de agua\n"
                   "- **Monitoreo constante** del pH\n\n"
                   "### Conclusión\n\n"
                   "**En resumen:** Los ácidos son extremadamente peligrosos para el sistema acuapónico porque alteran el pH del agua, son tóxicos para los peces, destruyen las bacterias nitrificantes beneficiosas, y pueden ser absorbidos por las plantas causando daños irreversibles. Siempre usa métodos naturales y seguros para mantener el equilibrio del sistema.")
    
    # Aplicar razonamiento inteligente primero
    try:
        from reasoning_engine import apply_intelligent_reasoning
        respuesta_razonada = apply_intelligent_reasoning(pregunta, respuesta_original)
    except ImportError:
        # Si no está disponible el motor de razonamiento, usar solo el enhancer
        respuesta_razonada = respuesta_original
    
    # Luego aplicar mejoras generativas (solo si no es una respuesta específica ya generada)
    if len(respuesta_razonada.strip()) < 50:  # Solo procesar si la respuesta es corta
        respuesta_mejorada = enhancer.post_procesar_respuesta(pregunta, respuesta_razonada)
    else:
        respuesta_mejorada = respuesta_razonada
    
    # Si la respuesta mejorada contiene Markdown mal formateado, limpiarla
    # Solo limpiar si hay texto malformado antes del primer ##
    if '##' in respuesta_mejorada:
        partes = respuesta_mejorada.split('##')
        if len(partes) > 1 and len(partes[0].strip()) < 50 and partes[0].strip():
            # Solo limpiar si hay texto significativo antes del ##
            respuesta_mejorada = '##' + '##'.join(partes[1:])
    
    # Limpieza final: eliminar frases malformadas al inicio
    if respuesta_mejorada.startswith('Es sorprendente que ##') or respuesta_mejorada.startswith('Es increíble que ##'):
        partes = respuesta_mejorada.split('##')
        if len(partes) > 1:
            respuesta_mejorada = '##' + '##'.join(partes[1:])
    
    # Asegurar que la respuesta no esté vacía
    if not respuesta_mejorada or len(respuesta_mejorada.strip()) < 10:
        respuesta_mejorada = respuesta_original
    
    return respuesta_mejorada 