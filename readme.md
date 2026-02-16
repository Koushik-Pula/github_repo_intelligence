# GitHub Repo Intelligence System

A Retrieval-Augmented Generation (RAG) based system that allows users to analyze and interact with any GitHub repository.

Users can:
- Index a GitHub repository
- Ask natural language questions about the codebase
- Receive context-aware answers grounded in actual source code

---

## Features

- GitHub repository ingestion
- Code parsing and chunking (Python support)
- Semantic embeddings using Hugging Face
- Vector storage using Pinecone
- Namespace-based repository isolation
- RAG pipeline using LangChain
- FastAPI backend
- (Optional) Streamlit frontend

---

## Architecture Overview

User → FastAPI → RAG Pipeline → Pinecone → LLM (LLaMA3 via Ollama)

### Step-by-step flow:

1. User submits GitHub repo URL
2. Repo is cloned locally
3. Source files are parsed and chunked
4. Chunks are converted into embeddings
5. Embeddings are stored in Pinecone (namespace = repo name)
6. User asks questions
7. Query embedding retrieves relevant code chunks
8. Retrieved chunks are injected into prompt
9. LLM generates grounded answer

---

## Project Structure

app/
├── api/                # FastAPI routes
├── embeddings/         # Hugging Face embeddings + Pinecone integration
├── ingestion/          # GitHub cloning & file collection
├── parsing/            # Code parsing & chunking
├── rag/                # RAG pipeline (retriever + prompt + LLM)
├── config.py           # Environment configuration
└── main.py             # FastAPI entry point

data/
└── repos/              # Locally cloned repositories

---

## Tech Stack

- Python
- FastAPI
- LangChain
- Pinecone (Vector DB)
- Hugging Face Sentence Transformers
- Ollama (LLaMA3 local LLM)
- Streamlit (optional frontend)

---

## Environment Variables

Create a `.env` file in the project root:

PINECONE_API_KEY=your_api_key_here  
PINECONE_INDEX_NAME=repo-intelligence  

Do NOT commit this file to GitHub.

---

## Running the Backend

1. Activate virtual environment:

   venv\Scripts\activate   (Windows)

2. Start FastAPI:

   uvicorn app.main:app --reload

3. Open:

   http://127.0.0.1:8000/docs

---

## API Endpoints

### POST /repo/analyze

Indexes a GitHub repository into Pinecone.

Request body:
{
  "repo_url": "https://github.com/owner/repo"
}

Response:
{
  "status": "success",
  "repo": "repo_name",
  "chunks_indexed": 42
}

---

### POST /repo/chat

Ask a question about a previously indexed repository.

Request body:
{
  "repo": "repo_name",
  "question": "How is preprocessing implemented?"
}

Response:
{
  "answer": "..."
}

---

## Namespace Design

Each repository is stored in a separate Pinecone namespace:

Index: repo-intelligence
  ├── namespace: repoA
  ├── namespace: repoB
  └── namespace: repoC

This ensures:
- No cross-repo contamination
- Clean retrieval isolation
- Easy deletion per repository

---

## Hallucination Control

The RAG prompt enforces:

- Answers must use retrieved code only
- No assumptions about missing files
- Clear refusal if concept not found

This reduces hallucinations significantly.

---

## Future Improvements

- Add conversational memory
- Add multi-language support
- Add repo management UI
- Add streaming responses
- Add source citations in answers
- Add repo deletion endpoint

---

## Interview Talking Points

- Implemented RAG over real-world codebases
- Used Pinecone namespaces for repo isolation
- Designed retrieval-first architecture
- Reduced hallucination using strict prompt grounding
- Built full-stack GenAI system (FastAPI + LLM + Vector DB)

---

## License

For educational and demonstration purposes.
