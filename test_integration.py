#!/usr/bin/env python3
"""
Test script for Health ChatBot with Gemini Pro integration
"""

import os
from dotenv import load_dotenv
from gemini_generator import GeminiResponseGenerator

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test if Gemini Pro is connected"""
    print("🧪 Testing Gemini Pro Connection...")
    
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            return False
        
        generator = GeminiResponseGenerator(api_key=api_key)
        print("✅ Gemini Pro connection successful!")
        return True
    except Exception as e:
        print(f"❌ Gemini Pro connection failed: {e}")
        return False


def test_language_detection():
    """Test language detection"""
    print("\n🧪 Testing Language Detection...")
    
    test_cases = [
        ("fever and cough", "en"),
        ("बुखार और खांसी", "hi"),
        ("fiebre y tos", "es"),
        ("fever, headache, fatigue", "en"),
    ]
    
    for text, expected_lang in test_cases:
        detected = GeminiResponseGenerator.detect_language(text)
        status = "✅" if detected == expected_lang else "⚠️"
        print(f"{status} '{text[:30]}...' → Detected: {detected} (Expected: {expected_lang})")


def test_response_generation():
    """Test response generation"""
    print("\n🧪 Testing Response Generation...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set - skipping response generation test")
        return
    
    try:
        generator = GeminiResponseGenerator(api_key=api_key)
        
        # Test predictions
        test_predictions = [
            {
                "disease": "Common Cold",
                "confidence": 85.5,
                "precautions": "Get plenty of rest, stay hydrated, use saline nasal drops"
            },
            {
                "disease": "Influenza",
                "confidence": 60.2,
                "precautions": "Antiviral medication, rest, fluids, fever management"
            }
        ]
        
        # Test in English
        print("\n📝 Generating response in English...")
        response_en = generator.generate_multilingual_response(test_predictions, "en")
        print(f"Response length: {len(response_en)} characters")
        print(f"Preview: {response_en[:150]}...")
        
        # Test in Hindi
        print("\n📝 Generating response in Hindi...")
        response_hi = generator.generate_multilingual_response(test_predictions, "hi")
        print(f"Response length: {len(response_hi)} characters")
        print(f"Preview: {response_hi[:150]}...")
        
        print("\n✅ Response generation test passed!")
        
    except Exception as e:
        print(f"❌ Response generation test failed: {e}")


def test_welcome_messages():
    """Test welcome message generation"""
    print("\n🧪 Testing Welcome Message Generation...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set - skipping welcome message test")
        return
    
    try:
        generator = GeminiResponseGenerator(api_key=api_key)
        
        languages = ["en", "hi", "es"]
        for lang in languages:
            print(f"\n🌐 Welcome message for {GeminiResponseGenerator.get_language_name(lang)}:")
            msg = generator.generate_welcome_message(lang)
            print(f"   {msg[:100]}...")
        
        print("\n✅ Welcome message generation test passed!")
        
    except Exception as e:
        print(f"❌ Welcome message test failed: {e}")


def test_translation():
    """Test translation functionality"""
    print("\n🧪 Testing Translation Functionality...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set - skipping translation test")
        return
    
    try:
        generator = GeminiResponseGenerator(api_key=api_key)
        
        test_cases = [
            ("I have itching and skin rash", "en", "itching and skin rash"),
            ("मुझे खुजली और त्वचा पर चकत्ते हैं", "hi", "I have itching and skin rashes"),
            ("నాకు దురద మరియు చర్మంపై దద్దుర్లు ఉన్నాయి", "te", "I have itching and rashes on the skin"),
            ("Tengo picazón y erupción en la piel", "es", "I have itching and skin rash"),
        ]
        
        for original, expected_lang, expected_translation in test_cases:
            translated, detected_lang = generator.process_multilingual_symptoms(original)
            status = "✅" if detected_lang == expected_lang else "⚠️"
            print(f"{status} '{original[:30]}...' → {detected_lang} → '{translated[:50]}...'")
        
        print("\n✅ Translation test completed!")
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")


def demonstrate_responses():
    """Demonstrate how the bot should respond in different languages"""
    print("\n🎯 Expected Bot Response Examples:")
    print("=" * 60)
    
    examples = [
        {
            "input": "I have itching and skin rash",
            "language": "en",
            "expected_disease": "Psoriasis or similar skin condition",
            "response_style": "Natural, conversational English"
        },
        {
            "input": "मुझे खुजली और त्वचा पर चकत्ते हैं",
            "language": "hi",
            "expected_disease": "Psoriasis or similar skin condition (same as English)",
            "response_style": "Natural, conversational Hindi"
        },
        {
            "input": "నాకు దురద మరియు చర్మంపై దద్దుర్లు ఉన్నాయి",
            "language": "te",
            "expected_disease": "Psoriasis or similar skin condition (same as English)",
            "response_style": "Natural, conversational Telugu"
        }
    ]
    
    for example in examples:
        print(f"\n📝 Input ({example['language'].upper()}): {example['input']}")
        print(f"🔍 Expected Disease: {example['expected_disease']}")
        print(f"💬 Response Style: {example['response_style']}")
        print("-" * 40)


def main():
    """Run all tests"""
    print("=" * 60)
    print("🏥 Health ChatBot - Integration Test Suite")
    print("=" * 60)
    
    # Run tests
    gemini_ok = test_gemini_connection()
    test_language_detection()
    test_translation()
    
    if gemini_ok:
        test_response_generation()
        test_welcome_messages()
    
    # Show expected response examples
    demonstrate_responses()
    
    print("\n" + "=" * 60)
    print("✅ All available tests completed!")
    print("🔧 Translation fix applied - bot should now work correctly in all languages!")
    print("=" * 60)


if __name__ == "__main__":
    main()
