# Encryption and Unmask Implementation

## Overview

Implemented consistent PII anonymization with AES-CBC encryption and a de-anonymization endpoint.

## Key Features

### 1. Consistent Anonymization
- Same PII value always gets same tag (e.g., "Bob" → `<PERSON_0>` every time)
- Entity-specific tags: `<PERSON_0>`, `<EMAIL_0>`, `<US_SSN_0>`, `<LOCATION_0>`, etc.
- Country-specific entities handled automatically (different entity types)

### 2. AES-CBC Encryption
- Each PII value encrypted with AES-256-CBC
- Random IV per value for security
- Output: Base64(IV + Ciphertext)
- Encryption key generated per request (32-character hex string)
- Key stored as plain text in database

### 3. Mapping Format
Stored in database as JSON:
```json
{
  "<PERSON_0>": {
    "encrypted_value": "base64_encoded_iv_ciphertext",
    "entity_type": "PERSON",
    "score": 0.95
  },
  "<EMAIL_0>": {
    "encrypted_value": "base64_encoded_iv_ciphertext",
    "entity_type": "EMAIL_ADDRESS",
    "score": 0.98
  }
}
```

## Implementation Details

### ConsistentAnonymizer Class
Located in `utility/PresidioUtility.py`

**Responsibilities:**
- Track seen PII values (`value_to_tag`)
- Assign consistent indexed tags
- Encrypt PII values using AES-CBC
- Maintain counters per entity type
- Generate mapping with metadata

**Key Methods:**
- `encrypt_value(plaintext)` - Encrypts a single value
- `operator_logic(original_value, entity_type)` - Core anonymization logic
- `get_mapping_with_metadata(entities)` - Returns Presidio-format mapping

### Updated PresidioUtility

**detect_pii(text, language)**
- Calls Presidio analyzer
- Returns list of RecognizerResult
- Decoupled from anonymization

**anonymize_text(text, entities)**
- Generates unique encryption key
- Creates ConsistentAnonymizer instance
- Sets up entity-specific operators
- Returns:
  - `anonymized_text` - Text with tags
  - `mapping` - Encrypted mapping with metadata
  - `encryption_key` - Plain text key
  - `entities_count` - Number of entities

**Helper Functions:**
- `decrypt_value(encrypted_blob, crypto_key)` - Decrypt single value
- `deanonymize_text(anonymized_text, mapping, encryption_key)` - Full de-anonymization

## API Endpoints

### 1. POST /v1/handle-pii (Updated)

**Request:**
```
POST /v1/handle-pii
Content-Type: multipart/form-data

assessment_id: uuid
prospect_id: uuid
caller_name: string
input_type: pdf|docx|txt|csv|xlsx|json|tavily
document: file
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "PDF processed successfully",
  "data": {
    "request_id": "req_abc123...",
    "processed_document": "/tmp/req_abc123_anonymized.pdf",
    "entities_detected": 15,
    "country": "United States",
    "processing_time_ms": 3450
  },
  "timestamp": "2026-02-13T10:30:45.123Z"
}
```

**What's Stored in Database:**
- `request_id` - Unique identifier
- `assessment_id`, `prospect_id` - References
- `input_type`, `caller_name`, `country` - Metadata
- `processed_document` - Path to anonymized file
- `output_text` - Anonymized text with tags
- `anonymizing_mapping` - JSON mapping (encrypted values + metadata)
- `encrypted_key` - Plain text encryption key
- `created_at`, `created_by`, etc. - Audit fields

### 2. POST /v1/unmask-pii (NEW)

**Purpose:** De-anonymize documents by replacing tags with decrypted original values

**Request:**
```
POST /v1/unmask-pii
Content-Type: multipart/form-data

request_id: req_abc123...
input_type: pdf|docx|txt|csv|xlsx|json|tavily
document: file (with tags like <PERSON_0>, <EMAIL_0>)
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "PDF de-anonymized successfully",
  "data": {
    "request_id": "req_abc123...",
    "unmasked_document": "/tmp/req_abc123_unmasked.pdf",
    "tags_replaced": 15,
    "processing_time_ms": 1250
  },
  "timestamp": "2026-02-13T10:35:20.456Z"
}
```

**Process Flow:**
1. Receive request_id and anonymized document
2. Retrieve mapping and encryption_key from database
3. Extract text from document
4. For each tag in mapping:
   - Decrypt the encrypted_value
   - Replace tag with decrypted value
5. Create new document with de-anonymized text
6. Delete received input file
7. Return unmasked document

## UnmaskService

Located in `services/UnmaskService.py`

**Responsibilities:**
- Retrieve PII record from database
- Extract text from anonymized document
- De-anonymize using stored mapping and key
- Create output document
- Clean up temporary files

**Key Methods:**
- `process_document(request_id, document, input_type)` - Main processing
- `_extract_text_by_type(document_bytes, input_type)` - Extract text
- `_create_document_by_type(text, output_path, input_type, original_bytes)` - Create output

**Supported Operations:**
- PDF: Extract text, create new PDF
- DOCX: Extract from paragraphs/tables, create new DOCX
- TXT: Direct read/write
- CSV: Parse with pandas, write back
- XLSX: Extract from cells, create new workbook
- JSON: Parse and format
- Tavily: HTML or plain text

## Security Considerations

### What's Encrypted
✅ Actual PII values (e.g., "Bob", "bob@email.com", "123-45-6789")

### What's NOT Encrypted
- Tags (e.g., `<PERSON_0>`, `<EMAIL_0>`)
- Entity types (e.g., "PERSON", "EMAIL_ADDRESS")
- Confidence scores
- Encryption key (stored as plain text)

### Why This Design
1. **Tags are not sensitive** - They're just placeholders
2. **Mapping structure is not sensitive** - Only shows entity types and positions
3. **Encryption key per request** - Each request has unique key
4. **No PII in logs** - Only tags appear in logs and anonymized documents

## Use Cases

### Use Case 1: LLM Processing
```
1. User uploads document → handle-pii
2. Get anonymized document with tags
3. Send anonymized text to LLM
4. LLM processes and returns response with tags
5. Call unmask-pii with LLM response
6. Get de-anonymized response with original PII
```

### Use Case 2: Secure Storage
```
1. Upload sensitive document → handle-pii
2. Store anonymized version
3. Delete original document
4. When needed, retrieve and unmask
```

### Use Case 3: Data Sharing
```
1. Anonymize document before sharing
2. Share anonymized version (no PII exposed)
3. Recipient can't see original PII
4. Only authorized users can unmask
```

## Database Schema

**pii_details table:**
```sql
request_id          VARCHAR PRIMARY KEY
assessment_id       VARCHAR FK
prospect_id         VARCHAR FK
input_type          VARCHAR(50)
caller_name         VARCHAR(255)
country             VARCHAR(100)
processed_document  TEXT
output_text         TEXT
anonymizing_mapping JSON
encrypted_key       TEXT
created_at          TIMESTAMP
created_by          VARCHAR
modified_at         TIMESTAMP
modified_by         VARCHAR
is_active           BOOLEAN
```

## Testing

### Test handle-pii
```bash
curl -X POST "http://localhost:8000/v1/handle-pii" \
  -F "assessment_id=uuid-here" \
  -F "prospect_id=uuid-here" \
  -F "caller_name=test-service" \
  -F "input_type=txt" \
  -F "document=@sample.txt"
```

### Test unmask-pii
```bash
curl -X POST "http://localhost:8000/v1/unmask-pii" \
  -F "request_id=req_abc123..." \
  -F "input_type=txt" \
  -F "document=@anonymized.txt"
```

## Example Flow

**Input Document (sample.txt):**
```
John Smith works at Acme Corp.
His email is john.smith@acme.com.
Phone: 555-123-4567
SSN: 123-45-6789
```

**After handle-pii (anonymized):**
```
<PERSON_0> works at <ORGANIZATION_0>.
His email is <EMAIL_0>.
Phone: <PHONE_NUMBER_0>
SSN: <US_SSN_0>
```

**Stored Mapping:**
```json
{
  "<PERSON_0>": {
    "encrypted_value": "aGVsbG8gd29ybGQ=...",
    "entity_type": "PERSON",
    "score": 0.95
  },
  "<EMAIL_0>": {
    "encrypted_value": "ZW1haWwgZGF0YQ==...",
    "entity_type": "EMAIL_ADDRESS",
    "score": 0.98
  }
}
```

**After unmask-pii (restored):**
```
John Smith works at Acme Corp.
His email is john.smith@acme.com.
Phone: 555-123-4567
SSN: 123-45-6789
```

## Dependencies Added

```
pycryptodome==3.19.0  # For AES encryption
```

## Files Modified/Created

**Modified:**
- `utility/PresidioUtility.py` - Added ConsistentAnonymizer, encryption
- `services/PDFService.py` - Updated to use new anonymization
- `controllers/PIIController.py` - Added unmask-pii endpoint
- `requirements.txt` - Added pycryptodome

**Created:**
- `services/UnmaskService.py` - De-anonymization service
- `ENCRYPTION_AND_UNMASK_IMPLEMENTATION.md` - This document

## Next Steps

1. Update remaining services (DOCX, TXT, CSV, XLSX, JSON, Tavily) to use new PresidioUtility
2. Test encryption/decryption with various document types
3. Add country-specific PII entity detection
4. Implement proper error handling for unmask endpoint
5. Add authentication/authorization for unmask endpoint
6. Consider adding audit logging for unmask operations
