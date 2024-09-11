import json
from sentence_transformers import SentenceTransformer, util
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Load the Sentence-BERT model for retrieval
retrieval_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load and process the knowledge base
with open('spanish_content.txt', 'r') as f:
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

    # Prepare the prompt for GPT-4 in Spanish
    prompt = f"{query}\n\nBasado en esta información de la base de conocimientos:\n{context}\n\nPor favor, responde la pregunta considerando tanto la información proporcionada como cualquier conocimiento adicional relevante que tengas. Primero, verifica la información dada y, si es satisfactorio, devuélvela. Si no, combina lo que se obtuvo de la información y cualquier conocimiento adicional relevante que tengas. Responde a la pregunta en español."

    # Call the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente muy informado."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

@app.route('/')
def index():
    return render_template('index-spanish.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    user_input = request.json.get('query')
    user_name = request.json.get('name', 'Usuario')

    # Step 1: Retrieve relevant content from the knowledge base
    retrieved_content = retrieve_relevant_content(user_input, knowledge_base, knowledge_base_embeddings)

    # Step 2: Generate a response using the retrieved content and GPT-4's broader knowledge
    response_text = generate_response(retrieved_content, user_input)

    # Return the generated response
    return jsonify({'response': f"{user_name}, esto es lo que encontré: {response_text}"})

if __name__ == '__main__':
    app.run(debug=True)
