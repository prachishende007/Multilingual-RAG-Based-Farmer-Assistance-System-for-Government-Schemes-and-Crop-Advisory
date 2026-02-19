import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

DB_DIR = "vector_db"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "krishisaarthi_chunks"

# Groq model
GROQ_MODEL = "llama-3.1-8b-instant"
# You can also use: "llama3-70b-8192" (better but heavier)

def main():
    print("🔹 Loading embedding model...")
    embed_model = SentenceTransformer(MODEL_NAME)

    print("🔹 Loading ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    print("🔹 Connecting Groq...")
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    print("\n RAG Chatbot Ready (Groq)! Type exit to stop.\n")

    while True:
        query = input("👨‍🌾 Farmer Question: ")
        if query.lower() == "exit":
            break

        # Step 1: Retrieve chunks
        query_embedding = embed_model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        retrieved_chunks = results["documents"][0]
        sources = results["metadatas"][0]

        context_text = ""
        for i, chunk in enumerate(retrieved_chunks):
            context_text += f"\n[Chunk {i+1}] {chunk}\n"

        # Step 2: Ask Groq LLM with context
        prompt = f"""
You are an agriculture scheme assistant for Indian farmers.

Answer the farmer's question using ONLY the context below.
If the answer is not in the context, say:
"I could not find this information in the available government documents."

Context:
{context_text}

Farmer Question:
{query}

Give answer in simple English, clear bullet points, and short steps.
"""

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful agriculture policy assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        print("\n🤖 Answer:\n")
        print(answer)

        print("\n📌 Sources used:")
        for s in sources:
            print("-", s.get("source_file"))

        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
