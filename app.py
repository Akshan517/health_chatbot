from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from simple_generator import SimpleMultilingualGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load model and dataset
model = joblib.load("model/best_disease_model.pkl")
df = pd.read_json("data/health_dataset.json")

# Initialize multilingual response generator
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
try:
    response_gen = SimpleMultilingualGenerator()
    print("✅ Multilingual generator initialized")
except Exception as e:
    print(f"❌ Generator initialization failed: {e}")
    response_gen = None

@app.route("/predict", methods=["POST"])
def predict():
    """Predict disease and generate multilingual response"""
    data = request.json
    user_input = data.get("symptoms")
    user_language = data.get("language", "auto")  # Allow auto-detection

    if not user_input:
        return jsonify({"error": "No symptoms provided"}), 400

    try:
        # Handle translation if generator is available
        if response_gen and user_language == "auto":
            detected_lang = response_gen.detect_language(user_input)
            translated_symptoms = response_gen.translate_to_english(user_input)
            response_lang = detected_lang
        elif response_gen and user_language != "auto":
            translated_symptoms = response_gen.translate_to_english(user_input)  # For now, assume input is in specified language
            response_lang = user_language
        else:
            translated_symptoms = user_input
            response_lang = user_language if user_language != "auto" else "en"
        
        # Use translated symptoms for ML prediction
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

        # Generate natural response using multilingual generator
        if response_gen:
            response_text = response_gen.generate_response(results, response_lang)
        else:
            # Fallback response
            response_text = _generate_fallback_response(results)
        
        return jsonify({
            "predictions": results,
            "response": response_text,
            "language": response_lang,
            "translated_input": translated_symptoms if translated_symptoms != user_input else None
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


if __name__ == "__main__":
    app.run(debug=True)