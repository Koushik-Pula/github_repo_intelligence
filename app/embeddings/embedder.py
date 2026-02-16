from typing import List
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


class HFEmbeddings(Embeddings):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()
