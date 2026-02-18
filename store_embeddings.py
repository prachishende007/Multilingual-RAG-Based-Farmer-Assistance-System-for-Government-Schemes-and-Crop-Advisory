import os
import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_DIR = "chunks"
DB_DIR = "vector_db"

MODEL_NAME = "all-MiniLM-L6-v2"

def main():
    Path(DB_DIR).mkdir(exist_ok=True)

    print("🔹 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("🔹 Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)

    collection = client.get_or_create_collection(name="krishisaarthi_chunks")

    chunk_files = [f for f in os.listdir(CHUNKS_DIR) if f.endswith("_chunks.json")]

    if not chunk_files:
        print("❌ No chunk JSON files found in chunks/")
        return

    print(f"✅ Found {len(chunk_files)} chunk files.\n")

    added_count = 0
    skipped_count = 0

    for file in chunk_files:
        file_path = os.path.join(CHUNKS_DIR, file)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        source_file = data.get("source_file", file)

        for chunk in data["chunks"]:
            chunk_id = chunk["chunk_id"]
            chunk_text = chunk["text"]

            # ✅ Check if already exists
            existing = collection.get(ids=[chunk_id])

            if existing and len(existing["ids"]) > 0:
                skipped_count += 1
                continue

            embedding = model.encode(chunk_text).tolist()

            collection.add(
                ids=[chunk_id],
                documents=[chunk_text],
                embeddings=[embedding],
                metadatas=[{"source_file": source_file}]
            )

            added_count += 1

        print(f"✅ Done: {source_file}")

    print("\n Phase 5 Done!")
    print(f" Newly added chunks: {added_count}")
    print(f" Skipped (already stored): {skipped_count}")
    print("📂 Vector DB saved inside vector_db/")

if __name__ == "__main__":
    main()
