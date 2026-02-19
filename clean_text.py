import os
import re
from pathlib import Path

INPUT_DIR = "extracted_text"
OUTPUT_DIR = "clean_text"

def clean_text(text: str) -> str:
    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove page numbers like "Page 1"
    text = re.sub(r"\n\s*Page\s*\d+\s*\n", "\n", text, flags=re.IGNORECASE)

    # Remove lines that are only a number (common page number)
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Fix broken lines: join lines if previous line doesn't end with punctuation
    lines = text.split("\n")
    fixed_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            fixed_lines.append("")
            continue

        if fixed_lines and fixed_lines[-1] and not fixed_lines[-1].endswith((".", ":", ";", "?", "!", ")")):
            fixed_lines[-1] += " " + line
        else:
            fixed_lines.append(line)

    text = "\n".join(fixed_lines)

    # Again remove extra blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    txt_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".txt")]

    if not txt_files:
        print("No TXT files found in extracted_text/")
        return

    print(f"✅ Found {len(txt_files)} extracted text files.\n")

    cleaned_count = 0
    skipped_count = 0

    for file in txt_files:
        input_path = os.path.join(INPUT_DIR, file)
        output_path = os.path.join(OUTPUT_DIR, file)

        # Skip if already cleaned
        if os.path.exists(output_path):
            print(f"⏩ Skipped (already cleaned): {file}")
            skipped_count += 1
            continue

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"✅ Cleaned: {file}")
        cleaned_count += 1

    print("\n Phase 3 Done!")
    print(f"Newly cleaned files: {cleaned_count}")
    print(f"Skipped already cleaned: {skipped_count}")
    print("📂 Clean files saved in clean_text/ folder.")


if __name__ == "__main__":
    main()
