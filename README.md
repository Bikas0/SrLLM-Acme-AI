# Healthcare Knowledge Assistant for Acme AI Ltd.

A RAG-powered backend system developed as part of the Sr. LLM / Backend Engineer assignment. This system helps clinicians retrieve medical guidelines and research summaries in both English and Japanese languages.

## Features

- **Bilingual Document Processing**: Ingest and process .txt documents in both English and Japanese
- **Smart Retrieval System**: FAISS-powered semantic search with top-3 relevancy scoring
- **Mock LLM Generation**: Contextual response generation based on retrieved documents
- **Bilingual Support**: Complete English and Japanese language support
- **Translation Capabilities**: Optional language toggle between English (en) and Japanese (ja)
- **Secure API Access**: Implementation of API key authentication
- **Modern Deployment**: Containerized solution with automated CI/CD pipeline

## Technical Requirements

### Core Dependencies

- Python 3.9+
- FastAPI framework
- FAISS for vector similarity search
- Sentence Transformers for embeddings
- Docker for containerization

### Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Bikas0/SrLLM-Acme-AI.git

cd SrLLM-Acme-AI
```

2. Create Virtual Environment

```bash
conda create -p venv python=3.9 -y

conda activate ./venv
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Configure API security at .env file:

```bash
API_KEY=SrLLM-Acme-AI2025
```

5. Launch the application:
```bash
python main.py
```

The service will be accessible at `http://localhost:8000`

### AI Usage Disclaimer
This project has been developed without the use of AI tools (Copilot, ChatGPT, Gemini, etc.) as per assignment requirements.

## API Documentation

### Document Ingestion (POST /ingest)
Endpoint for ingesting medical documents in either English or Japanese.

**Security:**
- Header: `x-api-key`: SrLLM-Acme-AI2025

**Request:**

```bash
curl -X 'POST' \
  'http://localhost:8000/ingest' \
  -H 'accept: application/json' \
  -H 'x-api-key: SrLLM-Acme-AI2025' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@diabetes_en.txt;type=text/plain'
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "message": "Document ingested successfully",
    "document_id": "fd27587c-6903-4a1e-8d14-8fc471dbb19f",
    "language": "en",
    "chunks_processed": 7
  }
}
```

### Knowledge Retrieval (POST /retrieve)
Semantic search endpoint for finding relevant medical information.

**Security:**
- Header: `x-api-key`: SrLLM-Acme-AI2025

# English Language
**Request:**

```bash
curl -X 'POST' \
  'http://localhost:8000/retrieve' \
  -H 'accept: application/json' \
  -H 'x-api-key: SrLLM-Acme-AI2025' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "How often should kidney function tests be conducted in type 2 diabetes patients?"
}'
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "documents": [
      {
        "content": "4. Regular Health Screenings: - Annual eye examinations for diabetic retinopathy - Kidney function tests every 6-12 months - Cardiovascular risk assessment - Foot examinations for diabetic neuropathy",
        "similarity_score": 0.639164388179779
      },
      {
        "content": "Type 2 Diabetes Management Guidelines Overview: Type 2 diabetes is a chronic condition that affects the way your body metabolizes sugar (glucose). Management requires a comprehensive approach including lifestyle modifications, medication adherence, and regular monitoring. Key Recommendations:",
        "similarity_score": 0.4624072313308716
      },
      {
        "content": "1. Blood Glucose Monitoring: - Check blood glucose levels as recommended by your healthcare provider - Target HbA1c levels should be below 7 for most adults - Monitor for signs of hypoglycemia and hyperglycemia",
        "similarity_score": 0.36771732568740845
      }
    ]
  }
}
```

# Japanese Language 
**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/retrieve' \
  -H 'accept: application/json' \
  -H 'x-api-key: SrLLM-Acme-AI2025' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "病気の日（sick day）の管理計画とは具体的に何を含むべきですか？"
}'
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "documents": [
      {
        "content": "5. 緊急時管理： - 糖尿病性ケトアシドーシスの兆候を知る - 病気の日の管理計画を持つ - 糖尿病診断を示す身分証明書を携帯する - 緊急時のグルコース供給を準備しておく 患者教育： 糖尿病とその管理を理解することは、長期的な成功にとって重要です。患者は適切な栄養、運動、服薬遵守、医療機関への受診時期について教育を受けるべきです。",
        "similarity_score": 0.4793800711631775
      },
      {
        "content": "1. 血糖値モニタリング： - 医療提供者の推奨に従って血糖値をチェックする - 成人の多くでHbA1c値は7未満を目標とする - 低血糖症と高血糖症の兆候をモニターする",
        "similarity_score": 0.42669224739074707
      },
      {
        "content": "4. 定期的な健康診断： - 糖尿病性網膜症の年次眼科検査 - 6-12ヶ月ごとの腎機能検査 - 心血管リスク評価 - 糖尿病性神経障害の足部検査",
        "similarity_score": 0.42118334770202637
      }
    ]
  }
}
```


### Response Generation (POST /generate)
AI-powered response generation with bilingual support.

**Security:**
- Header: `x-api-key`: SrLLM-Acme-AI2025

# English Language
**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'accept: application/json' \
  -H 'x-api-key: SrLLM-Acme-AI2025' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "How often should kidney function tests be conducted in type 2 diabetes patients?",
  "documents":[
      {
        "content": "4. Regular Health Screenings: - Annual eye examinations for diabetic retinopathy - Kidney function tests every 6-12 months - Cardiovascular risk assessment - Foot examinations for diabetic neuropathy",
        "similarity_score": 0.639164388179779
      },
      {
        "content": "Type 2 Diabetes Management Guidelines Overview: Type 2 diabetes is a chronic condition that affects the way your body metabolizes sugar (glucose). Management requires a comprehensive approach including lifestyle modifications, medication adherence, and regular monitoring. Key Recommendations:",
        "similarity_score": 0.4624072313308716
      },
      {
        "content": "1. Blood Glucose Monitoring: - Check blood glucose levels as recommended by your healthcare provider - Target HbA1c levels should be below 7 for most adults - Monitor for signs of hypoglycemia and hyperglycemia",
        "similarity_score": 0.36771732568740845
      }
    ]
}'
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "query": "How often should kidney function tests be conducted in type 2 diabetes patients?",
    "response_en": "4. Regular Health Screenings: - Annual eye examinations for diabetic retinopathy - Kidney function tests every 6-12 months - Cardiovascular risk assessment - Foot examinations for diabetic neuropathy",
    "response_ja": "4. 定期健康診断: - 糖尿病性網膜症に関する眼科検査を年に一度 - 6～12 か月ごとに腎機能検査 - 心血管リスク評価 - 糖尿病性神経障害に関する足の検査"
  }
}
```

# Japanese Language 
**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'accept: application/json' \
  -H 'x-api-key: SrLLM-Acme-AI2025' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "病気の日（sick day）の管理計画とは具体的に何を含むべきですか？",
  "documents":  [
      {
        "content": "5. 緊急時管理： - 糖尿病性ケトアシドーシスの兆候を知る - 病気の日の管理計画を持つ - 糖尿病診断を示す身分証明書を携帯する - 緊急時のグルコース供給を準備しておく 患者教育： 糖尿病とその管理を理解することは、長期的な成功にとって重要です。患者は適切な栄養、運動、服薬遵守、医療機関への受診時期について教育を受けるべきです。",
        "similarity_score": 0.4793800711631775
      },
      {
        "content": "1. 血糖値モニタリング： - 医療提供者の推奨に従って血糖値をチェックする - 成人の多くでHbA1c値は7未満を目標とする - 低血糖症と高血糖症の兆候をモニターする",
        "similarity_score": 0.42669224739074707
      },
      {
        "content": "4. 定期的な健康診断： - 糖尿病性網膜症の年次眼科検査 - 6-12ヶ月ごとの腎機能検査 - 心血管リスク評価 - 糖尿病性神経障害の足部検査",
        "similarity_score": 0.42118334770202637
      }
    ]
}'
```

**Response:**
```json
{
  "status": true,
  "message": "success",
  "data": {
    "query": "病気の日（sick day）の管理計画とは具体的に何を含むべきですか？",
    "response_en": "5. Emergency Management: - Know the signs of diabetic ketoacidosis - Have a sick day management plan - Carry identification showing your diabetes diagnosis - Have an emergency glucose supply ready Patient Education: Understanding diabetes and its management is critical to long-term success. Patients should be educated about proper nutrition, exercise, medication compliance, and when to seek medical attention.",
    "response_ja": "5. 緊急時管理： - 糖尿病性ケトアシドーシスの兆候を知る - 病気の日の管理計画を持つ - 糖尿病診断を示す身分証明書を携帯する - 緊急時のグルコース供給を準備しておく 患者教育： 糖尿病とその管理を理解することは、長期的な成功にとって重要です。患者は適切な栄養、運動、服薬遵守、医療機関への受診時期について教育を受けるべきです。"
  }
}
```

### Translation Features:
- Automatic language detection for input documents
- Optional output language specification
- Transparent handling of bilingual content

## Technical Design Notes

### System Architecture & Scalability
The system employs a modular, scalable architecture designed for high-performance medical information retrieval. FAISS indices are implemented with distributed computing capabilities. The FastAPI application is containerized and can be load-balanced for increased throughput. Key components like the embedding service and translation module are isolated for independent scaling based on demand.

### Modularity & Future Improvements
The codebase is structured with clear separation of concerns:
- Document Processing: Language detection and text chunking
- Vector Operations: Embedding generation and FAISS indexing
- Retrieval Service: Semantic search and ranking
- Generation Module: Response formatting and translation

Future improvements could include:
- Real-time index updates
- Caching layer for frequent queries
- Multi-region deployment
- Advanced language model integration

## Deployment Guide

### Docker Setup

```bash
# Build the image
docker build -t acme-healthcare-assistant .
```
# Run the image

```bash
docker run -d -p 8000:8000 --name acme-assistant acme-healthcare-assistant
```

### CI/CD Implementation
The repository includes a complete GitHub Actions workflow with Docker Hub integration:

#### Pipeline Stages:

1. **Container Management**
   - Docker image building with multi-stage optimization
   - Semantic version tagging (e.g., v1.0.0, latest)
   - **Docker Hub Registry Push**: Images are automatically pushed to Docker Hub repository

2. **Deployment Process**
   - **Production**: Automated deployment on main branch updates
   - Container pull and run with environment-specific configuration

#### Docker Hub Integration:

The CI/CD pipeline automatically:
1. **Builds** the Docker image with optimized layers
2. **Tags** with version and latest labels
3. **Pushes** to Docker Hub registry: `acmeai/healthcare-assistant:latest`
4. **Pulls** the image in target environments
5. **Runs** containers with proper configuration

#### Production Deployment Commands:
```bash
# Pull latest image from Docker Hub
docker pull bikas0/healthcare-assistant:latest
```

# Run container with production configuration

```bash
docker run -d -p 8000:8000 --name healthcare-assistant bikas0/healthcare-assistant:latest
```


#### CI/CD Workflow:

The streamlined pipeline focuses on efficient Docker image management:

**Workflow Steps:**
1. **Code Push**: Triggers on main or develop branch pushes
2. **Docker Build**: Creates optimized container images
3. **Registry Push**: Automatically pushes to Docker Hub
4. **Environment Deployment**: Pulls and runs containers in target environments

**Branch Strategy:**
- `main` branch → Production deployment (`bikas0/healthcare-assistant:latest`)
