# 🚀 Enterprise RAG Platform with Guardrails, Evaluation & Observability

A production-style Retrieval-Augmented Generation (RAG) system built with modern LLM engineering practices.
This project goes beyond a basic chatbot by integrating hybrid retrieval, reranking, hallucination detection, guardrails, and performance monitoring.

**🧠 Overview**

This platform enables users to query documents using natural language while ensuring:

* Accurate retrieval (Hybrid Search)

* High-quality answers (Reranking)

* Reliable outputs (Confidence + Hallucination detection)

* Safe responses (Toxicity guardrails)

* Observability (Latency + logging)

🏗️ Architecture

User Query

   ↓

🛡️ Input Guardrail (Toxicity Check)

   ↓

🔍 Hybrid Retrieval

   ├── FAISS (Semantic Search)

   └── BM25 (Keyword Search)

   ↓

🔄 Merge + Deduplicate

   ↓

📊 Cross-Encoder Reranker

   ↓

🤖 LLM (OpenRouter)

   ↓

🛡️ Output Guardrail (Toxicity Check)

   ↓

📈 Evaluation

   ├── Confidence Score

   └── RAGAS (Faithfulness)

   ↓

⏱️ Latency Tracking + Logging

   ↓

📦 API Response

✨ Features
🔍 Retrieval & Ranking

Hybrid search (FAISS + BM25)

Cross-encoder reranker (BGE reranker)

Multi-document support

🤖 LLM Integration

OpenRouter support (plug-and-play models)

Modular LLM abstraction

📊 Evaluation

RAGAS-based hallucination detection (faithfulness)

Custom confidence scoring

🛡️ Guardrails

Input toxicity filtering

Output toxicity filtering

Response validation

⏱️ Observability

Latency tracking (retrieval, rerank, generation)

Structured logging

📦 API

FastAPI-based REST API

Swagger UI for testing

🐳 Deployment

Fully Dockerized

One-command startup

🧰 Tech Stack

         | Component      | Technology        |
         | -------------- | ----------------- |
         | Backend        | FastAPI           |
         | LLM            | OpenRouter        |
         | Embeddings     | BGE (HuggingFace) |
         | Vector DB      | FAISS             |
         | Keyword Search | BM25              |
         | Reranker       | BGE Cross-Encoder |
         | Evaluation     | RAGAS             |
         | Guardrails     | Toxic-BERT        |
         | Deployment     | Docker            |

⚙️ Setup Instructions

1️⃣ Clone the 

   git clone <your-repo-url>
   cd evalguard-rag

2️⃣ Create .env File

   OPENROUTER_API_KEY=your_key
   OPENROUTER_MODEL=mistralai/mistral-7b-instruct

3️⃣ Run with Docker

   docker-compose up

4️⃣ Open API Docs

   http://localhost:8000/docs

📥 Ingest Documents

   python ingest.py --file data/your_document.pdf

Supports:

Multi-document ingestion

Deduplication via hashing

Metadata tracking (file + page)

📡 API Usage

Endpoint
   POST /query
   
   Request

   {

   "question": "What are AI agents?"

   }
   
   Response
   
   {

   "answer": "AI agents are autonomous systems...",

   "confidence": 0.84,

   "faithfulness": 0.91,

   "sources": [

      {

         "file": "Google-AI_Agents.pdf",

         "page": 4

      }

   ],

   "latency": {

      "retrieval": 0.05,

      "rerank": 0.21,

      "generation": 1.14,

      "total": 1.40

   }

   }

🧠 Key Design Decisions

🔹 Hybrid Retrieval

Combines semantic + keyword search to improve recall and accuracy.

🔹 Reranking

Uses cross-encoder to refine top results → reduces hallucination.

🔹 Confidence Scoring

Combines retrieval + rerank + answer quality signals.

🔹 RAGAS Integration

Measures faithfulness to detect hallucinations.

🔹 Guardrails

Ensures both user input and model output are safe.

📊 Observability

The system tracks:

retrieval latency

reranking latency

generation latency

total response time

Logs stored in:

logs/rag.log

🛡️ Safety Features

Input toxicity blocking

Output moderation

Answer validation

Hallucination detection

📁 Project Structure
  
   evalguard-rag/

   │

   ├── api/

   ├── ingestion/

   ├── retrieval/

   ├── orchestration/

   ├── evaluation/

   ├── guardrails/

   ├── monitoring/

   ├── metadata/

   ├── config/

   │

   ├── data/

   ├── logs/

   │

   ├── ingest.py

   ├── Dockerfile

   ├── docker-compose.yml

   ├── requirements.txt

   └── README.md
