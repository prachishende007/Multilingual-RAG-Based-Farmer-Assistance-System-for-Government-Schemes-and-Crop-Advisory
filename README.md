# Multilingual-RAG-Based-Farmer-Assistance-System-for-Government-Schemes-and-Crop-Advisory

KrishiSaarthi – Government Scheme RAG + Knowledge Base (NLP Project)

KrishiSaarthi is an AI-powered Government Scheme Assistant built using RAG (Retrieval Augmented Generation) for farmers.
It allows users to ask questions about agriculture-related schemes and get accurate answers from official PDF documents.

This project contains:

✅ PDF → Text Extraction
✅ Text Chunking
✅ Vector Database (ChromaDB)
✅ Semantic Search (Sentence Transformers)
✅ RAG Chatbot using Groq LLM
✅ Knowledge Base JSON Extraction (Dashboard-ready)

🎯 Project Goal

To build a system that can:

Store official Government Scheme PDFs

Convert them into searchable chunks

Retrieve the best matching scheme content for a farmer question

Generate a final answer using an LLM

Also generate a structured JSON knowledge base for dashboard display

🧠 Models Used
✅ Embedding Model (for Vector DB)

sentence-transformers/all-MiniLM-L6-v2

Used for:

Converting text chunks into embeddings

Semantic search inside ChromaDB

✅ LLM Model (for Chatbot + JSON extraction)

Groq model: llama-3.1-8b-instant

Used for:

Generating final farmer-friendly answers

Extracting structured JSON scheme information

🏗️ System Architecture (High Level)
Phase 1: PDF → Text

Government PDFs are converted into clean .txt files.

📌 Output:

data/txt_files/*.txt

Phase 2: Chunking

Large text files are broken into smaller chunks (ex: 400–700 words).

📌 Output:

chunks/*.txt

Phase 3: Embeddings + Vector DB

Each chunk is embedded using SentenceTransformer and stored in ChromaDB.

📌 Output:

vector_db/ (local ChromaDB storage)

Phase 4: RAG Chatbot

User question → embedded → retrieve top chunks → send to LLM → final answer.

📌 Output:

Answer + Sources (document names)

Phase 5B: Knowledge Base JSON (Dashboard-ready)

For each document, the system generates a structured JSON file containing:

Scheme Name

Eligibility

Benefits

Documents required

Application steps

Official links

Contact details

etc.

📌 Output:

knowledge_base/schemes/*.json

📂 Folder Structure
KrishiSaarthi/
│
├── data/
│   ├── pdfs/                      # Input PDFs (optional)
│   └── txt_files/                 # Extracted text from PDFs
│
├── chunks/                        # Chunked text for embedding
│
├── vector_db/                     # ChromaDB local storage (ignored in git)
│
├── knowledge_base/
│   ├── schemes/                   # Final JSON output (1 JSON per document)
│   └── raw_llm_outputs/           # Debug raw LLM outputs (optional)
│
├── embed_chunks.py                # Creates embeddings & stores in ChromaDB
├── search_chunks.py               # Semantic search testing
├── RAG_Chatbot_Groq.py            # Final RAG chatbot (Groq)
│
└── requirements.txt

⚙️ Setup Instructions
✅ Step 1: Create Virtual Environment
python -m venv .venv


Activate:

Windows

.venv\Scripts\activate

✅ Step 2: Install Dependencies
pip install -r requirements.txt

✅ Step 3: Add Groq API Key

Create a .env file in root folder:

GROQ_API_KEY=your_groq_api_key_here


⚠️ .env must NOT be uploaded to GitHub.

🚀 How to Run the Project
✅ (A) Build Vector Database (Embeddings)

This step creates the vector DB from chunk files.

python embed_chunks.py


📌 Output:

ChromaDB stored locally in vector_db/

✅ (B) Test Semantic Search

This checks if retrieval works properly.

python search_chunks.py


You will see:

Top matching chunks

Source document names

✅ (C) Run the Farmer RAG Chatbot (Groq)

This is the main chatbot file.

python RAG_Chatbot_Groq.py


Example:

👨‍🌾 Farmer Question:

What is PM-Kisan scheme and how much money is given?


🤖 Answer:

Generated response

Sources used

✅ (D) Build Knowledge Base JSON (Dashboard Ready)

This step generates 1 JSON file per document.

python knowledge_base/scripts/build_scheme_json.py


📌 Output:

knowledge_base/schemes/*.json

🌾 Sample Farmer Questions

Try these:

What is PM-Kisan scheme and how much money is given?

How to apply for PMFBY crop insurance?

What are the benefits of Soil Health Card?

How often Soil Health Card is issued?

Who is eligible for PM-KMY pension scheme?

What documents are required for PMKSY scheme?

What is PKVY scheme and how farmers can apply?

📌 Why RAG is Used?

Instead of training a model, RAG allows:

Using real government documents as knowledge

Avoiding hallucination

Answering using sources

Easy updating (just add new PDFs)

📊 Dashboard Support (Future Scope)

The JSON files created in knowledge_base/schemes/ can be used directly in a dashboard to show:

Scheme overview

Eligibility criteria

Benefits

Step-by-step process

Required documents

Official links

🔐 Security Notes

This repo uses .gitignore to avoid uploading:

.env (API keys)

.venv (virtual environment)

vector_db/ (local database)

*.sqlite3

👨‍💻 Tech Stack

Python

Sentence Transformers

ChromaDB

Groq LLM

RAG Pipeline

JSON Knowledge Base Builder

📌 Author / Team

This module is developed as part of the KrishiSaarthi project for:

📍 Government Schemes NLP + RAG + Knowledge Base generation
