from langchain.llms import OpenAI
from app.config import settings

def query_llm(prompt: str) -> str:
    llm = OpenAI(api_key=settings.OPENAI_API_KEY, temperature=0.7)
    return llm(prompt)