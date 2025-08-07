from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List
import json
from app.models.document_processor import DocumentProcessor
from app.models.embedding_service import EmbeddingService
from app.models.llm_service import LLMService
from app.config import settings

router = APIRouter(prefix="/api/v1")

AUTH_TOKEN = "2ba7e23413aa9c18fcb9af91082538112408d29f6fcd314fdbb5ccab13b688b6"

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid authorization token")

@router.post("/hackrx/run", dependencies=[Depends(verify_token)])
async def process_documents(
    documents: str,
    questions: List[str]
):
    try:
        # Initialize services
        doc_processor = DocumentProcessor()
        embedding_service = EmbeddingService()
        llm_service = LLMService()
        
        # Process document
        document_text = doc_processor.extract_text_from_url(documents)
        clauses = doc_processor.split_into_clauses(document_text)
        embedding_service.upsert_documents(clauses)
        
        # Process questions
        answers = []
        for question in questions:
            relevant_clauses = embedding_service.semantic_search(question)
            context = [clause["text"] for clause in relevant_clauses]
            response = llm_service.generate_response(question, context)
            answers.append(response)
        
        return {"answers": answers}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))