import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# Step 1: Load the JSON file containing the HTML content
with open('structured-knowledge-base.json', 'r') as f:
    data = json.load(f)

# Step 2: Parse the HTML content
html_content = data['html']
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Extract relevant data
extracted_data = []
for span in soup.find_all('span'):
    text_content = span.get_text().strip()
    if text_content:
        extracted_data.append({'type': 'span', 'content': text_content})

for p in soup.find_all('p'):
    text_content = p.get_text().strip()
    if text_content:
        extracted_data.append({'type': 'paragraph', 'content': text_content})

# Step 4: Convert to structured JSON
structured_data = {
    "data": extracted_data
}

# Save the structured data for future use (optional)
with open('structured_knowledge_base.json', 'w') as f:
    json.dump(structured_data, f, indent=2)

# Step 5: Use the structured JSON in your chatbot
def search_knowledge_base(query, knowledge_base):
    results = []
    query = query.lower()
    for item in knowledge_base['data']:
        if query in item['content'].lower():
            results.append(item['content'])
    return results

@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    user_input = request.json.get('query')
    user_name = request.json.get('name', 'User')
    results = search_knowledge_base(user_input, structured_data)

    if results:
        response = f"{user_name}, here's what I found: {results[0]}"
    else:
        response = f"Sorry, {user_name}, I couldn't find any information on that topic."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
