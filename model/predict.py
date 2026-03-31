import joblib
import pandas as pd
import numpy as np

# Load trained model and vectorizer
model = joblib.load("disease_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load dataset to fetch precautions
df = pd.read_json("../data/health_dataset.json")
df.columns = df.columns.str.strip()

def predict_disease(user_input):
    # Transform input text
    input_vector = vectorizer.transform([user_input])

    # Get probabilities
    probabilities = model.predict_proba(input_vector)[0]
    classes = model.classes_

    # Get top 2 predictions
    top_indices = np.argsort(probabilities)[-2:][::-1]

    results = []

    for index in top_indices:
        disease = classes[index]
        confidence = round(probabilities[index] * 100, 2)

        # Fetch precautions
        precautions = df[df["disease"] == disease]["precautions"].iloc[0]

        results.append({
            "disease": disease,
            "confidence": confidence,
            "precautions": precautions
        })

    return results


if __name__ == "__main__":
    user_input = input("Enter symptoms: ")

    predictions = predict_disease(user_input)

    print("\nPrediction Results:\n")

    for p in predictions:
        print(f"Disease: {p['disease']}")
        print(f"Confidence: {p['confidence']}%")
        print(f"Precautions: {p['precautions']}")
        print("-" * 50)
