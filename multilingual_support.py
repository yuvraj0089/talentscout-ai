"""
Multilingual Support Module for TalentScout
Provides language detection, translation, and localized responses
"""

from typing import Dict, Optional, Tuple
import streamlit as st
from dataclasses import dataclass

@dataclass
class LanguageConfig:
    """Configuration for supported languages."""
    code: str
    name: str
    flag: str
    rtl: bool = False  # Right-to-left languages

class MultilingualManager:
    """Manages multilingual support for the application."""
    
    def __init__(self):
        self.supported_languages = {
            'en': LanguageConfig('en', 'English', '🇺🇸'),
            'es': LanguageConfig('es', 'Español', '🇪🇸'),
            'fr': LanguageConfig('fr', 'Français', '🇫🇷'),
            'de': LanguageConfig('de', 'Deutsch', '🇩🇪'),
            'it': LanguageConfig('it', 'Italiano', '🇮🇹'),
            'pt': LanguageConfig('pt', 'Português', '🇵🇹'),
            'zh': LanguageConfig('zh', '中文', '🇨🇳'),
            'ja': LanguageConfig('ja', '日本語', '🇯🇵'),
            'ko': LanguageConfig('ko', '한국어', '🇰🇷'),
            'ar': LanguageConfig('ar', 'العربية', '🇸🇦', rtl=True),
            'hi': LanguageConfig('hi', 'हिन्दी', '🇮🇳'),
            'ru': LanguageConfig('ru', 'Русский', '🇷🇺')
        }
        
        self.translations = {
            'en': {
                'welcome_message': "Welcome to TalentScout! 👋 I'm your AI Hiring Assistant, and I'll be helping you with the initial screening process.",
                'name_question': "Could you please tell me your full name?",
                'email_question': "Great! Could you please provide your email address?",
                'phone_question': "Thank you! What's the best phone number to reach you?",
                'experience_question': "How many years of professional experience do you have?",
                'position_question': "What position(s) are you interested in?",
                'location_question': "What is your current location?",
                'tech_stack_question': "Please list the technologies you're proficient in (programming languages, frameworks, databases, tools, etc.):",
                'technical_questions_intro': "Great! Here are some technical questions based on your expertise:",
                'thank_you': "Thank you for completing the initial screening! Our team will review your information and get back to you soon.",
                'invalid_email': "Please provide a valid email address.",
                'invalid_phone': "Please provide a valid phone number.",
                'invalid_experience': "Please provide your experience in years (e.g., 5 or 2.5).",
                'goodbye': "Thank you for your time! We appreciate you taking the time to speak with us. Have a great day! 👋"
            },
            'es': {
                'welcome_message': "¡Bienvenido a TalentScout! 👋 Soy tu Asistente de Contratación IA y te ayudaré con el proceso de selección inicial.",
                'name_question': "¿Podrías decirme tu nombre completo?",
                'email_question': "¡Excelente! ¿Podrías proporcionar tu dirección de correo electrónico?",
                'phone_question': "¡Gracias! ¿Cuál es el mejor número de teléfono para contactarte?",
                'experience_question': "¿Cuántos años de experiencia profesional tienes?",
                'position_question': "¿En qué puesto(s) estás interesado?",
                'location_question': "¿Cuál es tu ubicación actual?",
                'tech_stack_question': "Por favor, enumera las tecnologías en las que eres competente (lenguajes de programación, frameworks, bases de datos, herramientas, etc.):",
                'technical_questions_intro': "¡Excelente! Aquí tienes algunas preguntas técnicas basadas en tu experiencia:",
                'thank_you': "¡Gracias por completar la selección inicial! Nuestro equipo revisará tu información y se pondrá en contacto contigo pronto.",
                'invalid_email': "Por favor, proporciona una dirección de correo electrónico válida.",
                'invalid_phone': "Por favor, proporciona un número de teléfono válido.",
                'invalid_experience': "Por favor, proporciona tu experiencia en años (ej., 5 o 2.5).",
                'goodbye': "¡Gracias por tu tiempo! Apreciamos que hayas dedicado tiempo a hablar con nosotros. ¡Que tengas un gran día! 👋"
            },
            'fr': {
                'welcome_message': "Bienvenue chez TalentScout ! 👋 Je suis votre Assistant de Recrutement IA et je vais vous aider avec le processus de sélection initial.",
                'name_question': "Pourriez-vous me dire votre nom complet ?",
                'email_question': "Parfait ! Pourriez-vous fournir votre adresse e-mail ?",
                'phone_question': "Merci ! Quel est le meilleur numéro de téléphone pour vous joindre ?",
                'experience_question': "Combien d'années d'expérience professionnelle avez-vous ?",
                'position_question': "À quel(s) poste(s) êtes-vous intéressé(e) ?",
                'location_question': "Quelle est votre localisation actuelle ?",
                'tech_stack_question': "Veuillez énumérer les technologies que vous maîtrisez (langages de programmation, frameworks, bases de données, outils, etc.) :",
                'technical_questions_intro': "Parfait ! Voici quelques questions techniques basées sur votre expertise :",
                'thank_you': "Merci d'avoir complété la sélection initiale ! Notre équipe examinera vos informations et vous recontactera bientôt.",
                'invalid_email': "Veuillez fournir une adresse e-mail valide.",
                'invalid_phone': "Veuillez fournir un numéro de téléphone valide.",
                'invalid_experience': "Veuillez indiquer votre expérience en années (ex., 5 ou 2.5).",
                'goodbye': "Merci pour votre temps ! Nous apprécions que vous ayez pris le temps de parler avec nous. Passez une excellente journée ! 👋"
            },
            'de': {
                'welcome_message': "Willkommen bei TalentScout! 👋 Ich bin Ihr KI-Recruiting-Assistent und helfe Ihnen beim ersten Auswahlverfahren.",
                'name_question': "Könnten Sie mir bitte Ihren vollständigen Namen nennen?",
                'email_question': "Großartig! Könnten Sie bitte Ihre E-Mail-Adresse angeben?",
                'phone_question': "Danke! Wie lautet die beste Telefonnummer, um Sie zu erreichen?",
                'experience_question': "Wie viele Jahre Berufserfahrung haben Sie?",
                'position_question': "An welcher/welchen Position(en) sind Sie interessiert?",
                'location_question': "Wo befinden Sie sich derzeit?",
                'tech_stack_question': "Bitte listen Sie die Technologien auf, in denen Sie kompetent sind (Programmiersprachen, Frameworks, Datenbanken, Tools, etc.):",
                'technical_questions_intro': "Großartig! Hier sind einige technische Fragen basierend auf Ihrer Expertise:",
                'thank_you': "Vielen Dank für das Abschließen der ersten Auswahl! Unser Team wird Ihre Informationen prüfen und sich bald bei Ihnen melden.",
                'invalid_email': "Bitte geben Sie eine gültige E-Mail-Adresse an.",
                'invalid_phone': "Bitte geben Sie eine gültige Telefonnummer an.",
                'invalid_experience': "Bitte geben Sie Ihre Erfahrung in Jahren an (z.B. 5 oder 2.5).",
                'goodbye': "Vielen Dank für Ihre Zeit! Wir schätzen es, dass Sie sich die Zeit genommen haben, mit uns zu sprechen. Haben Sie einen großartigen Tag! 👋"
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text."""
        try:
            from langdetect import detect
            detected = detect(text)
            return detected if detected in self.supported_languages else 'en'
        except:
            # Fallback: simple keyword detection
            return self._detect_language_simple(text)
    
    def _detect_language_simple(self, text: str) -> str:
        """Simple language detection based on common words."""
        text_lower = text.lower()
        
        # Spanish indicators
        if any(word in text_lower for word in ['hola', 'gracias', 'por favor', 'sí', 'no', 'español']):
            return 'es'
        
        # French indicators
        if any(word in text_lower for word in ['bonjour', 'merci', 'oui', 'non', 'français', 'je suis']):
            return 'fr'
        
        # German indicators
        if any(word in text_lower for word in ['hallo', 'danke', 'ja', 'nein', 'deutsch', 'ich bin']):
            return 'de'
        
        # Default to English
        return 'en'
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language using fallback method."""
        # For Python 3.13 compatibility, we use pre-translated content
        # In production, you could integrate with Azure Translator, AWS Translate, etc.

        # Simple keyword-based translation for common phrases
        if target_language == 'es' and 'welcome' in text.lower():
            return text.replace('Welcome', 'Bienvenido').replace('welcome', 'bienvenido')
        elif target_language == 'fr' and 'welcome' in text.lower():
            return text.replace('Welcome', 'Bienvenue').replace('welcome', 'bienvenue')
        elif target_language == 'de' and 'welcome' in text.lower():
            return text.replace('Welcome', 'Willkommen').replace('welcome', 'willkommen')

        # Fallback: return original text
        return text
    
    def get_translation(self, key: str, language: str = 'en') -> str:
        """Get translated text for a given key."""
        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        elif key in self.translations['en']:
            return self.translations['en'][key]
        else:
            return key
    
    def get_language_selector(self) -> str:
        """Create language selector for Streamlit."""
        language_options = {
            f"{config.flag} {config.name}": config.code 
            for config in self.supported_languages.values()
        }
        
        selected_display = st.selectbox(
            "🌍 Select Language / Seleccionar Idioma / Choisir la Langue",
            options=list(language_options.keys()),
            index=0
        )
        
        return language_options[selected_display]
    
    def get_rtl_css(self, language: str) -> str:
        """Get CSS for right-to-left languages."""
        if language in self.supported_languages and self.supported_languages[language].rtl:
            return """
            <style>
            .stApp {
                direction: rtl;
                text-align: right;
            }
            .stTextInput > div > div > input {
                text-align: right;
            }
            </style>
            """
        return ""
    
    def format_message_with_language(self, message: str, language: str) -> str:
        """Format message with language-specific styling."""
        if language in self.supported_languages:
            flag = self.supported_languages[language].flag
            return f"{flag} {message}"
        return message
    
    def get_language_specific_prompts(self, language: str) -> Dict[str, str]:
        """Get language-specific prompts for technical questions."""
        base_prompt = """Based on the candidate's tech stack: {tech_stack}
Generate 3-5 relevant technical questions in {language} that:
1. Assess fundamental understanding
2. Test practical application knowledge  
3. Evaluate problem-solving abilities
Format the response as a numbered list of questions in {language}."""
        
        language_names = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'ru': 'Russian'
        }
        
        language_name = language_names.get(language, 'English')
        
        return {
            'tech_assessment_prompt': base_prompt.format(
                tech_stack='{tech_stack}',
                language=language_name
            )
        }

# Global instance
multilingual_manager = MultilingualManager()
