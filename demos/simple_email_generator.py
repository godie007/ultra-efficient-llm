#!/usr/bin/env python3
"""
Simple Email Generator using UltraEfficientLLM
Generates professional emails using predefined templates
"""

import sys
import os
import json
import random
from datetime import datetime
from typing import List, Dict, Optional

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ultra_efficient_llm import UltraEfficientLLM


class SimpleEmailGenerator:
    """Simple professional email generator using UltraEfficientLLM"""
    
    def __init__(self):
        self.model = UltraEfficientLLM(
            max_pattern_length=6,
            min_frequency=2,
            max_patterns=3000
        )
        self.email_templates = self.load_email_templates()
        self.trained = False
        
    def load_email_templates(self) -> Dict[str, List[str]]:
        """Load professional email templates in Spanish"""
        return {
            "meeting_request": [
                "Estimado/a [Nombre], espero que este correo le encuentre bien. Le escribo para solicitar una reunión con el fin de discutir [tema]. Me gustaría proponer [día] a las [hora] para nuestra reunión. Quedo a la espera de su confirmación. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], me pongo en contacto con usted para coordinar una reunión sobre [tema]. ¿Podría estar disponible [día] a las [hora]? Si este horario no le conviene, por favor hágame saber sus alternativas. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], agradezco su tiempo. Quisiera solicitar una reunión para discutir [tema]. Propongo reunirnos [día] a las [hora]. Por favor, confirme si este horario le resulta conveniente. Atentamente, [Tu Nombre]"
            ],
            "thank_you": [
                "Estimado/a [Nombre], muchas gracias por [acción]. Realmente aprecio [detalle específico]. [Impacto]. Espero poder [interacción futura]. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], le escribo para expresar mi sincera gratitud por [lo que hicieron]. [Por qué importa]. Gracias nuevamente por su [apoyo/ayuda]. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], quería tomar un momento para agradecerle por [acción específica]. [Cómo ayudó]. Su [apoyo] significa mucho para mí. Atentamente, [Tu Nombre]"
            ],
            "follow_up": [
                "Estimado/a [Nombre], espero que este correo le encuentre bien. Quería hacer seguimiento sobre [tema] que discutimos [fecha]. [Estado actual]. ¿Podría proporcionarme una actualización? Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], me pongo en contacto con usted para hacer seguimiento sobre [asunto]. [Recordatorio]. Agradecería su respuesta para continuar con [próximo paso]. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], espero que esté bien. Quería consultar sobre [tema] del que hablamos recientemente. [Progreso]. Quedo a la espera de su respuesta. Atentamente, [Tu Nombre]"
            ],
            "business_proposal": [
                "Estimado/a [Nombre], espero que este mensaje le encuentre bien. Me pongo en contacto con usted para presentarle [propuesta]. [Detalles de la propuesta]. Me gustaría discutir esta oportunidad más a fondo. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], le escribo para presentarle una propuesta de [servicio/producto]. [Beneficios]. ¿Podríamos agendar una reunión para discutir los detalles? Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], agradezco su interés en [asunto]. Me complace presentarle nuestra propuesta para [objetivo]. [Información clave]. Quedo a la espera de su respuesta. Atentamente, [Tu Nombre]"
            ],
            "general": [
                "Estimado/a [Nombre], espero que este correo le encuentre bien. Le escribo para [propósito]. [Detalles]. Quedo a la espera de su respuesta. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], me pongo en contacto con usted respecto a [tema]. [Explicación]. Agradecería su opinión sobre este asunto. Atentamente, [Tu Nombre]",
                "Estimado/a [Nombre], agradezco su tiempo. Le escribo para [propósito]. [Información]. Estoy disponible para cualquier consulta. Atentamente, [Tu Nombre]"
            ]
        }
    
    def train_model(self):
        """Train the model with email templates"""
        if self.trained:
            return
            
        print("📧 Entrenando modelo con plantillas de correo...")
        
        # Combine all templates for training
        all_templates = []
        for category, templates in self.email_templates.items():
            all_templates.extend(templates)
        
        # Add email-specific patterns
        email_patterns = [
            "Estimado/a [Nombre], espero que este correo le encuentre bien.",
            "Agradezco su tiempo.",
            "Le escribo para",
            "Quedo a la espera de su respuesta.",
            "Atentamente,",
            "Saludos cordiales,",
            "Por favor, hágame saber si",
            "Agradecería",
            "Gracias por su tiempo.",
            "Espero que esté bien.",
            "Quería hacer seguimiento sobre",
            "Me pongo en contacto con usted",
            "No dude en",
            "Quedo a la espera de",
            "Agradezco su",
            "Me complace informarle que",
            "Quería consultar sobre",
            "Muchas gracias por",
            "Realmente aprecio",
            "Estoy agradecido por"
        ]
        
        training_data = all_templates + email_patterns
        self.model.train(training_data)
        self.trained = True
        
        print("✅ Modelo entrenado con plantillas de correo")
    
    def determine_email_type(self, context: str) -> str:
        """Determine the type of email based on context"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ["reunión", "meeting", "cita", "appointment", "encuentro", "coordin"]):
            return "meeting_request"
        elif any(word in context_lower for word in ["gracias", "thank", "agradecer", "appreciate", "agradecimiento"]):
            return "thank_you"
        elif any(word in context_lower for word in ["seguimiento", "follow", "check", "update", "consulta", "recordatorio"]):
            return "follow_up"
        elif any(word in context_lower for word in ["negocio", "business", "propuesta", "proposal", "comercial", "servicio", "producto"]):
            return "business_proposal"
        else:
            return "general"
    
    def customize_template(self, template: str, context: str, tone: str = "formal") -> str:
        """Customize template with context-specific details"""
        
        # Replace placeholders with context-appropriate content
        customized = template
        
        # Replace [tema] with context
        if "[tema]" in customized:
            customized = customized.replace("[tema]", context)
        
        # Replace [propósito] with context
        if "[propósito]" in customized:
            customized = customized.replace("[propósito]", context)
        
        # Replace [día] and [hora] with suggestions
        if "[día]" in customized:
            days = ["el próximo lunes", "el martes", "el miércoles", "el jueves", "el viernes", "la próxima semana"]
            customized = customized.replace("[día]", random.choice(days))
        
        if "[hora]" in customized:
            hours = ["10:00 AM", "2:00 PM", "3:00 PM", "4:00 PM", "11:00 AM", "1:00 PM"]
            customized = customized.replace("[hora]", random.choice(hours))
        
        # Replace [fecha] with relative date
        if "[fecha]" in customized:
            dates = ["la semana pasada", "hace unos días", "recientemente", "el otro día"]
            customized = customized.replace("[fecha]", random.choice(dates))
        
        # Replace [acción] with context-appropriate action
        if "[acción]" in customized:
            actions = ["su tiempo", "su consideración", "su apoyo", "su ayuda", "su colaboración"]
            customized = customized.replace("[acción]", random.choice(actions))
        
        # Replace [detalle específico] with context
        if "[detalle específico]" in customized:
            customized = customized.replace("[detalle específico]", context)
        
        # Replace [Impacto] with impact statement
        if "[Impacto]" in customized:
            impacts = ["Esto ha sido muy valioso para nosotros.", "Su contribución ha sido fundamental.", "Esto nos ha ayudado mucho."]
            customized = customized.replace("[Impacto]", random.choice(impacts))
        
        # Replace [interacción futura] with future interaction
        if "[interacción futura]" in customized:
            interactions = ["trabajar juntos nuevamente", "colaborar en el futuro", "mantener nuestra relación profesional"]
            customized = customized.replace("[interacción futura]", random.choice(interactions))
        
        # Replace [lo que hicieron] with context
        if "[lo que hicieron]" in customized:
            customized = customized.replace("[lo que hicieron]", context)
        
        # Replace [Por qué importa] with importance statement
        if "[Por qué importa]" in customized:
            importance = ["Su contribución ha sido fundamental para nuestro proyecto.", "Su apoyo ha sido invaluable.", "Su participación ha sido clave."]
            customized = customized.replace("[Por qué importa]", random.choice(importance))
        
        # Replace [apoyo/ayuda] with appropriate term
        if "[apoyo/ayuda]" in customized:
            support = ["apoyo", "ayuda", "colaboración", "participación", "contribución"]
            customized = customized.replace("[apoyo/ayuda]", random.choice(support))
        
        # Replace [acción específica] with context
        if "[acción específica]" in customized:
            customized = customized.replace("[acción específica]", context)
        
        # Replace [Cómo ayudó] with help description
        if "[Cómo ayudó]" in customized:
            help_desc = ["Su participación ha sido fundamental.", "Su contribución ha sido invaluable.", "Su apoyo ha sido clave."]
            customized = customized.replace("[Cómo ayudó]", random.choice(help_desc))
        
        # Replace [apoyo] with support term
        if "[apoyo]" in customized:
            support_terms = ["apoyo", "ayuda", "colaboración", "participación"]
            customized = customized.replace("[apoyo]", random.choice(support_terms))
        
        # Replace [Estado actual] with status
        if "[Estado actual]" in customized:
            status = ["Necesito una actualización sobre el progreso.", "Quisiera conocer el estado actual del proyecto.", "Me gustaría saber cómo van las cosas."]
            customized = customized.replace("[Estado actual]", random.choice(status))
        
        # Replace [Recordatorio] with reminder
        if "[Recordatorio]" in customized:
            reminder = "Necesito recordarle sobre este asunto importante."
            customized = customized.replace("[Recordatorio]", reminder)
        
        # Replace [próximo paso] with next step
        if "[próximo paso]" in customized:
            next_steps = ["el proyecto", "nuestros objetivos", "el plan establecido"]
            customized = customized.replace("[próximo paso]", random.choice(next_steps))
        
        # Replace [Progreso] with progress
        if "[Progreso]" in customized:
            progress = ["Necesito una actualización sobre el progreso.", "Quisiera conocer el estado actual.", "Me gustaría saber cómo van las cosas."]
            customized = customized.replace("[Progreso]", random.choice(progress))
        
        # Replace [propuesta] with proposal
        if "[propuesta]" in customized:
            customized = customized.replace("[propuesta]", context)
        
        # Replace [Detalles de la propuesta] with details
        if "[Detalles de la propuesta]" in customized:
            details = "Esta propuesta incluye todos los detalles necesarios para su consideración."
            customized = customized.replace("[Detalles de la propuesta]", details)
        
        # Replace [servicio/producto] with service/product
        if "[servicio/producto]" in customized:
            services = ["servicio", "producto", "solución", "propuesta"]
            customized = customized.replace("[servicio/producto]", random.choice(services))
        
        # Replace [Beneficios] with benefits
        if "[Beneficios]" in customized:
            benefits = "Esta propuesta ofrece múltiples beneficios para su organización."
            customized = customized.replace("[Beneficios]", benefits)
        
        # Replace [asunto] with subject
        if "[asunto]" in customized:
            customized = customized.replace("[asunto]", context)
        
        # Replace [objetivo] with objective
        if "[objetivo]" in customized:
            objectives = ["nuestro proyecto", "sus necesidades", "sus objetivos", "su proyecto"]
            customized = customized.replace("[objetivo]", random.choice(objectives))
        
        # Replace [Información clave] with key information
        if "[Información clave]" in customized:
            key_info = "La propuesta incluye toda la información necesaria para su evaluación."
            customized = customized.replace("[Información clave]", key_info)
        
        # Replace [Detalles] with details
        if "[Detalles]" in customized:
            details = "Los detalles completos se incluyen en la propuesta adjunta."
            customized = customized.replace("[Detalles]", details)
        
        # Replace [Explicación] with explanation
        if "[Explicación]" in customized:
            explanation = "Este asunto requiere su atención y consideración."
            customized = customized.replace("[Explicación]", explanation)
        
        # Replace [Información] with information
        if "[Información]" in customized:
            information = "Toda la información relevante se encuentra en los documentos adjuntos."
            customized = customized.replace("[Información]", information)
        
        return customized
    
    def generate_email(self, context: str, tone: str = "formal", recipient: str = "[Nombre]", 
                      sender: str = "[Tu Nombre]", subject: str = "") -> str:
        """Generate a complete email"""
        
        # Train model if not already trained
        if not self.trained:
            self.train_model()
        
        # Determine email type
        email_type = self.determine_email_type(context)
        
        # Select appropriate template
        templates = self.email_templates[email_type]
        template = random.choice(templates)
        
        # Customize template
        content = self.customize_template(template, context, tone)
        
        # Format email
        email = self.format_email(content, recipient, sender, subject, tone)
        
        return email
    
    def format_email(self, content: str, recipient: str = "[Nombre]", sender: str = "[Tu Nombre]", 
                    subject: str = "", tone: str = "formal") -> str:
        """Format the generated content into a proper email"""
        
        # Clean content
        content = content.strip()
        
        # Add email structure
        email = f"Asunto: {subject}\n\n"
        
        # Replace placeholders
        content = content.replace("[Nombre]", recipient)
        content = content.replace("[Tu Nombre]", sender)
        
        # Add main content
        email += f"{content}\n\n"
        
        # Add closing if not present
        if "Atentamente" not in content and "Saludos" not in content and "Saludos cordiales" not in content:
            if tone == "casual":
                email += f"Saludos,\n{sender}"
            else:
                email += f"Atentamente,\n{sender}"
        
        return email
    
    def generate_multiple_emails(self, context: str, tones: List[str] = None, 
                               recipient: str = "[Nombre]", sender: str = "[Tu Nombre]", 
                               subject: str = "") -> Dict[str, str]:
        """Generate emails in multiple tones"""
        
        if tones is None:
            tones = ["formal", "business", "casual"]
        
        emails = {}
        for tone in tones:
            emails[tone] = self.generate_email(context, tone, recipient, sender, subject)
        
        return emails
    
    def save_emails(self, emails: Dict[str, str], filename: str = None):
        """Save generated emails to a file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"correos_generados_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CORREOS ELECTRÓNICOS GENERADOS POR ULTRAEFFICIENTLLM\n")
            f.write("=" * 80 + "\n\n")
            
            for context_name, context_emails in emails.items():
                if isinstance(context_emails, dict):
                    # Multiple emails per context
                    f.write(f"📝 CONTEXTO: {context_name}\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for tone, email in context_emails.items():
                        f.write(f"🎯 TONO: {tone.upper()}\n")
                        f.write("-" * 40 + "\n")
                        f.write(email)
                        f.write("\n\n" + "-" * 40 + "\n\n")
                    
                    f.write("=" * 80 + "\n\n")
                else:
                    # Single email
                    f.write(f"🎯 TONO: {context_name.upper()}\n")
                    f.write("-" * 40 + "\n")
                    f.write(context_emails)
                    f.write("\n\n" + "=" * 80 + "\n\n")
        
        print(f"💾 Correos guardados en: {filename}")
        return filename


def demo_simple_email_generation():
    """Demo of simple email generation capabilities"""
    
    print("🚀 DEMOSTRACIÓN: GENERADOR SIMPLE DE CORREOS")
    print("=" * 60)
    
    generator = SimpleEmailGenerator()
    
    # Sample contexts
    contexts = [
        "Solicitar una reunión para discutir el proyecto de marketing digital",
        "Agradecer por la entrevista de trabajo realizada ayer en la empresa TechCorp",
        "Seguimiento sobre la propuesta de servicios enviada la semana pasada",
        "Informar sobre el retraso en la entrega del producto debido a problemas de logística",
        "Invitar a un evento de networking que se realizará el próximo mes"
    ]
    
    tones = ["formal", "business", "casual"]
    
    print("\n📧 Generando correos de ejemplo...")
    
    all_emails = {}
    
    for i, context in enumerate(contexts, 1):
        print(f"\n📝 Contexto {i}: {context}")
        
        emails = generator.generate_multiple_emails(
            context, tones, 
            recipient="María García",
            sender="Carlos Rodríguez",
            subject=f"Re: {context[:30]}..."
        )
        
        all_emails[f"Contexto_{i}"] = emails
        
        # Show one example
        print(f"📧 Ejemplo (formal):")
        print("-" * 40)
        print(emails["formal"])
        print("=" * 60)
    
    # Save all emails
    filename = generator.save_emails(all_emails, "correos_simples.txt")
    print(f"\n💾 Todos los correos guardados en: {filename}")
    
    return all_emails


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Email Generator using UltraEfficientLLM")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--context", type=str, help="Email context")
    parser.add_argument("--tone", type=str, default="formal", 
                       choices=["formal", "business", "casual"],
                       help="Email tone")
    parser.add_argument("--recipient", type=str, default="[Nombre]", help="Recipient name")
    parser.add_argument("--sender", type=str, default="[Tu Nombre]", help="Sender name")
    parser.add_argument("--subject", type=str, default="", help="Email subject")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_simple_email_generation()
    elif args.context:
        generator = SimpleEmailGenerator()
        email = generator.generate_email(
            args.context, args.tone, args.recipient, args.sender, args.subject
        )
        print(f"\n📧 CORREO GENERADO ({args.tone.upper()}):")
        print("=" * 60)
        print(email)
        print("=" * 60)
    else:
        print("📧 GENERADOR SIMPLE DE CORREOS CON ULTRAEFFICIENTLLM")
        print("=" * 60)
        print("Uso:")
        print("  python simple_email_generator.py --demo")
        print("  python simple_email_generator.py --context 'Tu contexto aquí' --tone formal")
        print("\nEjemplos:")
        print("  python simple_email_generator.py --context 'Solicitar reunión' --tone formal")
        print("  python simple_email_generator.py --context 'Agradecer entrevista' --tone formal") 