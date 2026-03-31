import pandas as pd
import joblib
import os
import random

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

# ----------------------------
# Load Dataset
# ----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "../data/health_dataset.json")

df = pd.read_json(dataset_path)
df.columns = df.columns.str.strip()

# Remove missing
df = df.dropna()

# ----------------------------
# Convert Symptoms (list → string)
# ----------------------------
df["Symptoms"] = df["Symptoms"].apply(lambda x: " ".join(x))

# ----------------------------
# 🔥 DATA AUGMENTATION (KEY FIX)
# ----------------------------
def augment(symptoms):
    words = symptoms.split()
    random.shuffle(words)

    # remove 1 word randomly
    if len(words) > 3:
        words = words[:-1]

    return " ".join(words)

augmented_data = []

for _, row in df.iterrows():
    new_row = row.copy()
    new_row["Symptoms"] = augment(row["Symptoms"])
    augmented_data.append(new_row)

# Add augmented rows
df = pd.concat([df, pd.DataFrame(augmented_data)], ignore_index=True)

print("\nDataset after augmentation:", df.shape)

# ----------------------------
# Features & Labels
# ----------------------------
X = df["Symptoms"]
y = df["Disease"]

# ----------------------------
# Train/Test Split (STRATIFIED)
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------------
# Models (only using classifiers with predict_proba support)
# ----------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000),
    "Naive Bayes": MultinomialNB(),
    "Random Forest": RandomForestClassifier(n_estimators=200)
}

results = {}

# ----------------------------
# Training Loop
# ----------------------------
for name, model in models.items():

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("classifier", model)
    ])

    print("\n==============================")
    print("Training:", name)

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    results[name] = {
        "accuracy": acc,
        "model": pipeline
    }

    print("Accuracy:", acc)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

# ----------------------------
# Best Model
# ----------------------------
best_model_name = max(results, key=lambda x: results[x]["accuracy"])
best_model = results[best_model_name]["model"]

print("\n==============================")
print("Best Model:", best_model_name)
print("Best Accuracy:", results[best_model_name]["accuracy"])

# ----------------------------
# Save Model
# ----------------------------
model_path = os.path.join(script_dir, "best_disease_model.pkl")
joblib.dump(best_model, model_path)

print("\n[SUCCESS] Model saved successfully!")