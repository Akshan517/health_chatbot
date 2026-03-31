from simple_generator import SimpleMultilingualGenerator

gen = SimpleMultilingualGenerator()

# Debug the translation mappings
print("SYMPTOM_TRANSLATIONS structure:")
for symptom, translations in gen.SYMPTOM_TRANSLATIONS.items():
    print(f"  {symptom}: {translations}")

print("\nTesting Hindi input:")
hindi_text = "मुझे खुजली और त्वचा पर चकत्ते हैं"
print(f"Input: {hindi_text}")
print(f"Detected lang: {gen.detect_language(hindi_text)}")
print(f"Words: {hindi_text.split()}")

# Create reverse map
reverse_map = {}
for symptom, translations_dict in gen.SYMPTOM_TRANSLATIONS.items():
    for lang, translated_word in translations_dict.items():
        if lang == 'hi':
            reverse_map[translated_word] = symptom
            for word in translated_word.split():
                reverse_map[word] = symptom

print(f"Reverse map for Hindi: {reverse_map}")
print(f"Translated: {gen.translate_to_english(hindi_text)}")
