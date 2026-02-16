from langchain_pinecone import PineconeVectorStore
from app.config import PINECONE_INDEX_NAME


class VectorStore:
    def __init__(self, embeddings):
        self.vectorstore = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            embedding=embeddings,
        )

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    def get_retriever(self, k: int = 5):
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
