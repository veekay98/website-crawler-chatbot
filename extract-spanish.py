from langdetect import detect

def extract_spanish_content(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    spanish_lines = []

    for line in lines:
        try:
            # Detect the language of the line
            if detect(line.strip()) == 'es':  # 'es' is the language code for Spanish
                spanish_lines.append(line)
        except:
            # If detection fails, skip that line
            continue

    # Write the Spanish content to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(spanish_lines)

    print(f"Extraction complete! The Spanish content has been saved to {output_file_path}")

# Example usage
input_file = 'extracted_content.txt'
output_file = 'spanish_content.txt'
extract_spanish_content(input_file, output_file)
