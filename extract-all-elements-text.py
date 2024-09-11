import json
from bs4 import BeautifulSoup

# Step 1: Load the JSON file containing the HTML content
with open('knowledge-base.json', 'r') as f:
    data = json.load(f)

# Step 2: Initialize an empty string for HTML content
html_content = ""

# Step 3: Check if the data is a list or dictionary and extract HTML
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str) and "<" in value:  # Check if it contains HTML tags
                    html_content += value  # Combine HTML contents if needed
elif isinstance(data, dict):
    for key, value in data.items():
        if isinstance(value, str) and "<" in value:  # Check if it contains HTML tags
            html_content += value

# Step 4: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 5: Extract relevant data from the HTML
extracted_data = []

# Function to extract text from an element type
def extract_text_from_element(element_name):
    for element in soup.find_all(element_name):
        text_content = element.get_text().strip()
        if text_content:
            extracted_data.append({'type': element_name, 'content': text_content})

# List of relevant HTML elements that can contain text
elements_to_extract = [
    'span', 'a', 'b', 'strong', 'i', 'em', 'u', 'small', 'abbr', 'cite', 'code', 'kbd', 'var', 's', 'mark', 'q',
    'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'li', 'dt', 'dd', 'figcaption', 'textarea',
    'label', 'title', 'caption', 'option', 'summary', 'button'
]

# Extract text from each relevant HTML element
for element in elements_to_extract:
    extract_text_from_element(element)

# Step 6: Convert to structured JSON
structured_data = {
    "data": extracted_data
}

# Step 7: Save the structured data to a JSON file
output_file = 'structured-text-data.json'
with open(output_file, 'w') as f:
    json.dump(structured_data, f, indent=2)

print(f"Structured data has been saved to {output_file}")
