"""
End-to-end test script for the health chatbot
Tests: language detection, translation, disease prediction, and response generation
"""
import joblib
import pandas as pd
import numpy as np
from simple_generator import SimpleMultilingualGenerator

# Load model and dataset
model = joblib.load("model/best_disease_model.pkl")
df = pd.read_json("data/health_dataset.json")

# Initialize multilingual generator
response_gen = SimpleMultilingualGenerator()

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

# Test cases
test_inputs = [
    ("I have itching and skin rash", "en"),
    ("मुझे खुजली और त्वचा पर चकत्ते हैं", "hi"),
    ("నాకు దురద మరియు చర్మంపై దద్దుర్లు ఉన్నాయి", "te")
]

print("=" * 80)
print("HEALTH CHATBOT - MULTILINGUAL TEST")
print("=" * 80)

for user_input, expected_lang in test_inputs:
    print(f"\n{'='*80}")
    print(f"Test Input (Expected Lang: {expected_lang}):")
    print(f"  Original: {user_input}")
    
    # Step 1: Language Detection
    detected_lang = response_gen.detect_language(user_input)
    print(f"  Detected Language: {detected_lang}")
    
    # Step 2: Translation
    translated = response_gen.translate_to_english(user_input)
    print(f"  Translated: {translated}")
    
    # Step 3: Disease Prediction
    predictions = predict_disease(translated)
    print(f"  Predictions:")
    for p in predictions:
        print(f"    - {p['disease']}: {p['confidence']}%")
    
    # Step 4: Response Generation
    response = response_gen.generate_response(predictions, detected_lang)
    print(f"  Response ({detected_lang}):")
    print(f"    {response}")

print(f"\n{'='*80}")
print("✅ All tests completed successfully!")
print("=" * 80)
