import os
import re
import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

DB_DIR = "vector_db"
COLLECTION_NAME = "krishisaarthi_chunks"

OUTPUT_DIR = "knowledge_base/schemes"
RAW_DIR = "knowledge_base/raw_llm_outputs"

MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"

TOP_K = 18
RETRIES = 2


def safe_filename(name: str) -> str:
    name = name.lower().strip()
    name = name.replace(".txt", "")
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def extract_json_from_text(text: str):
    text = text.strip()

    # remove markdown fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```", "", text).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        return None

    json_str = text[start:end+1].strip()

    # fix trailing commas
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    try:
        return json.loads(json_str)
    except:
        return None


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(RAW_DIR).mkdir(parents=True, exist_ok=True)

    print("🔹 Loading embedding model...")
    embed_model = SentenceTransformer(MODEL_NAME)

    print("🔹 Loading ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    print("🔹 Connecting Groq...")
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Get unique TXT sources from vector DB
    all_data = collection.get(include=["metadatas"])
    metas = all_data["metadatas"]

    sources = sorted(list(set(m.get("source_file", "unknown") for m in metas)))

    print(f"\n✅ Found {len(sources)} documents in vector DB.\n")

    for source_file in sources:
        if source_file == "unknown":
            continue

        json_name = safe_filename(source_file) + ".json"
        output_path = os.path.join(OUTPUT_DIR, json_name)

        # Skip if already done
        if os.path.exists(output_path):
            print(f"⏩ Skipped (already extracted): {source_file}")
            continue

        print("\n==============================")
        print(f"📌 Document: {source_file}")

        # Query embedding (simple)
        query_embedding = embed_model.encode(source_file).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K,
            include=["documents", "metadatas"]
        )

        docs = results["documents"][0]
        metadatas = results["metadatas"][0]

        # Keep only chunks from same source_file
        filtered_docs = []
        for d, m in zip(docs, metadatas):
            if m.get("source_file") == source_file:
                filtered_docs.append(d)

        context = "\n\n".join(filtered_docs)

        prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

You are extracting structured scheme information from an official agriculture PDF.

Source file: {source_file}

Context:
{context}

JSON format:
{{
  "document_title": "",
  "scheme_or_topic": "",
  "objective": "",
  "benefits": [],
  "eligibility": [],
  "documents_required": [],
  "how_to_apply": [],
  "official_links": [],
  "helpline": [],
  "important_dates_or_frequency": "",
  "notes": "",
  "source_file": "{source_file}"
}}

Rules:
- Use ONLY given context.
- If unknown keep "" or [].
"""

        success = False
        last_raw = ""

        for attempt in range(RETRIES + 1):
            resp = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            raw = resp.choices[0].message.content
            last_raw = raw

            parsed = extract_json_from_text(raw)

            if parsed:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)

                print(f"✅ Saved JSON: {output_path}")
                success = True
                
                break
            else:
                print(f"⚠️ JSON parsing failed attempt {attempt+1}/{RETRIES+1}... retrying")

        if not success:
            raw_path = os.path.join(RAW_DIR, safe_filename(source_file) + "_raw.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(last_raw)

            print(f"❌ Failed. Saved raw output: {raw_path}")

    print("\n🎉 Phase 5B Done! 1 JSON created per PDF in knowledge_base/schemes/")


if __name__ == "__main__":
    main()
