import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Step 1: Load the content from the text file
with open('extracted_content.txt', 'r') as f:
    extracted_content = f.readlines()

# Step 2: Clean and preprocess the content
def preprocess_content(lines):
    processed_lines = []
    seen = set()  # To remove duplicates
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            processed_lines.append(line)
            seen.add(line)
    return processed_lines

processed_content = preprocess_content(extracted_content)

# Debugging: Print out some lines from the processed content
print("Processed Content:")
for i, line in enumerate(processed_content[:10]):  # Print the first 10 lines
    print(f"{i+1}: {line}")

# Step 3: Search Functionality
def search_knowledge_base(query, knowledge_base):
    results = []
    query_words = query.lower().split()
    print(f"Query: {query}")  # Debugging: Print the query
    for line in knowledge_base:
        line_lower = line.lower()
        print(f"Checking line: {line}")  # Debugging: Print each line being checked
        if all(word in line_lower for word in query_words):
            print(f"Match found: {line}")  # Debugging: Print matched line
            results.append(line)
    return results

@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    user_input = request.json.get('query')
    user_name = request.json.get('name', 'User')
    results = search_knowledge_base(user_input, processed_content)

    if results:
        response = f"{user_name}, here's what I found: {results[0]}"
    else:
        response = f"Sorry, {user_name}, I couldn't find any information on that topic."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
