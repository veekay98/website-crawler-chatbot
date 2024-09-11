import json
from bs4 import BeautifulSoup

# Step 1: Load the JSON file containing the HTML content
with open('knowledge-base.json', 'r') as f:
    data = json.load(f)

# Step 2: Initialize an empty string for HTML content
html_content = ""

# Step 3: Check if the data is a list or dictionary and extract HTML
if isinstance(data, list):
    print("Data is a list.")
    for i, item in enumerate(data):
        if isinstance(item, dict) and 'html' in item:
            print(f"Extracting HTML from item {i}")
            html_content += item['html']  # Combine HTML contents if needed
        else:
            print(f"No 'html' key found in item {i} or item is not a dictionary.")
elif isinstance(data, dict):
    print("Data is a dictionary.")
    html_content = data.get('html', '')
    if not html_content:
        print("No 'html' key found in the dictionary.")

# Step 4: Print out the extracted HTML content for verification
if html_content:
    print("Extracted HTML content (first 500 chars):")
    print(html_content[:500])  # Print the first 500 characters for inspection
else:
    print("No HTML content found.")

# Step 5: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 6: Extract relevant data from the HTML
extracted_data = []
for span in soup.find_all('span'):
    text_content = span.get_text().strip()
    if text_content:
        print(f"Found span content: {text_content}")
        extracted_data.append({'type': 'span', 'content': text_content})
    else:
        print("Found empty span tag.")

for p in soup.find_all('p'):
    text_content = p.get_text().strip()
    if text_content:
        print(f"Found paragraph content: {text_content}")
        extracted_data.append({'type': 'paragraph', 'content': text_content})
    else:
        print("Found empty paragraph tag.")

# Step 7: Print the extracted data to ensure it's working
print("Extracted Data:")
print(extracted_data)

# Step 8: Convert to structured JSON
structured_data = {
    "data": extracted_data
}

# Step 9: Save the structured data to a JSON file
output_file = 'structured-knowledge-base.json'
with open(output_file, 'w') as f:
    json.dump(structured_data, f, indent=2)

print(f"Structured data has been saved to {output_file}")
