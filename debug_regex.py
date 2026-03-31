from simple_generator import SimpleMultilingualGenerator
import re

gen = SimpleMultilingualGenerator()

# Test Hindi translation
hindi_text = "मुझे खुजली और त्वचा पर चकत्ते हैं"
print(f"Hindi input: {hindi_text}")

# Debug the translation logic
detected_lang = gen.detect_language(hindi_text)
print(f"Detected language: {detected_lang}")

# Create translation entries
translation_entries = []
for symptom, translations_dict in gen.SYMPTOM_TRANSLATIONS.items():
    if detected_lang in translations_dict:
        translated_phrase = translations_dict[detected_lang]
        word_count = len(translated_phrase.split())
        translation_entries.append((translated_phrase, symptom, word_count))
        print(f"  Found: '{translated_phrase}' -> '{symptom}' (words: {word_count})")

# Test each pattern
translation_entries.sort(key=lambda x: x[2], reverse=True)
result = hindi_text
for translated_phrase, english_word, _ in translation_entries:
    pattern = r'\b' + re.escape(translated_phrase) + r'\b'
    print(f"\nTesting pattern for '{translated_phrase}':")
    print(f"  Pattern: {pattern}")
    matches = re.findall(pattern, result, flags=re.IGNORECASE)
    print(f"  Matches: {matches}")
    result = re.sub(pattern, english_word, result, flags=re.IGNORECASE)
    print(f"  Result so far: {result}")

print(f"\nFinal translation: {result}")
