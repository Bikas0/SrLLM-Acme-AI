from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile, File
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from services.document_service import DocumentService
from services.retrieval_service import RetrievalService
from services.generation_service import GenerationService
from services.translation_service import TranslationService
from models.schemas import IngestRequest, RetrievalRequest, GenerationRequest, DocumentResponse, RetrievalResponse, StandardResponse

app = FastAPI(
    title="Healthcare Knowledge Assistant",
    description="RAG-powered assistant for medical guidelines and research summaries",
    version="1.0.0"
)

# Initialize services
document_service = DocumentService()
retrieval_service = RetrievalService()
generation_service = GenerationService()
translation_service = TranslationService()

# Security
security = HTTPBearer()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required. Please set it in your .env file.")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
) -> StandardResponse:
    """
    Ingest a .txt document for indexing.
    Detects language, generates embeddings, and stores in FAISS.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.txt'):
            return StandardResponse(
                status=False,
                message="Only .txt files are supported",
                data=None
            )
        
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Process the document
        result = await document_service.ingest_document(
            content=text_content,
            filename=file.filename
        )
        
        return StandardResponse(
            status=True,
            message="success",
            data={
                "message": result.message,
                "document_id": result.document_id,
                "language": result.language,
                "chunks_processed": result.chunks_processed
            }
        )
    except UnicodeDecodeError:
        return StandardResponse(
            status=False,
            message="File must be valid UTF-8 encoded text",
            data=None
        )
    except Exception as e:
        return StandardResponse(
            status=False,
            message="fail",
            data={"error": str(e)}
        )



@app.post("/retrieve")
async def retrieve_documents(
    request: RetrievalRequest,
    api_key: str = Depends(verify_api_key)
) -> StandardResponse:
    """
    Retrieve top-3 relevant documents for a query.
    Returns documents with similarity scores.
    """
    try:
        results = await retrieval_service.retrieve(
            query=request.query,
            top_k=3
        )
        
        # Convert to response format
        documents = [
            {
                "content": doc.content,
                "similarity_score": doc.similarity_score
            }
            for doc in results
        ]
        
        return StandardResponse(
            status=True,
            message="success",
            data={"documents": documents}
        )
    except Exception as e:
        return StandardResponse(
            status=False,
            message="fail",
            data={"error": str(e)}
        )

@app.post("/generate")
async def generate_response(
    request: GenerationRequest,
    api_key: str = Depends(verify_api_key)
) -> StandardResponse:
    """
    Generate AI response based on query and provided documents.
    Returns responses in both English and Japanese.
    """
    try:
        # Convert input documents to DocumentResponse objects
        documents = []
        for doc in request.documents:
            doc_response = DocumentResponse(
                content=doc["content"],
                filename="provided_document",
                similarity_score=doc["similarity_score"],
                language="en",  # Default language
                document_id="provided"
            )
            documents.append(doc_response)
        
        # Generate response in both languages
        response = await generation_service.generate(
            query=request.query,
            documents=documents
        )
        
        return StandardResponse(
            status=True,
            message="success",
            data={
                "query": response.query,
                "response_en": response.response_en,
                "response_ja": response.response_ja
            }
        )
    except Exception as e:
        return StandardResponse(
            status=False,
            message="fail",
            data={"error": str(e)}
        )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)