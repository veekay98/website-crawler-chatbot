from deep_translator import GoogleTranslator

def translate_file_to_spanish(input_file_path, output_file_path):
    # Initialize the translator
    translator = GoogleTranslator(source='en', target='es')

    # Read the English text from the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        english_text = file.read()

    # Translate the text to Spanish
    spanish_text = translator.translate(english_text)

    # Write the translated text to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(spanish_text)

    print(f"Translation complete! The translated text has been saved to {output_file_path}")

# Example usage
input_file = 'extracted_content.txt'
output_file = 'extracted_content_spanish.txt'
translate_file_to_spanish(input_file, output_file)
