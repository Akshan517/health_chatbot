import google.generativeai as genai
from langdetect import detect, DetectorFactory
from googletrans import Translator
from datetime import datetime
import os

# Set seed for consistent language detection
DetectorFactory.seed = 0

class GeminiResponseGenerator:
    """Generate natural, multilingual health chatbot responses using Gemini Pro API"""
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'pt': 'Portuguese',
        'it': 'Italian',
        'ja': 'Japanese',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)',
        'ru': 'Russian',
        'ar': 'Arabic',
        'ta': 'Tamil',
        'te': 'Telugu',
        'ur': 'Urdu'
    }
    
    def __init__(self, api_key=None):
        """Initialize Gemini Pro with API key"""
        self.gemini_available = False
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.chat = self.model.start_chat(history=[])
                self.gemini_available = True
                print("✅ Gemini Pro connected")
            except Exception as e:
                print(f"⚠️ Gemini Pro failed: {e}")
        
        # Always try to initialize translator
        try:
            self.translator = Translator()
            print("✅ Google Translate initialized")
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")
            self.translator = None
    
    @staticmethod
    def detect_language(text):
        """Detect the language of input text"""
        try:
            lang = detect(text)
            return lang
        except:
            return 'en'  # Default to English if detection fails
    
    @staticmethod
    def get_language_name(lang_code):
        """Get full language name from code"""
        return GeminiResponseGenerator.SUPPORTED_LANGUAGES.get(lang_code, 'English')
    
    def translate_to_english(self, text, source_lang=None):
        """
        Translate text to English for ML processing
        
        Args:
            text: Text to translate
            source_lang: Source language code (auto-detect if None)
        
        Returns:
            Translated text in English
        """
        if not self.translator:
            return text  # Return original if translator not available
            
        if not source_lang:
            source_lang = self.detect_language(text)
        
        # If already English, return as-is
        if source_lang == 'en':
            return text
        
        try:
            translation = self.translator.translate(text, src=source_lang, dest='en')
            return translation.text
        except Exception as e:
            print(f"Translation failed: {e}")
            return text  # Return original text if translation fails
    
    def process_multilingual_symptoms(self, user_input):
        """
        Process user symptoms with translation support
        
        Args:
            user_input: User's symptom description in any language
        
        Returns:
            Tuple of (translated_symptoms, original_language)
        """
        # Detect original language
        original_lang = self.detect_language(user_input)
        
        # Translate to English for ML processing
        translated_symptoms = self.translate_to_english(user_input, original_lang)
        
        return translated_symptoms, original_lang
    
    def generate_health_response(self, disease, confidence, precautions, user_language='en'):
        """
        Generate a natural health response using Gemini Pro
        
        Args:
            disease: Predicted disease name
            confidence: Confidence percentage
            precautions: Precautions/care guidelines
            user_language: Language code for response
        
        Returns:
            Natural language response in user's language
        """
        
        language_name = self.get_language_name(user_language)
        
        # Create a detailed prompt for Gemini Pro
        prompt = f"""You are a helpful health assistant chatbot. Generate a natural, conversational response for a patient.

Patient's predicted condition: {disease}
Confidence level: {confidence}%
Recommended precautions: {precautions}

Generate response in {language_name}. The response should:
1. Be conversational and empathetic (not robotic)
2. Clearly mention the predicted condition and confidence level in natural language
3. Include the precautions in an easy-to-follow format
4. Add a disclaimer that this is AI-generated and they should consult a healthcare professional
5. Be concise but informative (2-3 paragraphs)
6. Use relevant emojis appropriately

Provide only the response message, no additional commentary."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback response if API fails
            return self._fallback_response(disease, confidence, precautions, user_language)
    
    def generate_multilingual_response(self, predictions, detected_language='en'):
        """
        Generate a complete response with primary and secondary diagnoses
        
        Args:
            predictions: List of prediction dictionaries with disease, confidence, precautions
            detected_language: Detected language code
        
        Returns:
            Natural language response
        """
        
        if not predictions:
            return "I apologize, but I couldn't analyze the symptoms provided. Please try again with more details."
        
        primary = predictions[0]
        
        # Build context for Gemini with all predictions
        predictions_text = f"Primary prediction: {primary['disease']} ({primary['confidence']}% confidence)"
        
        if len(predictions) > 1:
            secondary = predictions[1]
            predictions_text += f"\nSecondary possibility: {secondary['disease']} ({secondary['confidence']}% confidence)"
            precautions_text = f"Primary precautions: {primary['precautions']}\nSecondary precautions: {secondary['precautions']}"
        else:
            precautions_text = f"Recommended precautions: {primary['precautions']}"
        
        language_name = self.get_language_name(detected_language)
        
        prompt = f"""You are a compassionate health chatbot. Generate a natural, conversational health assessment response.

{predictions_text}

{precautions_text}

Instructions:
1. Generate response in {language_name}
2. Be empathetic and reassuring while remaining accurate
3. Present the diagnosis in a conversational way (not as structured data)
4. Include practical, easy-to-follow advice
5. If there's a secondary diagnosis, mention it as an additional consideration
6. Add a strong medical disclaimer encouraging consultation with a healthcare professional
7. Keep tone warm and helpful (not scary or overly clinical)
8. Use 2-3 paragraphs, add relevant emojis sparingly
9. Do NOT include confidence percentages in a clinical way - integrate naturally

Provide only the response message."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API failed: {e}")
            return self._fallback_response(
                primary['disease'], 
                primary['confidence'], 
                primary['precautions'], 
                detected_language
            )
    
    def generate_welcome_message(self, user_language='en'):
        """Generate a personalized welcome message in user's language"""
        
        language_name = self.get_language_name(user_language)
        
        prompt = f"""Create a warm, welcoming greeting message for a health chatbot in {language_name}.

The message should:
1. Welcome the user warmly
2. Briefly explain what the chatbot does
3. Ask them to describe their symptoms with an example
4. Be concise but friendly (2-3 sentences with emojis)
5. Encourage them to be specific about their symptoms

Provide only the message text."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return self._default_welcome(user_language)
    
    def generate_clarification_message(self, user_language='en'):
        """Generate a request for more symptom details in user's language"""
        
        language_name = self.get_language_name(user_language)
        
        prompt = f"""Generate a polite request for more symptom details in {language_name}.

The message should:
1. Acknowledge their input
2. Ask for more specific symptoms
3. Provide an example of what to share
4. Be friendly and encouraging
5. Be concise (1-2 sentences)

Provide only the message text."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return self._default_clarification(user_language)
    
    def _fallback_response(self, disease, confidence, precautions, language):
        """Fallback response if Gemini Pro fails"""
        responses = {
            'en': f"Based on your symptoms, you may have {disease} (confidence: {confidence}%). Please take the following precautions: {precautions}\n\n⚠️ This is an AI-generated assessment. Please consult a healthcare professional for accurate diagnosis.",
            'hi': f"आपके लक्षणों के आधार पर, आपको {disease} हो सकता है ({confidence}% आत्मविश्वास)। कृपया निम्नलिखित सावधानियां बरतें: {precautions}\n\n⚠️ यह एक AI-जनित आकलन है। सटीक निदान के लिए कृपया एक स्वास्थ्य सेवा पेशेवर से परामर्श करें।",
            'es': f"Según sus síntomas, podría tener {disease} (confianza: {confidence}%). Por favor tome las siguientes precauciones: {precautions}\n\n⚠️ Esta es una evaluación generada por IA. Consulte a un profesional de la salud para un diagnóstico preciso.",
        }
        return responses.get(language, responses['en'])
    
    def _default_welcome(self, language):
        """Default welcome messages"""
        welcomes = {
            'en': "👋 Welcome to Health ChatBot! I'm here to help analyze your symptoms.\n\nPlease describe your symptoms (e.g., fever, cough, headache) and I'll provide guidance.",
            'hi': "👋 स्वास्थ्य चैटबॉट में आपका स्वागत है! मैं आपके लक्षणों का विश्लेषण करने में मदद करूंगा।\n\nकृपया अपने लक्षण बताएं (जैसे, बुखार, खांसी, सिरदर्द)।",
            'es': "👋 ¡Bienvenido al Chatbot de Salud! Estoy aquí para ayudarte a analizar tus síntomas.\n\nDescribe tus síntomas (por ejemplo, fiebre, tos, dolor de cabeza).",
        }
        return welcomes.get(language, welcomes['en'])
    
    def _default_clarification(self, language):
        """Default clarification messages"""
        clarifications = {
            'en': "Could you please provide more details about your symptoms? For example: intensity, duration, or specific locations.",
            'hi': "कृपया अपने लक्षणों के बारे में अधिक विवरण प्रदान करें। उदाहरण के लिए: गंभीरता, अवधि, या विशिष्ट स्थान।",
            'es': "¿Podrías proporcionar más detalles sobre tus síntomas? Por ejemplo: intensidad, duración o ubicación específica.",
        }
        return clarifications.get(language, clarifications['en'])


# Initialize generator
def get_gemini_generator(api_key=None):
    """Factory function to get Gemini generator instance"""
    return GeminiResponseGenerator(api_key)
