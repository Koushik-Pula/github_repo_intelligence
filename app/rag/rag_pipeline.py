from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from typing import List


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(
        f"File: {doc.metadata.get('file')}\n"
        f"Symbol: {doc.metadata.get('symbol')}\n"
        f"Code:\n{doc.page_content}"
        for doc in docs
    )


def build_rag_chain(retriever):
    prompt = ChatPromptTemplate.from_template(
        """
You are a senior software engineer.

Use ONLY the following code context to answer the question.
If the answer is not present in the context, say "I don't know based on the provided code."

Code Context:
{context}

Question:
{question}

Answer clearly and mention file names or functions when relevant.
"""
    )

    llm = ChatOllama(
        model="llama3",
        temperature=0.2,
    )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    return rag_chain
