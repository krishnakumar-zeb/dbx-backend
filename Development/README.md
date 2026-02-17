# PII Anonymization API

API for detecting and anonymizing Personally Identifiable Information (PII) in various document formats.

## Features

- Supports multiple document formats: PDF, DOCX, TXT, CSV, XLSX, JSON, Tavily
- Detects 14 PII entity types using custom Presidio installation
- Asynchronous processing with connection pooling
- Secure: No PII data stored, only anonymization mappings
- RESTful API with comprehensive error handling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the application:
```bash
python main.py
```

## API Endpoint

### POST /v1/handle-pii

Process document for PII anonymization.

**Parameters:**
- `assessment_id` (string, required): UUID of the assessment
- `caller_name` (string, required): Name of the calling service
- `input_type` (string, required): Document type (pdf, docx, txt, csv, xlsx, json, tavily)
- `document` (file, required): Document file to process

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "PDF processed successfully",
  "data": {
    "request_id": "req_xxx",
    "processed_document": "/output/anonymized.pdf",
    "entities_detected": 15,
    "processing_time_ms": 3450
  },
  "timestamp": "2026-02-10T14:30:45.123Z"
}
```

## Architecture

- **Main**: FastAPI application entry point
- **Controller**: Request handling and routing
- **Services**: Document-specific processing (7 services)
- **Utility**: Presidio integration, database, exceptions
- **Repository**: Database operations

## Database

Uses Databricks Postgres with connection pooling:
- Pool size: 10 base connections
- Max overflow: 20 additional connections
- Total max: 30 concurrent connections

## Security

- Original files deleted after processing
- Only anonymization mappings stored (no actual PII)
- Encrypted data storage support
- Secure connection pooling
