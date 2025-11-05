# Healthcare Knowledge Assistant

A RAG-powered backend system that helps clinicians retrieve medical guidelines and research summaries in both English and Japanese.

## Features

- **Bilingual Document Ingestion**: Accept .txt documents in English or Japanese
- **Intelligent Retrieval**: FAISS-powered semantic search with similarity scores
- **AI-Powered Generation**: Mock LLM responses based on retrieved documents
- **Translation Support**: Optional translation between English and Japanese
- **API Security**: API key authentication
- **Containerized Deployment**: Docker support with CI/CD pipeline

## Setup

### Prerequisites

- Python 3.8+
- Docker (optional)

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and set your API key
# API_KEY=your-secret-api-key-here
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /ingest
Ingest .txt documents for indexing.

**Headers:**
- `X-API-Key`: Your API key

**Body:** 
Upload a .txt file using multipart/form-data

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "message": "Document ingested successfully",
    "document_id": "generated-uuid",
    "language": "en",
    "chunks_processed": 3
  }
}
```

### POST /retrieve
Retrieve top-3 relevant documents for a query.

**Headers:**
- `X-API-Key`: Your API key

**Body:**
```json
{
  "query": "What are the latest recommendations for Type 2 diabetes management?"
}
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "documents": [
      {
        "content": "Document content...",
        "similarity_score": 0.85
      }
    ]
  }
}
```

### POST /generate
Generate AI response based on query and provided documents. Returns responses in both English and Japanese.

**Headers:**
- `X-API-Key`: Your API key

**Body:**
```json
{
  "query": "How many minutes of physical activity are recommended per week?",
  "documents": [
    {
      "content": "Type 2 Diabetes Management Guidelines recommend at least 150 minutes of physical activity per week for adults.",
      "similarity_score": 0.95
    },
    {
      "content": "Regular physical activity is important for weight management and blood sugar control in Type 2 diabetes.",
      "similarity_score": 0.90
    }
  ]
}
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "query": "How many minutes of physical activity are recommended per week?",
    "response_en": "Based on your query, here's what I found from the medical guidelines: Type 2 Diabetes Management Guidelines recommend at least 150 minutes of physical activity per week for adults...",
    "response_ja": "お問い合わせについて、医療ガイドラインに基づいてお答えします：2型糖尿病管理ガイドラインでは、成人に対して週に少なくとも150分の身体活動を推奨しています..."
  }
}
```

**Bilingual Feature:**
- Always returns both English (`response_en`) and Japanese (`response_ja`) responses
- No need to specify output language - both are provided automatically

## Design Notes

### Scalability
The system is designed with horizontal scalability in mind. FAISS indices can be distributed across multiple nodes, and the FastAPI application can be deployed behind a load balancer. The modular architecture allows for easy scaling of individual components like the embedding service or translation module.

### Modularity
The codebase follows a clean separation of concerns with dedicated modules for document processing, embedding generation, retrieval, and translation. This modular approach facilitates maintenance, testing, and future feature additions while keeping the core functionality isolated and reusable.

## Docker Deployment

Build and run with Docker:

```bash
docker build -t healthcare-assistant .
docker run -p 8000:8000 -e API_KEY=your-secret-key healthcare-assistant
```

## CI/CD Pipeline

The project includes GitHub Actions workflow for automated deployment. The pipeline:
1. Builds Docker image
2. Pushes to container registry
3. Deploys to staging/production environments