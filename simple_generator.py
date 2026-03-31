import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleMultilingualGenerator:
    """Simple multilingual health chatbot with basic translation support"""

    # Basic translations for common symptoms
    SYMPTOM_TRANSLATIONS = {
        'itching': {
            'hi': 'खुजली',
            'te': 'దురద',
            'es': 'picazón',
            'fr': 'démangeaison'
        },
        'skin rash': {
            'hi': 'त्वचा पर चकत्ते',
            'te': 'చర్మంపై దద్దుర్లు',
            'es': 'erupción en la piel',
            'fr': 'éruption cutanée'
        },
        'fever': {
            'hi': 'बुखार',
            'te': 'జ్వరం',
            'es': 'fiebre',
            'fr': 'fièvre'
        },
        'cough': {
            'hi': 'खांसी',
            'te': 'దగ్గు',
            'es': 'tos',
            'fr': 'toux'
        },
        'headache': {
            'hi': 'सिरदर्द',
            'te': 'తలనొప్పి',
            'es': 'dolor de cabeza',
            'fr': 'mal de tête'
        }
    }

    # Language detection keywords
    LANGUAGE_KEYWORDS = {
        'hi': ['मुझे', 'है', 'हैं', 'खुजली', 'त्वचा', 'चकत्ते'],
        'te': ['నాకు', 'దురద', 'చర్మం', 'దద్దుర్లు', 'ఉన్నాయి'],
        'es': ['tengo', 'picazón', 'piel', 'erupción'],
        'fr': ['j\'ai', 'démangeaison', 'éruption']
    }

    def __init__(self):
        self.gemini_available = False
        # Try to import Gemini if API key is available
        try:
            import google.generativeai as genai
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.gemini_available = True
                print("✅ Gemini Pro connected")
            else:
                print("⚠️ No GEMINI_API_KEY found")
        except Exception as e:
            print(f"⚠️ Gemini Pro not available: {e}")

    @staticmethod
    def detect_language(text):
        """Simple language detection based on keywords"""
        text_lower = text.lower()

        for lang, keywords in SimpleMultilingualGenerator.LANGUAGE_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                return lang

        return 'en'  # Default to English

    def translate_to_english(self, text):
        """Simple translation using predefined mappings without word boundaries"""
        detected_lang = self.detect_language(text)

        if detected_lang == 'en':
            return text

        # Create a mapping of full phrases and individual words for translation
        translation_entries = []  # List of (translated_phrase, english_word, word_count)
        
        for symptom, translations_dict in self.SYMPTOM_TRANSLATIONS.items():
            if detected_lang in translations_dict:
                translated_phrase = translations_dict[detected_lang]
                word_count = len(translated_phrase.split())
                translation_entries.append((translated_phrase, symptom, word_count))
        
        # Sort by word count (longest phrases first) to match multi-word phrases before single words
        translation_entries.sort(key=lambda x: x[2], reverse=True)
        
        # Replace phrases and words in order (without word boundaries, which don't work well with non-Latin scripts)
        result = text
        for translated_phrase, english_word, _ in translation_entries:
            # Simple string replacement - works better with non-Latin scripts
            result = result.replace(translated_phrase, english_word)
        
        return result

    def generate_response(self, predictions, language='en'):
        """Generate a response in the specified language"""
        if not predictions:
            return self._get_message("no_analysis", language)

        primary = predictions[0]

        if self.gemini_available:
            try:
                return self._generate_gemini_response(predictions, language)
            except:
                pass  # Fall back to template

        return self._generate_template_response(predictions, language)

    def _generate_gemini_response(self, predictions, language):
        """Generate response using Gemini Pro"""
        primary = predictions[0]

        prompt = f"""Generate a natural, conversational health response in {self._get_language_name(language)}.

Disease: {primary['disease']}
Confidence: {primary['confidence']}%
Precautions: {primary['precautions']}

Make it empathetic, informative, and include a medical disclaimer."""

        response = self.model.generate_content(prompt)
        return response.text

    def _generate_template_response(self, predictions, language):
        """Generate response using templates"""
        primary = predictions[0]

        templates = {
            'en': f"Based on your symptoms, you may have {primary['disease']} (confidence: {primary['confidence']}%). Please take the following precautions: {primary['precautions']}\n\n⚠️ This is an AI-generated assessment. Please consult a healthcare professional for accurate diagnosis.",
            'hi': f"आपके लक्षणों के आधार पर, आपको {primary['disease']} हो सकता है ({primary['confidence']}% आत्मविश्वास)। कृपया निम्नलिखित सावधानियां बरतें: {primary['precautions']}\n\n⚠️ यह एक AI-जनित आकलन है। सटीक निदान के लिए कृपया एक स्वास्थ्य सेवा पेशेवर से परामर्श करें।",
            'te': f"మీ లక్షణాల ప్రకారం, మీకు {primary['disease']} ఉండవచ్చు ({primary['confidence']}% నమ్మకం)। దయచేసి కింది జాగ్రత్తలు తీసుకోండి: {primary['precautions']}\n\n⚠️ ఇది AI-ఉత్పత్తి చేసిన మూల్యాంకనం. ఖచ్చితమైన నిర్ధారణ కోసం దయచేసి ఆరోగ్య సేవా నిపుణుడిని సంప్రదించండి।",
            'es': f"Según sus síntomas, podría tener {primary['disease']} (confianza: {primary['confidence']}%). Por favor tome las siguientes precauciones: {primary['precautions']}\n\n⚠️ Esta es una evaluación generada por IA. Consulte a un profesional de la salud para un diagnóstico preciso.",
            'fr': f"Selon vos symptômes, vous pourriez avoir {primary['disease']} (confiance: {primary['confidence']}%). Veuillez prendre les précautions suivantes: {primary['precautions']}\n\n⚠️ Il s'agit d'une évaluation générée par IA. Veuillez consulter un professionnel de la santé pour un diagnostic précis."
        }

        return templates.get(language, templates['en'])

    def _get_language_name(self, lang_code):
        """Get full language name"""
        names = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu',
            'es': 'Spanish',
            'fr': 'French'
        }
        return names.get(lang_code, 'English')

    def _get_message(self, message_type, language):
        """Get localized messages"""
        messages = {
            'no_analysis': {
                'en': "I apologize, but I couldn't analyze the symptoms provided. Please try again with more details.",
                'hi': "क्षमा करें, लेकिन मैं दिए गए लक्षणों का विश्लेषण नहीं कर सका। कृपया अधिक विवरण के साथ पुनः प्रयास करें।",
                'te': "క్షమించండి, కానీ నేను అందించిన లక్షణాలను విశ్లేషించలేకపోయాను. దయచేసి మరిన్ని వివరాలతో మళ్లీ ప్రయత్నించండి.",
                'es': "Disculpe, pero no pude analizar los síntomas proporcionados. Por favor, inténtelo de nuevo con más detalles.",
                'fr': "Désolé, mais je n'ai pas pu analyser les symptômes fournis. Veuillez réessayer avec plus de détails."
            }
        }

        return messages.get(message_type, {}).get(language, messages[message_type]['en'])

    def generate_welcome_message(self, language='en'):
        """Generate welcome message"""
        welcomes = {
            'en': "👋 Welcome to Health ChatBot! I'm here to help analyze your symptoms.\n\nPlease describe your symptoms (e.g., fever, cough, headache) and I'll provide guidance.",
            'hi': "👋 स्वास्थ्य चैटबॉट में आपका स्वागत है! मैं आपके लक्षणों का विश्लेषण करने में मदद करूंगा।\n\nकृपया अपने लक्षण बताएं (जैसे, बुखार, खांसी, सिरदर्द)।",
            'te': "👋 ఆరోగ్య చాట్‌బాట్‌కు స్వాగతం! మీ లక్షణాలను విశ్లేషించడంలో నేను సహాయం చేస్తాను.\n\nదయచేసి మీ లక్షణాలను వివరించండి (ఉదా., జ్వరం, దగ్గు, తలనొప్పి)।",
            'es': "👋 ¡Bienvenido al Chatbot de Salud! Estoy aquí para ayudarte a analizar tus síntomas.\n\nDescribe tus síntomas (por ejemplo, fiebre, tos, dolor de cabeza).",
            'fr': "👋 Bienvenue sur le Chatbot Santé ! Je suis là pour vous aider à analyser vos symptômes.\n\nDécrivez vos symptômes (par exemple, fièvre, toux, mal de tête)."
        }
        return welcomes.get(language, welcomes['en'])

    def generate_clarification_message(self, language='en'):
        """Generate clarification message"""
        clarifications = {
            'en': "Could you please provide more details about your symptoms? For example: intensity, duration, or specific locations.",
            'hi': "कृपया अपने लक्षणों के बारे में अधिक विवरण प्रदान करें। उदाहरण के लिए: गंभीरता, अवधि, या विशिष्ट स्थान।",
            'te': "దయచేసి మీ లక్షణాల గురించి మరిన్ని వివరాలు అందించగలరా? ఉదాహరణకు: తీవ్రత, వ్యవధి, లేదా నిర్దిష్ట స్థానాలు.",
            'es': "¿Podrías proporcionar más detalles sobre tus síntomas? Por ejemplo: intensidad, duración o ubicación específica.",
            'fr': "Pourriez-vous fournir plus de détails sur vos symptômes ? Par exemple : intensité, durée ou localisation spécifique."
        }
        return clarifications.get(language, clarifications['en'])