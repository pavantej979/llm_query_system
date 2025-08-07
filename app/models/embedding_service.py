import pinecone
import google.generativeai as genai  # Fixed module name
from typing import List, Dict
from app.config import settings

class EmbeddingService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        pinecone.init(
            api_key=settings.PINECONE_API_KEY, 
            environment=settings.PINECONE_ENV  # Added missing environment variable
        )
        if settings.PINECONE_INDEX not in pinecone.list_indexes():  # Added missing colon
            pinecone.create_index(
                name=settings.PINECONE_INDEX,
                dimension=768,  # Gemini embeddings are 768-dimensional
                metric="cosine"
            )
        self.index = pinecone.Index(settings.PINECONE_INDEX)  # Fixed capitalization of Index
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        result = genai.embed_content(
            model=settings.EMBEDDING_MODEL,
            content=texts,
            task_type="retrieval_document"
        )
        if isinstance(texts, str) or len(texts) == 1:
            return [result['embedding']]
        return result['embeddings']
    
    def upsert_documents(self, documents: List[Dict]):
        texts = [doc["text"] for doc in documents]
        embeddings = self.get_embeddings(texts)
        vectors = []
        for idx, (doc, embedding) in enumerate(zip(documents, embeddings)):
            vectors.append({
                "id": f"vec_{idx}",
                "values": embedding,
                "metadata": {"text": doc["text"]}
            })
        self.index.upsert(vectors=vectors)
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.get_embeddings([query])[0]
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return [match.metadata for match in results.matches]