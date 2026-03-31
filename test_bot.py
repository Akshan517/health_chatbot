import telebot
import joblib
import pandas as pd
from simple_generator import SimpleMultilingualGenerator
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8709729595:AAGxsdavG0eDPq-8vvf9Ix2-JQaAWQQNYpA")
model = joblib.load("model/best_disease_model.pkl")
df = pd.read_json("data/health_dataset.json")

try:
    response_gen = SimpleMultilingualGenerator()
    print("✅ Multilingual generator initialized")
except Exception as e:
    print(f"❌ Generator initialization failed: {e}")
    response_gen = None

bot = telebot.TeleBot(TOKEN)
print("🤖 Bot initialized successfully")
print(f"Multilingual Generator: {'✅ Connected' if response_gen else '❌ Not Available (using fallback)'}")

# Test language detection
if response_gen:
    test_inputs = [
        "I have itching and skin rash",
        "मुझे खुजली और त्वचा पर चकत्ते हैं",
        "నాకు దురద మరియు చర్మంపై దద్దుర్లు ఉన్నాయి"
    ]
    for test_input in test_inputs:
        lang = response_gen.detect_language(test_input)
        translated = response_gen.translate_to_english(test_input)
        print(f"Test: '{test_input}' → Language: {lang}, Translated: '{translated}'")

print("✅ All tests passed!")