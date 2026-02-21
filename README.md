# 🌾 KrishiSaarthi  
### AI-Powered Sustainable Agriculture & Government Scheme Advisory Platform  
**Maharashtra First. India Next.**

---

## 📌 Overview

KrishiSaarthi is a **Multilingual RAG-Based Farmer Assistance System** designed to:

- 📜 Simplify complex Government Scheme documents  
- 🌱 Provide Soil-Aware Crop & Product Recommendations  
- 📊 Introduce a Soil Health Impact Score for sustainable farming  
- 🧠 Deliver Source-Backed AI responses using Retrieval-Augmented Generation (RAG)

We are building **India’s first AI-powered Sustainable Agriculture Decision Platform**, starting with Maharashtra.

---

## 🚨 Problem Statement

Farmers face three major challenges:

1. **Information Asymmetry**  
   Government schemes are buried in lengthy PDFs and GRs.

2. **Fragmented & English-Centric Data**  
   Most advisories are not available in simple regional language.

3. **Soil Health Negligence**  
   Farmers often prioritize short-term yield over long-term soil sustainability.

In Maharashtra:
- Large rainfed regions (Vidarbha, Marathwada)
- Declining soil organic carbon
- High nitrogen overuse patterns
- Limited personalized advisory systems

KrishiSaarthi bridges this gap.

---

## 💡 Our Solution

KrishiSaarthi provides:

### ✅ 1. AI-Based Government Scheme Matching
- Personalized eligibility detection
- Structured step-by-step guidance
- Source-backed answers
- Regional language support

### ✅ 2. Soil Health Impact Score (Core Innovation)
Each agricultural product is evaluated on:

- 📈 Short-Term Yield Boost
- 📉 Long-Term Soil Impact
- ⚖ pH Effect
- ♻ Recovery Period
- 🚫 When NOT to Use

This creates accountability in agricultural recommendations.

### ✅ 3. Digital Soil Health Passport
For every farmer:
- Soil history tracking
- Usage patterns
- Risk prediction
- Sustainable nudges
- Scheme auto-linking

---

## 🏗 System Architecture

### 🔹 Data Ingestion Layer
- Government Scheme PDFs
- Government Resolutions (GRs)
- ICAR & Krishi Vigyan Kendra advisories
- State Agriculture Circulars

### 🔹 Processing Pipeline
- PDF extraction via `pdfplumber`
- OCR via `pytesseract + poppler`
- Text chunking
- Embedding generation
- Vector storage in ChromaDB

### 🔹 Retrieval-Augmented Generation (RAG)
- Semantic search
- Context injection into LLM
- Source-backed answer generation
- Structured JSON outputs

---

## 🧠 Tech Stack

### 🔹 Core AI & NLP
- **LLM API:** Groq API
- **Model:** Llama-3.1-8B-Instant
- **Embedding Model:** SentenceTransformers
- **Embedding Name:** all-MiniLM-L6-v2

### 🔹 Database & Retrieval
- **Vector DB:** ChromaDB (Local Persistent)
- **Storage:** vector_db/chroma.sqlite3
- **Similarity Search:** Semantic Retrieval

### 🔹 Backend
- FastAPI (Python)
- Docker & Docker Compose

### 🔹 Frontend
- React

---

## 📊 Dataset

### Type:
Unstructured Government Documents

### Sources:
- Central Government Scheme PDFs
- Maharashtra State GR Documents
- ICAR advisories
- Soil Health Card references

### Includes:
- Eligibility Criteria
- Benefits
- Application Process
- Crop Advisory
- Best Practices

---

## 🌍 Target Users

### 👩‍🌾 Farmers (Free)
- Scheme Recommendations
- Soil Health Tracking
- Product Advisory
- Risk & Profit Insights

### 🏢 Vendors (Paid)
- Product Listings
- District-Level Targeting
- Sustainability Score-Based Placement
- Analytics Dashboard

---

## 💰 Revenue Model

1. Vendor Listing Fee
2. Featured Placement (Only if Soil Score Acceptable)
3. Vendor Analytics Dashboard
4. Premium Farmer Analytics
5. Government Partnerships (Future)

---

## 🛡 Competitive Moat

- AI-based Scheme Matching Engine
- Soil Health Impact Score (Unique Differentiator)
- Compounding Soil Data
- Vendor Sustainability Ratings
- Behavioral Nudging System
- Policy Alignment

The longer farmers use the system,
the stronger our predictive intelligence becomes.

---

## 🎯 Vision

We are not building a marketplace.

We are building **India’s Soil Intelligence Layer**.

KrishiSaarthi transforms agriculture from:

Reactive → Predictive  
Yield-Focused → Sustainability-Focused  
Fragmented → Integrated  

---

## 🚀 Future Roadmap

- Voice-Based Queries (Marathi First)
- WhatsApp & SMS Integration
- Hyperlocal Soil Clustering
- IoT Soil Sensor Integration
- District-Level Sustainability Dashboards

---

## 🏆 Positioning Statement

> “KrishiSaarthi is an AI-powered sustainable agriculture platform that connects farmers to government schemes and verified vendors — while protecting their most valuable asset: their soil.”

---

## 👨‍💻 Team

**Syntax Error** 
**Department of Computer Science & Engineering (AI)**  
Vishwakarma Institute of Information Technology  

---

## 📜 License

This project is built for educational and research purposes under a National Hackathon submission.

---

## 🙏 Acknowledgment

We acknowledge:
- Government open data portals
- ICAR advisories
- ISRO Land Degradation Atlas
- Soil Health Card initiative

---

## ⭐ Contribute

Contributions, suggestions, and collaborations are welcome.

Let’s build sustainable agriculture — together.
