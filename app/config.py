from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in environment variables")

if not PINECONE_INDEX_NAME:
    raise ValueError("PINECONE_INDEX_NAME not found in environment variables")
