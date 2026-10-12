# GitHub Repo Intelligence System

An end-to-end Retrieval-Augmented Generation (RAG) platform that indexes multi-file GitHub codebases and enables context-grounded semantic search and reasoning over source code.

Built with FastAPI, LangChain, Pinecone Serverless, and LLaMA 3 (via Ollama).

---

## Architecture Flow

+-------------------+
|   GitHub Repo     |
+---------+---------+
          |  (Shallow Clone --depth 1)
          v
+-------------------+
| Ingestion & AST   |
| Code Splitter     |
+---------+---------+
          |
          v
+-------------------+
| Hugging Face      |
| Embeddings        |
+---------+---------+
          |
          v
+------------------+  Query   +-------------------+   Top-K Chunks   +------------------+
| User / Streamlit | -------> | FastAPI Backend   | <--------------> | Pinecone (Vector |
| Client           | <------- | (RAG Orchestrator)|                  | Namespace / Repo)|
+------------------+  Answer  +---------+---------+                  +------------------+
                                  |
                                  v
                        +-------------------+
                        | Ollama (LLaMA 3)  |
                        | Context Grounding |
                        +-------------------+

### Core Pipeline:
1. Targeted Ingestion: Clones repositories using shallow depth (--depth 1) and filters out binaries, lock files, and dependencies (.git, node_modules, venv, *.png).
2. Syntax-Aware Chunking: Recursively segments source code using language-specific separators to preserve complete function and class boundaries.
3. Isolated Vector Storage: Vectors are generated using Hugging Face Sentence Transformers and upserted into isolated Pinecone namespaces per repository to eliminate cross-codebase data leakage.
4. Context-Grounded Retrieval: Injects top-k semantic code chunks into a strict hallucination-resistant prompt before querying local LLaMA 3 via Ollama.

---

## Tech Stack

- Orchestration & API: FastAPI, LangChain, Uvicorn
- Vector Database: Pinecone (Serverless)
- Embeddings: Hugging Face (sentence-transformers/all-MiniLM-L6-v2)
- LLM Inference: Ollama (llama3:8b)
- Frontend: Streamlit
- Language: Python 3.10+

---

## Project Structure

app/
|-- api/             # FastAPI routers & request/response schemas
|-- embeddings/      # Vector encoding & Pinecone client management
|-- ingestion/       # Git shallow clone & file discovery filters
|-- parsing/         # Code chunking & AST boundary splitting
|-- rag/             # LCEL retrieval chains & system prompt templates
|-- config.py        # Pydantic environment configurations
`-- main.py          # FastAPI application factory
frontend/
`-- streamlit_app.py # Interactive codebase explorer UI
data/
`-- repos/           # Local repository staging (ephemeral)
requirements.txt
.env.example
README.md

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Ollama installed and running
- Pinecone account & API key

### 2. Pull the Local Model
ollama pull llama3

### 3. Environment Configuration
Clone the repository and set up your .env:

git clone https://github.com/Koushik-Pula/github_repo_intelligence.git
cd github_repo_intelligence
cp .env.example .env

Configure your .env variables:
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=repo-intelligence
PINECONE_ENVIRONMENT=us-east-1
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

### 4. Installation
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt

### 5. Run the System

Start the FastAPI Service:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Interactive Swagger docs will be live at http://127.0.0.1:8000/docs.

Start the Streamlit UI (Optional):
streamlit run frontend/streamlit_app.py

---

## API Reference

### 1. Index a Repository
POST /repo/analyze

Request:
{
  "repo_url": "https://github.com/fastapi/fastapi"
}

Response:
{
  "status": "success",
  "namespace": "fastapi-fastapi",
  "files_processed": 142,
  "chunks_indexed": 846
}

### 2. Query Codebase
POST /repo/chat

Request:
{
  "namespace": "fastapi-fastapi",
  "question": "How does the dependency injection system resolve sub-dependencies?"
}

Response:
{
  "answer": "FastAPI resolves sub-dependencies through the solve_dependencies function in routing.py by traversing...",
  "sources": [
    {
      "file_path": "fastapi/dependencies/utils.py",
      "lines": "45-98"
    }
  ]
}

---

## Production & Architectural Highlights

- Namespace Partitioning: Vector indices partition each repository into discrete Pinecone namespaces, allowing dynamic multi-tenant ingestion without vector mixing.
- Grounding & Guardrails: Prompt templates enforce strict retrieval constraints; if a symbol, class, or route does not exist within retrieved contexts, the model explicitly flags lack of context rather than hallucinating external implementations.
- AST-Aware Splitting: Avoids naive character chunking by preserving complete function/class declarations during code segmentation.
