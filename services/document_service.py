import uuid
from typing import List
from langdetect import detect
from sentence_transformers import SentenceTransformer
import numpy as np

from models.schemas import IngestResponse
from utils.text_processor import TextProcessor
from utils.faiss_manager import FAISSManager

class DocumentService:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.faiss_manager = FAISSManager()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    async def ingest_document(self, content: str, filename: str) -> IngestResponse:
        """
        Ingest a document: detect language, chunk, embed, and store in FAISS.
        """
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Detect language
        try:
            language = detect(content)
            # Map detected language codes to our supported languages
            if language in ['ja', 'jp']:
                language = 'ja'
            else:
                language = 'en'  # Default to English for unsupported languages
        except:
            language = 'en'  # Default to English if detection fails
            
        # Check if document with same filename already exists
        existing_docs = [meta for meta in self.faiss_manager.metadata_store 
                        if meta.get('filename') == filename]
        
        if existing_docs:
            print(f"Warning: Document {filename} already exists. Skipping to avoid duplicates.")
            return IngestResponse(
                message=f"Document {filename} already exists",
                document_id=existing_docs[0]['document_id'],
                language=language,
                chunks_processed=0
            )
            
        # Chunk the document
        chunks = self.text_processor.chunk_text(content, language)
        
        if not chunks:
            return IngestResponse(
                message="No valid chunks created from document",
                document_id=document_id,
                language=language,
                chunks_processed=0
            )
        
        # Generate embeddings for each chunk
        embeddings = []
        chunk_metadata = []
        
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = self.embedding_model.encode(chunk)
            embeddings.append(embedding)
            
            # Store metadata
            metadata = {
                'document_id': document_id,
                'filename': filename,
                'chunk_id': i,
                'content': chunk,
                'language': language
            }
            chunk_metadata.append(metadata)
        
        # Store in FAISS
        embeddings_array = np.array(embeddings)
        self.faiss_manager.add_embeddings(embeddings_array, chunk_metadata)
        
        return IngestResponse(
            message="Document ingested successfully",
            document_id=document_id,
            language=language,
            chunks_processed=len(chunks)
        )