import uuid
from typing import List
from langdetect import detect
from sentence_transformers import SentenceTransformer
import numpy as np

from models.schemas import IngestResponse
from utils.text_processor import TextProcessor
from utils.faiss_manager import FAISSManager

class DocumentService:
    def __init__(self, faiss_manager=None):
        self.text_processor = TextProcessor()
        self.faiss_manager = faiss_manager or FAISSManager()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    async def ingest_document(self, content: str, filename: str) -> IngestResponse:
        """
        Ingest a document: detect language, chunk, embed, and store in FAISS.
        """
        document_id = str(uuid.uuid4())
        
        try:
            language = detect(content)
            if language in ['ja', 'jp']:
                language = 'ja'
            else:
                language = 'en'  
        except:
            language = 'en' 
            
        existing_docs = [meta for meta in self.faiss_manager.metadata_store 
                        if meta.get('filename') == filename]
        
        if existing_docs:
            return IngestResponse(
                message=f"Document {filename} already exists",
                document_id=existing_docs[0]['document_id'],
                language=language,
                chunks_processed=0
            )
            
        chunks = self.text_processor.chunk_text(content, language)
        
        if not chunks:
            return IngestResponse(
                message="No valid chunks created from document",
                document_id=document_id,
                language=language,
                chunks_processed=0
            )
        
        embeddings = []
        chunk_metadata = []
        
        for i, chunk in enumerate(chunks):
            embedding = self.embedding_model.encode(chunk)
            embeddings.append(embedding)
            
            metadata = {
                'document_id': document_id,
                'filename': filename,
                'chunk_id': i,
                'content': chunk,
                'language': language
            }
            chunk_metadata.append(metadata)
        
        embeddings_array = np.array(embeddings)
        self.faiss_manager.add_embeddings(embeddings_array, chunk_metadata)
        
        return IngestResponse(
            message="Document ingested successfully",
            document_id=document_id,
            language=language,
            chunks_processed=len(chunks)
        )