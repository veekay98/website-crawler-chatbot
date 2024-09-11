import re

# File paths
input_file = 'kb.txt'  # Path to the input RTF file
output_file = 'extracted_content.txt'  # Path to the output text file

# Read the RTF file
with open(input_file, 'r') as file:
    txt_data = file.read()

# Regular expression to find all "content" values
pattern = r'"content":\s*"([^"]+)"'
matches = re.findall(pattern, txt_data)

# Remove duplicates by converting the list to a set, then back to a list
unique_matches = list(set(matches))

# Sort the unique matches to maintain some order (optional)
unique_matches.sort()

# Write the extracted content to a new text file, each on a new line
with open(output_file, 'w') as file:
    for match in unique_matches:
        file.write(match + '\n')

print(f"Extracted and deduplicated content has been saved to {output_file}")
