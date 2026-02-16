from pydantic import BaseModel


class RepoAnalyzeRequest(BaseModel):
    repo_url: str


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
