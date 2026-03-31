# Health ChatBot - Gemini Pro Integration & Multilingual Setup Guide

## 🚀 Overview

Your Health ChatBot has been enhanced with:
- **Gemini Pro API** for natural, context-aware text generation
- **Multilingual Support** - Automatic language detection and response generation in 15+ languages
- **Conversational Responses** - No more repetitive template-based replies

## 📋 Prerequisites

- Python 3.8+
- Gemini Pro API key (free)
- Telegram Bot Token

## 🔑 Step 1: Get Gemini Pro API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the API key
4. Keep it safe (never commit to git!)

## 🤖 Step 2: Setup Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Follow the prompts to create a new bot
3. Copy the bot token
4. Keep it safe

## 📝 Step 3: Configure Environment Variables

### Option A: Using .env file (Recommended)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_pro_api_key_here
   ```

### Option B: Set Environment Variables Directly

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
$env:TELEGRAM_BOT_TOKEN = "your_token_here"
```

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
set TELEGRAM_BOT_TOKEN=your_token_here
```

## 📦 Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Step 5: Run the Chatbot

### For Telegram Bot:
```bash
python bot.py
```

Expected output:
```
🤖 Health ChatBot starting...
Gemini Pro: ✅ Connected
```

### For Flask API:
```bash
python app.py
```

Then test with:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "fever and cough", "language": "en"}'
```

## 🌐 Supported Languages

The chatbot automatically detects and responds in these languages:

| Code | Language |
|------|----------|
| en | English |
| hi | Hindi |
| es | Spanish |
| fr | French |
| de | German |
| pt | Portuguese |
| it | Italian |
| ja | Japanese |
| zh-cn | Chinese (Simplified) |
| zh-tw | Chinese (Traditional) |
| ru | Russian |
| ar | Arabic |
| ta | Tamil |
| te | Telugu |
| ur | Urdu |

## 💬 How It Works

### Language Detection & Response Generation

1. **User sends message** → Chatbot detects language automatically
2. **Disease prediction** → ML model predicts disease and confidence
3. **Gemini Pro generation** → Creates natural, multilingual response with:
   - Conversational tone
   - Practical advice
   - Medical disclaimer
   - Empathetic language

### Example Interactions

**Input (English):** "I have fever and cough"
**Response:** 
```
Based on your symptoms, you may have common cold or influenza. 
The analysis shows a 78% confidence level. Here's what I recommend...
[Natural, conversational continuation with precautions]
```

**Input (Hindi):** "मुझे बुखार और खांसी है"
**Response:** 
```
आपके लक्षणों के आधार पर, आपको सर्दी या फ्लू हो सकता है...
[Natural Hindi response with advice]
```

## 🛠️ API Endpoints

### Flask API

**POST /predict**

Request:
```json
{
    "symptoms": "fever, cough, headache",
    "language": "en"
}
```

Response:
```json
{
    "predictions": [
        {
            "disease": "Common Cold",
            "confidence": 85.5,
            "precautions": "Get rest, drink fluids..."
        }
    ],
    "response": "[Natural language response from Gemini Pro]",
    "language": "en"
}
```

## 🔧 Troubleshooting

### Gemini Pro Connection Issues

**Problem:** "Warning: Could not initialize Gemini Pro"

**Solutions:**
1. Check API key in .env file
2. Ensure internet connection is active
3. Verify API key is valid at https://makersuite.google.com/app/apikey
4. Check rate limits haven't been exceeded

### Language Detection Not Working

**Problem:** Response not in expected language

**Solutions:**
1. Ensure input contains clear language indicators
2. Use language parameter explicitly in API
3. Check langdetect library is installed: `pip install langdetect --upgrade`

### Incorrect Disease Predictions for Non-English Languages

**Problem:** Hindi/Telugu inputs giving wrong predictions (like Asthma instead of Psoriasis)

**Solutions:**
✅ **FIXED:** The bot now automatically translates all inputs to English before ML processing
- English: "I have itching and skin rash" → Psoriasis ✅
- Hindi: "मुझे खुजली और त्वचा पर चकत्ते हैं" → Translated to English → Psoriasis ✅
- Telugu: "నాకు దురద మరియు చర్మంపై దద్దుర్లు ఉన్నాయి" → Translated to English → Psoriasis ✅

**How it works:**
1. Detect language of user input
2. Translate symptoms to English for ML model
3. Get accurate disease prediction
4. Generate response in original language using Gemini Pro

### Bot Not Responding

**Problem:** Bot doesn't reply to messages

**Solutions:**
1. Verify Telegram token is correct
2. Check bot is running (no errors in terminal)
3. Ensure bot is added to chat properly
4. Check internet connection

## 📊 File Structure

```
health-chatBot/
├── app.py                    # Flask API
├── bot.py                    # Telegram Bot
├── gemini_generator.py       # Gemini Pro integration (NEW)
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── TELEGRAM_BOT_SETUP.md     # Telegram setup guide
├── data/
│   └── health_dataset.json
└── model/
    ├── predict.py
    ├── train_model.py
    └── best_disease_model.pkl
```

## 🎯 Features

✅ **Natural Language Generation** - Gemini Pro creates unique responses every time
✅ **Multilingual Support** - Auto-detects language and responds accordingly
✅ **Context-Aware** - Considers confidence levels in tone
✅ **Empathetic** - Conversational, not robotic
✅ **Fallback Support** - Works even if Gemini Pro temporarily unavailable
✅ **Easy Configuration** - Simple .env setup

## ⚠️ Important Notes

1. **API Rate Limits**: Gemini Pro has free tier limits. Monitor usage.
2. **Medical Disclaimer**: Always remind users to consult healthcare professionals
3. **Privacy**: Do not log user health information
4. **Cost**: Gemini Pro is free but may have usage limits

## 📞 Support

- Gemini Pro Docs: https://ai.google.dev/
- Telegram Bot Docs: https://python-telegram-bot.readthedocs.io/
- langdetect: https://github.com/Mimino666/langdetect

## 🎓 Next Steps

1. Test with different languages
2. Monitor Gemini Pro usage
3. Add user feedback mechanism
4. Implement response caching for common queries
5. Add conversation history for context

---

**Happy Coding! 🚀**
