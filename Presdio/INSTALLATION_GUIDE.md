# Installation Guide for Modified Presidio

## Overview
This guide explains how to install and use the modified Presidio analyzer with custom recognizers in your FastAPI application.

---

## Method 1: Editable Install (Recommended for Development)

### Prerequisites
- Python 3.8+
- pip

### Steps

1. **Install the modified Presidio as editable package:**
```bash
cd presidio-main/presidio-analyzer
pip install -e .
```

2. **Verify installation:**
```bash
python -c "from presidio_analyzer.predefined_recognizers import AgeRecognizer, GenderRecognizer; print('Success!')"
```

3. **In your FastAPI project, use it directly:**
```python
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    AgeRecognizer,
    GenderRecognizer,
    EthnicityRecognizer,
    CookieRecognizer,
    ZipCodeRecognizer,
    CertificateRecognizer,
)
```

---

## Method 2: Build and Install Wheel Package

### Steps

1. **Build the package:**
```bash
cd presidio-main/presidio-analyzer

# Install build tools
pip install build

# Build
python -m build
```

2. **Install the wheel:**
```bash
pip install dist/presidio_analyzer-*.whl
```

3. **Share the wheel file:**
- The `.whl` file in `dist/` can be shared with team members
- They can install it with: `pip install presidio_analyzer-*.whl`

---

## Method 3: Install from Git Repository

### Steps

1. **Push your modified Presidio to Git:**
```bash
cd presidio-main
git init
git add .
git commit -m "Custom Presidio with additional recognizers"
git remote add origin https://github.com/yourcompany/presidio-custom.git
git push -u origin main
```

2. **Install from Git URL:**
```bash
pip install git+https://github.com/yourcompany/presidio-custom.git#subdirectory=presidio-analyzer
```

3. **Add to requirements.txt:**
```txt
git+https://github.com/yourcompany/presidio-custom.git#subdirectory=presidio-analyzer
```

---

## Method 4: Docker Deployment

### Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy and install modified Presidio
COPY presidio-main/presidio-analyzer /tmp/presidio-analyzer
RUN pip install /tmp/presidio-analyzer && \
    rm -rf /tmp/presidio-analyzer

# Copy FastAPI app
COPY api/ /app/
COPY ethnicities.json /app/

# Install dependencies
RUN pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and run:
```bash
docker build -t pii-anonymization-api .
docker run -p 8000:8000 pii-anonymization-api
```

---

## Custom Recognizers Included

Your modified Presidio includes these custom recognizers:

1. **AgeRecognizer** - Detects age mentions
2. **GenderRecognizer** - Detects gender terms
3. **EthnicityRecognizer** - Detects ethnicity mentions
4. **CookieRecognizer** - Detects cookies and session tokens
5. **ZipCodeRecognizer** - Detects US ZIP codes
6. **CertificateRecognizer** - Detects certificates, licenses, passports

### Modified Recognizers:
- **IpRecognizer** - Fixed IPv4 detection bug
- **UsBankRecognizer** - Added dash-separated account pattern
- **PhoneRecognizer** - Added IP address filter

---

## Required Files

Make sure these files are accessible to your application:

1. **Custom Recognizers:**
   - `presidio_analyzer/predefined_recognizers/generic/age_recognizer.py`
   - `presidio_analyzer/predefined_recognizers/generic/gender_recognizer.py`
   - `presidio_analyzer/predefined_recognizers/generic/ethnicity_recognizer.py`
   - `presidio_analyzer/predefined_recognizers/generic/cookie_recognizer.py`
   - `presidio_analyzer/predefined_recognizers/generic/zip_code_recognizer.py`
   - `presidio_analyzer/predefined_recognizers/generic/certificate_recognizer.py`

2. **Data Files:**
   - `ethnicities.json` (must be in same directory as your app or provide path)

---

## Testing Installation

Create a test script `test_installation.py`:

```python
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    AgeRecognizer,
    GenderRecognizer,
    EthnicityRecognizer,
    CookieRecognizer,
    ZipCodeRecognizer,
    CertificateRecognizer,
)

# Initialize analyzer
analyzer = AnalyzerEngine()

# Add custom recognizers
analyzer.registry.add_recognizer(AgeRecognizer())
analyzer.registry.add_recognizer(GenderRecognizer())
analyzer.registry.add_recognizer(EthnicityRecognizer())
analyzer.registry.add_recognizer(CookieRecognizer())
analyzer.registry.add_recognizer(ZipCodeRecognizer())
analyzer.registry.add_recognizer(CertificateRecognizer())

# Test
text = "John is 25 years old, male, lives in New York 10001"
results = analyzer.analyze(text=text, language='en')

print(f"Found {len(results)} entities:")
for result in results:
    print(f"  - {result.entity_type}: {text[result.start:result.end]}")
```

Run:
```bash
python test_installation.py
```

Expected output:
```
Found 5 entities:
  - PERSON: John
  - AGE: 25 years old
  - GENDER: male
  - LOCATION: New York
  - ZIP_CODE: 10001
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'presidio_analyzer'"
**Solution:** Install the package first:
```bash
cd presidio-main/presidio-analyzer
pip install -e .
```

### Issue: "No module named 'spacy'"
**Solution:** Install spaCy and download model:
```bash
pip install spacy
python -m spacy download en_core_web_lg
```

### Issue: Custom recognizers not found
**Solution:** Make sure `__init__.py` is updated to export them:
```python
# In presidio_analyzer/predefined_recognizers/__init__.py
from .generic.age_recognizer import AgeRecognizer
from .generic.gender_recognizer import GenderRecognizer
# ... etc
```

---

## Next Steps

Once installed, you can:
1. Create your FastAPI endpoints
2. Process different file formats (PDF, DOCX, CSV, etc.)
3. Deploy to production

See the main documentation for API implementation examples.
