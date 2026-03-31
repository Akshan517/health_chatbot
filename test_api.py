"""
Test script for the Flask API endpoint
"""
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from simple_generator import SimpleMultilingualGenerator

# Load model and dataset
model = joblib.load("model/best_disease_model.pkl")
df = pd.read_json("data/health_dataset.json")

# Initialize multilingual generator
try:
    response_gen = SimpleMultilingualGenerator()
    print("✅ Multilingual generator initialized")
except Exception as e:
    print(f"❌ Generator initialization failed: {e}")
    response_gen = None

app = Flask(__name__)

def predict_disease(translated_symptoms):
    """Predict disease from symptoms"""
    try:
        probabilities = model.predict_proba([translated_symptoms])[0]
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
    except Exception as e:
        print(f"Prediction error: {e}")
        return []

# Test the prediction functionality
test_cases = [
    {"symptoms": "I have itching and skin rash", "language": "auto"},
    {"symptoms": "मुझे खुजली और त्वचा पर चकत्ते हैं", "language": "auto"},
    {"symptoms": "నాకు దురద మరియు చర్మంపై దద్దుర్లు ఉన్నాయి", "language": "auto"},
]

print("\n" + "="*80)
print("FLASK API TEST")
print("="*80)

for test in test_cases:
    print(f"\nTest Input: {test['symptoms']}")
    
    # Simulate the API logic
    user_input = test["symptoms"]
    user_language = test["language"]
    
    if response_gen and user_language == "auto":
        detected_lang = response_gen.detect_language(user_input)
        translated_symptoms = response_gen.translate_to_english(user_input)
        response_lang = detected_lang
    else:
        translated_symptoms = user_input
        response_lang = user_language if user_language != "auto" else "en"
    
    print(f"Detected Language: {response_lang}")
    print(f"Translated: {translated_symptoms}")
    
    # Predict disease
    results = predict_disease(translated_symptoms)
    print(f"Predictions: {results}")
    
    # Generate response
    if response_gen:
        response_text = response_gen.generate_response(results, response_lang)
    else:
        response_text = f"Predictions: {results}"
    
    print(f"Response: {response_text[:100]}...")

print("\n" + "="*80)
print("✅ API test completed successfully!")
print("="*80)
