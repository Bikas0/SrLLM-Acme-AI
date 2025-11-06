from typing import List, Optional
from langdetect import detect

from models.schemas import DocumentResponse, GenerationResponse
from services.translation_service import TranslationService

class GenerationService:
    def __init__(self):
        self.translation_service = TranslationService()
        
    async def generate(
        self, 
        query: str, 
        documents: List[DocumentResponse]
    ) -> GenerationResponse:
        """
        Generate a mock LLM response based on query and retrieved documents.
        Returns responses in both English and Japanese via translation.
        """
        # Detect document language
        document_content = documents[0].content if documents else ""
        is_japanese_doc = any(ord(char) > 127 for char in document_content)
        
        if is_japanese_doc:
            # Japanese documents: Generate Japanese response, translate to English
            response_ja = self._generate_response_from_documents(documents)
            response_en = await self.translation_service.translate_text(
                response_ja,
                target_language="en", 
                source_language="ja"
            )
        else:
            # English documents: Generate English response, translate to Japanese
            response_en = self._generate_response_from_documents(documents)
            response_ja = await self.translation_service.translate_text(
                response_en,
                target_language="ja", 
                source_language="en"
            )
        
        return GenerationResponse(
            query=query,
            response_en=response_en,
            response_ja=response_ja
        )
        
    def _generate_response_from_documents(self, documents: List[DocumentResponse]) -> str:
        """Generate response directly from documents in their original language."""
        
        if not documents:
            return "I apologize, but I couldn't find any relevant documents for your query."
        
        # Use document content directly in its original language
        document_content = documents[0].content
        
        # Detect if it's Japanese or English and add appropriate wrapper
        is_japanese = any(ord(char) > 127 for char in document_content)
        
        if is_japanese:
            # Japanese response format
            response = (
                f"{document_content}")
        else:
            # English response format
            response = (
                f"{document_content}")
            
        return response