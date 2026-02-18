import fitz  # PyMuPDF
import os
from pathlib import Path

# OCR imports
from pdf2image import convert_from_path
import pytesseract

INPUT_DIR = "new_pdfs"
OUTPUT_DIR = "extracted_text"

# If text is too small, use OCR
MIN_TEXT_LENGTH = 200


def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []

    for page in doc:
        text = page.get_text("text")
        if text:
            full_text.append(text)

    doc.close()
    return "\n".join(full_text)


def extract_text_ocr(pdf_path):
    images = convert_from_path(pdf_path, dpi=150)  # 150 = faster
    full_text = []

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang="eng")
        full_text.append(text)

    return "\n".join(full_text)


def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in new_pdfs/")
        return

    print(f"Found {len(pdf_files)} PDFs...\n")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        txt_name = pdf_file.rsplit(".", 1)[0] + ".txt"
        output_path = os.path.join(OUTPUT_DIR, txt_name)

        # Skip if already extracted
        if os.path.exists(output_path):
            print(f" ✅ Skipped (already extracted): {pdf_file}")
            continue

        print(f"\n📌 Processing: {pdf_file}")

        try:
            # Step 1: Normal extraction
            text = extract_text_pymupdf(pdf_path)

            # Step 2: If too small, use OCR
            if len(text.strip()) < MIN_TEXT_LENGTH:
                print("  Text is very small. Using OCR...")
                text = extract_text_ocr(pdf_path)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f" Saved: {txt_name}")

        except Exception as e:
            print(f"   Failed: {pdf_file} | Error: {e}")

    print("\n Phase 2 Done! Text files saved in extracted_text/")


if __name__ == "__main__":
    main()
