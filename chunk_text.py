import os
import json
from pathlib import Path

INPUT_DIR = "clean_text"
OUTPUT_DIR = "chunks"

CHUNK_SIZE = 800
OVERLAP = 100


def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        new_start = end - overlap
        if new_start <= start:
            break
        start = new_start

    return chunks


def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    txt_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".txt")]

    if not txt_files:
        print("❌ No cleaned text files found in clean_text/")
        return

    print(f"✅ Found {len(txt_files)} cleaned files.\n")

    chunked_count = 0
    skipped_count = 0

    for file in txt_files:
        input_path = os.path.join(INPUT_DIR, file)
        output_path = os.path.join(OUTPUT_DIR, file.replace(".txt", "_chunks.json"))

        # ✅ Skip if already chunked
        if os.path.exists(output_path):
            print(f"⏩ Skipped (already chunked): {file}")
            skipped_count += 1
            continue

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)

        output_json = {
            "source_file": file,
            "chunk_size": CHUNK_SIZE,
            "overlap": OVERLAP,
            "total_chunks": len(chunks),
            "chunks": []
        }

        for i, chunk in enumerate(chunks):
            output_json["chunks"].append({
                "chunk_id": f"{file.replace('.txt','')}_chunk_{i+1}",
                "text": chunk
            })

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)

        print(f"✅ Chunked: {file} → {len(chunks)} chunks")
        chunked_count += 1

    print("\n Phase 4 Done!")
    print(f"Newly chunked files: {chunked_count}")
    print(f" Skipped already chunked: {skipped_count}")
    print("📂 Chunks saved in chunks/ folder.")


if __name__ == "__main__":
    main()
