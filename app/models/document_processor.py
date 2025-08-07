from typing import List, Dict

import PyPDF2
import docx
import re
import os
from app.file_handlers import download_file  # <-- Correct import

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")

    @staticmethod
    def extract_text_from_url(url: str, temp_dir: str = "temp") -> str:
        """Download and extract text from URL"""
        file_path = None
        try:
            os.makedirs(temp_dir, exist_ok=True)
            file_path = download_file(url, temp_dir)
            
            if url.lower().endswith('.pdf'):
                return DocumentProcessor.extract_text_from_pdf(file_path)
            elif url.lower().endswith(('.docx', '.doc')):
                return DocumentProcessor.extract_text_from_docx(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            raise ValueError(f"Error processing URL: {str(e)}")
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

    @staticmethod
    def split_into_clauses(text: str, min_length: int = 100) -> List[Dict]:
        """Split document text into meaningful clauses"""
        clauses = []
        current_clause = ""
        
        # First split by major sections
        sections = re.split(r'\n\s*(Section|Article|Chapter|Clause)\s+\d+[:\.]?\s*\n', text)
        
        for section in sections:
            if not section.strip():
                continue
                
            # Further split by paragraphs
            paragraphs = re.split(r'\n\s*\n', section)
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                    
                # Check if this starts a new clause
                if re.match(r'^\d+[\.\)]', para) or len(current_clause) + len(para) > 1000:
                    if current_clause and len(current_clause) >= min_length:
                        pass
                        clauses.append({"text": current_clause.strip()})
                    current_clause = para
                else:
                    current_clause += "\n" + para
                    
        if current_clause and len(current_clause) >= min_length:
            pass