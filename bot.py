import telebot
import joblib
import pandas as pd
import numpy as np
from simple_generator import SimpleMultilingualGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8709729595:AAGxsdavG0eDPq-8vvf9Ix2-JQaAWQQNYpA")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load model and dataset
model = joblib.load("model/best_disease_model.pkl")
df = pd.read_json("data/health_dataset.json")

# Initialize multilingual response generator
try:
    response_gen = SimpleMultilingualGenerator()
    print("✅ Multilingual generator initialized")
except Exception as e:
    print(f"❌ Generator initialization failed: {e}")
    response_gen = None

# Initialize bot
bot = telebot.TeleBot(TOKEN)


def predict_disease(user_input):
    """Predict disease based on user input symptoms"""
    probabilities = model.predict_proba([user_input])[0]
    classes = model.classes_

    top_indices = np.argsort(probabilities)[-2:][::-1]
    results = []

    for index in top_indices:
        disease = classes[index]
        confidence = round(probabilities[index] * 100, 2)
        precautions = df[df["Disease"] == disease]["Precautions"].iloc[0]

        results.append({
            "disease": disease,
            "confidence": confidence,
            "precautions": precautions
        })

    return results


def _generate_fallback_response(predictions):
    """Fallback response when Gemini Pro is not available"""
    response = "🩺 Prediction Results:\n\n"

    for p in predictions:
        response += (
            f"🦠 Disease: {p['disease']}\n"
            f"📊 Confidence: {p['confidence']}%\n"
            f"💊 Precautions: {p['precautions']}\n\n"
        )

    response += "⚠️ As it is an AI generated message, please consult a healthcare professional for accurate diagnosis.\n"
    return response


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command with multilingual welcome"""

    # Initialize user language if not present
    if 'language' not in bot.user_data:
        bot.user_data['language'] = 'en'

    if response_gen:
        welcome_msg = response_gen.generate_welcome_message(bot.user_data['language'])
    else:
        welcome_msg = "👨‍⚕️ Welcome to Health ChatBot!\n\nPlease enter your symptoms like:\nfever, cough, headache"

    bot.reply_to(message, welcome_msg)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle user messages with multilingual responses"""
    user_message = message.text

    # Detect language and translate for processing
    if response_gen:
        detected_lang = response_gen.detect_language(user_message)
        translated_symptoms = response_gen.translate_to_english(user_message)
        print(f"Original: '{user_message}' → Translated: '{translated_symptoms}' (Language: {detected_lang})")
    else:
        translated_symptoms = user_message
        detected_lang = 'en'

    # Update user language preference for consistency
    if 'language' not in bot.user_data:
        bot.user_data['language'] = detected_lang
    else:
        # Use previously detected language for consistency
        detected_lang = bot.user_data['language']

    # Validate input
    if not user_message.strip():
        if response_gen:
            clarification_msg = response_gen.generate_clarification_message(detected_lang)
        else:
            clarification_msg = "Could you please provide more details about your symptoms?"
        bot.reply_to(message, clarification_msg)
        return

    try:
        # Use translated symptoms for ML prediction
        predictions = predict_disease(translated_symptoms)

        if not predictions:
            if response_gen:
                clarification_msg = response_gen.generate_clarification_message(detected_lang)
            else:
                clarification_msg = "Could you please provide more details about your symptoms?"
            bot.reply_to(message, clarification_msg)
            return

        # Generate response in the detected language
        if response_gen:
            response_text = response_gen.generate_response(predictions, detected_lang)
        else:
            # Fallback response if generator not available
            response_text = _generate_fallback_response(predictions)

        bot.reply_to(message, response_text)

    except Exception as e:
        error_response = f"Sorry, there was an error processing your request. Please try again."
        bot.reply_to(message, error_response)


# Initialize user data storage
bot.user_data = {}

if __name__ == "__main__":
    print("🤖 Health ChatBot starting...")
    print(f"Multilingual Generator: {'✅ Connected' if response_gen else '❌ Not Available (using fallback)'}")
    print("Bot is running... Press Ctrl+C to stop")
    bot.polling()
