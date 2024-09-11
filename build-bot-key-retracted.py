import json
from sentence_transformers import SentenceTransformer, util
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Load the Sentence-BERT model for retrieval
retrieval_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load and process the knowledge base
with open('extracted_content.txt', 'r') as f:
    knowledge_base = f.read().splitlines()

# Precompute the embeddings for the knowledge base content
knowledge_base_embeddings = retrieval_model.encode(knowledge_base, convert_to_tensor=True)

# Set your OpenAI API key
openai.api_key = 'xxxxx'

def retrieve_relevant_content(query, knowledge_base, knowledge_base_embeddings, top_k=5):
    # Convert the query to an embedding
    query_embedding = retrieval_model.encode(query, convert_to_tensor=True)

    # Compute the cosine similarity between the query and the knowledge base
    similarities = util.pytorch_cos_sim(query_embedding, knowledge_base_embeddings)

    # Find the top_k best matches
    top_k_indices = similarities.topk(k=top_k).indices[0].tolist()

    # Retrieve the top_k matching sentences
    retrieved_content = [knowledge_base[i] for i in top_k_indices]

    return retrieved_content

def generate_response(retrieved_content, query):
    # Combine the retrieved content into a single context
    context = "\n".join(retrieved_content)

    # Prepare the prompt for GPT-4
    prompt = f"{query}\n\nBased on this information from the knowledge base:\n{context}\n\nPlease answer the question considering both the provided information and any additional relevant knowledge you have. First check the information that was given and if it gives a satisfactory answer then return it. Else combine whatever could be gotten from the info, and any additional relevant knowledge you have. Make sure that the answer is better than the one given by default without the knowledge base."

    # Call the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    user_input = request.json.get('query')
    user_name = request.json.get('name', 'User')

    # Step 1: Retrieve relevant content from the knowledge base
    retrieved_content = retrieve_relevant_content(user_input, knowledge_base, knowledge_base_embeddings)

    # Step 2: Generate a response using the retrieved content and GPT-4's broader knowledge
    response_text = generate_response(retrieved_content, user_input)

    # Return the generated response
    return jsonify({'response': f"{user_name}, here's what I found: {response_text}"})

if __name__ == '__main__':
    app.run(debug=True)
