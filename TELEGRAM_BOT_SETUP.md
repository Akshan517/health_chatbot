# Telegram Health ChatBot Setup Guide

## ✅ Bot is Ready!

Your health chatbot is now configured to work on Telegram. Here's what's included:

### 📋 Features
- **Disease Prediction**: Users send symptoms, bot predicts diseases
- **Confidence Scores**: Shows prediction confidence percentage
- **Precautions**: Provides medical precautions for predicted diseases
- **Accuracy**: 88.88% using Random Forest classifier
- **Dataset**: 405 health records with 60+ diseases

### 🚀 How to Run

1. **Activate Virtual Environment**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Start the Bot**
   ```bash
   python bot.py
   ```

3. **Test on Telegram**
   - Search for `@aksha_health_bot` or use this link: [t.me/aksha_health_bot](https://t.me/aksha_health_bot)
   - Type `/start` to begin
   - Send symptoms like: `fever, cough, fatigue`
   - Bot will respond with predictions

### 📤 Example Usage

**User Input:**
```
fever, cough, headache
```

**Bot Response:**
```
🩺 Prediction Results:

🦠 Disease: Common Cold
📊 Confidence: 98.5%
💊 Precautions: ['drink warm fluids', 'rest', 'steam inhalation', 'consult doctor']

🦠 Disease: Viral Fever
📊 Confidence: 1.5%
💊 Precautions: ['rest', 'fluids', 'medication', 'consult doctor']
```

### 📁 Files Structure
```
health-chatBot/
├── bot.py                    # Telegram bot main script
├── app.py                    # Flask API (optional)
├── model/
│   ├── train_model.py       # Training script
│   └── best_disease_model.pkl  # Trained model (88.88% accuracy)
├── data/
│   └── health_dataset.json  # 405 disease records
└── requirements.txt         # Dependencies
```

### 🔧 Dependencies Installed
- `python-telegram-bot`: Telegram bot library
- `scikit-learn`: ML models
- `pandas`: Data processing
- `joblib`: Model serialization
- `flask`: API framework (optional)

### ⚙️ Bot Configuration
- **Token**: Already configured
- **Model**: Random Forest (3 models trained: Logistic Regression, Naive Bayes, Random Forest)
- **TF-IDF**: Bigram vectorization for better pattern recognition
- **Data Augmentation**: Dataset doubled during training

### 📊 Model Details
- **Best Model**: Random Forest with 200 estimators
- **Accuracy**: 88.88%
- **Test Set**: 162 samples
- **Features**: TF-IDF with bigrams (1-2 word combinations)
- **Classes**: 60+ diseases supported

### 🛑 To Stop the Bot
Press `Ctrl + C` in the terminal

### 📝 Notes
- Bot is publicly available on Telegram
- Ensure your internet connection is active
- Keep the terminal running for the bot to stay active
- Model loads automatically on startup

### 🎯 Next Steps
1. Test with Telegram: `t.me/aksha_health_bot`
2. Try various symptoms combinations
3. For Flask API, run: `python app.py` (separate from bot)

---
**Status**: ✅ Ready to Deploy
**Last Updated**: March 18, 2026
