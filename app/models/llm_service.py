import google.generativeai as genai
import json
from typing import List, Dict
from app.config import settings

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.LLM_MODEL)
        self.generation_config = {
            "temperature": 0.3,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    
    def generate_response(self, query: str, context: List[str]) -> Dict:
        context_str = "\n\n".join([f"Reference {i+1}:\n{text}" for i, text in enumerate(context)])
        
        prompt = f"""You are a professional document analyst. Answer questions based on these references:
        
        {context_str}
        
        Question: {query}
        
        Provide response as JSON with:
        - "answer": Direct answer
        - "clauses": Relevant clauses
        - "conditions": Any conditions
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            response_text = response.text
            
            # Clean JSON response if wrapped in markdown
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()
                
            return json.loads(response_text)
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "clauses": context,
                "conditions": "Unable to parse response"
            }