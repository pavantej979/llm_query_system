from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Replace OpenAI with Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Pinecone remains the same
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX", "policy-documents")
    
    # Model Configuration for Gemini
    EMBEDDING_MODEL = "models/embedding-001"  # Gemini embedding model
    LLM_MODEL = "gemini-pro"  # Gemini Pro model
    
    API_TITLE = "LLM Query Retrieval System (Gemini)"
    API_DESCRIPTION = "Using Google Gemini for document processing"

settings = Settings()