# PII Anonymization API - Setup Guide

## Quick Start

### 1. Create New API Folder
```bash
# From your current workspace
cd ..
mkdir pii-anonymization-api
cd pii-anonymization-api
```

### 2. Install Modified Presidio
```bash
# Install your custom Presidio as editable package
pip install -e ../Presdio/presidio-main/presidio-analyzer

# Verify installation
python -c "from presidio_analyzer.predefined_recognizers import AgeRecognizer; print('✅ Custom Presidio loaded')"
```

### 3. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_lg
```

### 4. Copy Required Files
```bash
# Copy ethnicities.json from Presidio folder
cp ../Presdio/ethnicities.json .
```

### 5. Run the API
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API
Open browser: http://localhost:8000/docs

---

## Project Structure

```
pii-anonymization-api/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
├── README.md                    # API documentation
├── ethnicities.json             # Ethnicity data
│
├── config/
│   └── settings.py              # Configuration management
│
├── core/
│   ├── __init__.py
│   ├── analyzer.py              # Presidio analyzer setup
│   └── models.py                # Pydantic models
│
├── processors/
│   ├── __init__.py
│   ├── base.py                  # Base processor class
│   ├── pdf_processor.py         # PDF processing
│   ├── docx_processor.py        # DOCX processing
│   ├── txt_processor.py         # TXT processing
│   ├── csv_processor.py         # CSV processing
│   ├── excel_processor.py       # XLSX processing
│   ├── json_processor.py        # JSON processing
│   └── web_processor.py         # Web content processing
│
├── routers/
│   ├── __init__.py
│   ├── anonymize.py             # Anonymization endpoints
│   └── health.py                # Health check endpoints
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py          # File upload/download utilities
│   └── validators.py            # Input validation
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    └── test_processors.py
```

---

## API Endpoints

### 1. Health Check
- `GET /health` - API health status
- `GET /health/presidio` - Presidio recognizers status

### 2. Anonymization
- `POST /anonymize/pdf` - Anonymize PDF (preserves formatting)
- `POST /anonymize/docx` - Anonymize DOCX
- `POST /anonymize/txt` - Anonymize text file
- `POST /anonymize/csv` - Anonymize CSV
- `POST /anonymize/excel` - Anonymize Excel
- `POST /anonymize/json` - Anonymize JSON
- `POST /anonymize/web` - Anonymize web content (URL or HTML)
- `POST /anonymize/auto` - Auto-detect format and anonymize

### 3. Analysis (without anonymization)
- `POST /analyze/text` - Analyze text and return detected entities
- `POST /analyze/file` - Analyze file and return detected entities

---

## Environment Variables

Create `.env` file:
```env
# API Configuration
API_TITLE=PII Anonymization API
API_VERSION=1.0.0
API_HOST=0.0.0.0
API_PORT=8000

# File Upload Limits
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=pdf,docx,txt,csv,xlsx,json

# Presidio Configuration
ETHNICITY_JSON_PATH=ethnicities.json
SPACY_MODEL=en_core_web_lg

# Logging
LOG_LEVEL=INFO
```

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install custom Presidio
COPY ../Presdio/presidio-main/presidio-analyzer /tmp/presidio-analyzer
RUN pip install /tmp/presidio-analyzer && rm -rf /tmp/presidio-analyzer

# Copy API code
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run
```bash
docker build -t pii-api .
docker run -p 8000:8000 pii-api
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Test specific endpoint
pytest tests/test_api.py::test_anonymize_pdf
```

---

## Usage Examples

### cURL Examples

**Anonymize PDF:**
```bash
curl -X POST "http://localhost:8000/anonymize/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  --output anonymized.pdf
```

**Anonymize Text:**
```bash
curl -X POST "http://localhost:8000/anonymize/txt" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.txt" \
  --output anonymized.txt
```

**Analyze Text:**
```bash
curl -X POST "http://localhost:8000/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "John Doe, age 30, lives in New York 10001"}' \
  | jq
```

### Python Client Example

```python
import requests

# Anonymize PDF
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/anonymize/pdf',
        files={'file': f}
    )
    
with open('anonymized.pdf', 'wb') as f:
    f.write(response.content)

# Analyze text
response = requests.post(
    'http://localhost:8000/analyze/text',
    json={'text': 'John Doe, age 30, email: john@example.com'}
)
print(response.json())
```

---

## Next Steps

1. Create the new folder: `mkdir pii-anonymization-api`
2. Copy the files I'll create for you
3. Install dependencies
4. Run and test the API
5. Deploy to your environment

Ready to proceed?
