from typing import List
from sentence_transformers import SentenceTransformer
from langdetect import detect

from models.schemas import DocumentResponse
from utils.faiss_manager import FAISSManager

class RetrievalService:
    def __init__(self, faiss_manager=None):
        self.faiss_manager = faiss_manager or FAISSManager()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    async def retrieve(self, query: str, top_k: int = 3) -> List[DocumentResponse]:
        """
        Retrieve top-k relevant documents for a query.
        """
        # Detect query language
        try:
            query_language = detect(query)
            if query_language in ['ja', 'jp']:
                query_language = 'ja'
            else:
                query_language = 'en'
        except:
            query_language = 'en'
            
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Search in FAISS
        results = self.faiss_manager.search(query_embedding, top_k)
        
        # Convert to response format
        document_responses = []
        for metadata, score in results:
            doc_response = DocumentResponse(
                content=metadata['content'],
                filename=metadata['filename'],
                similarity_score=float(score),
                language=metadata['language'],
                document_id=metadata['document_id']
            )
            document_responses.append(doc_response)
            
        return document_responses