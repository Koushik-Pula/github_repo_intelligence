from fastapi import APIRouter, HTTPException
from langchain_core.documents import Document

from app.api.schemas import RepoAnalyzeRequest, ChatRequest, ChatResponse
from app.ingestion.github_loader import clone_repo
from app.ingestion.file_filter import collect_source_files
from app.parsing.code_parser import parse_python_file
from app.parsing.chunker import create_code_chunks
from app.embeddings.embedder import HFEmbeddings
from app.embeddings.vector_store import VectorStore
from app.rag.rag_pipeline import build_rag_chain

router = APIRouter()

# --- Init once ---
embeddings = HFEmbeddings()
vector_store = VectorStore(embeddings)
retriever = vector_store.get_retriever(k=5)
rag_chain = build_rag_chain(retriever)


@router.post("/repo/analyze")
def analyze_repo(request: RepoAnalyzeRequest):
    try:
        repo_path = clone_repo(request.repo_url)
        files = collect_source_files(repo_path)

        documents = []

        for file_path in files:
            if file_path.endswith(".py"):
                parsed = parse_python_file(file_path)
                chunks = create_code_chunks(parsed, file_path)

                for chunk in chunks:
                    documents.append(
                        Document(
                            page_content=chunk["page_content"],
                            metadata=chunk["metadata"],
                        )
                    )

        vector_store.add_documents(documents)

        return {
            "status": "success",
            "chunks_indexed": len(documents),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/repo/chat", response_model=ChatResponse)
def chat_repo(request: ChatRequest):
    try:
        response = rag_chain.invoke(request.question)
        return ChatResponse(answer=response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
