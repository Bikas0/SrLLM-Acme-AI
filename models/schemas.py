from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    content: str
    filename: str

class IngestResponse(BaseModel):
    message: str
    document_id: str
    language: str
    chunks_processed: int

class RetrievalRequest(BaseModel):
    query: str

class DocumentResponse(BaseModel):
    content: str
    filename: str
    similarity_score: float
    language: str
    document_id: str

class GenerationRequest(BaseModel):
    query: str
    documents: List[dict]  # List of documents with content and similarity_score

class GenerationResponse(BaseModel):
    query: str
    response_en: str
    response_ja: str

class RetrievalResponse(BaseModel):
    content: str
    similarity_score: float

class StandardResponse(BaseModel):
    status: bool
    message: str
    data: Optional[dict] = None