import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

app = Flask(__name__)

DB_DIR = "vector_db"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "krishisaarthi_chunks"
GROQ_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

embed_model = None
collection = None
groq_client = None


def initialize():
    global embed_model, collection, groq_client
    print("Loading embedding model...")
    embed_model = SentenceTransformer(MODEL_NAME)
    print("Loading ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    print("Connecting to Groq...")
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    print("KrishiSaarthi is ready!")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("message", "").strip()

        if not query:
            return jsonify({"error": "Empty message"}), 400

        query_embedding = embed_model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        retrieved_chunks = results["documents"][0]
        sources = results["metadatas"][0]

        context_text = "\n".join(
            [f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(retrieved_chunks)]
        )

        prompt = f"""You are KrishiSaarthi, an agriculture scheme assistant for Indian farmers.

Answer the farmer's question using ONLY the context below.
If the answer is not in the context, say: "I could not find this information in the available government documents."

Context:
{context_text}

Farmer Question: {query}

Give a comprehensive answer in simple English. Use bullet points and clear numbered steps where appropriate."""

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are KrishiSaarthi, a helpful and knowledgeable agriculture policy assistant for Indian farmers. Help farmers understand government schemes, subsidies, eligibility, and how to apply for benefits."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content
        source_files = list(set([
            s.get("source_file", "Unknown")
             .replace(".txt", "")
             .replace("_", " ")
             .replace("-", " ")
             .title()
            for s in sources
        ]))

        return jsonify({"answer": answer, "sources": source_files})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    initialize()
    app.run(debug=False, port=5000, host="0.0.0.0")
