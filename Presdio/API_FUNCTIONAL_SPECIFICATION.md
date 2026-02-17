# PII Anonymization API - Functional Specification

## API Purpose
A RESTful API service that detects and anonymizes Personally Identifiable Information (PII) in various document formats while preserving the original document structure and formatting.

---

## Core Functionality

### 1. Document Anonymization
**Purpose:** Accept a document in any supported format, detect all PII entities, replace them with entity type tags, and return the anonymized document in the same format.

**Input:** Document file (PDF, DOCX, TXT, CSV, XLSX, JSON) or web content
**Output:** Anonymized document in the same format with PII replaced by tags like `<PERSON>`, `<EMAIL_ADDRESS>`, etc.
**Behavior:** 
- Preserves original formatting (fonts, tables, layout, images)
- Replaces only the detected PII text
- Maintains document structure
- Handles overlapping entity detections (keeps highest confidence)

---

### 2. PII Analysis (Detection Only)
**Purpose:** Analyze a document or text to identify and report all PII entities without modifying the content.

**Input:** Document file or plain text
**Output:** JSON report containing:
- List of detected entities with type, location, confidence score
- Original text snippet for each detection
- Summary statistics (count by entity type)
**Behavior:**
- Read-only operation
- No document modification
- Useful for auditing and validation

---

### 3. Format-Specific Processing

#### 3.1 PDF Processing
**Functionality:** 
- Extract text while tracking position information
- Detect PII in extracted text
- Redact PII directly in the PDF structure
- Preserve tables, images, fonts, colors, page layout
**Output:** Anonymized PDF with original formatting intact

#### 3.2 DOCX Processing
**Functionality:**
- Parse Word document structure (paragraphs, tables, headers, footers)
- Detect PII in all text elements
- Replace PII while maintaining styles, formatting, structure
**Output:** Anonymized DOCX with original formatting

#### 3.3 TXT Processing
**Functionality:**
- Read plain text content
- Detect PII
- Replace with tags
**Output:** Anonymized text file

#### 3.4 CSV Processing
**Functionality:**
- Parse CSV structure (columns, rows)
- Detect PII in each cell
- Replace PII while maintaining CSV structure
- Preserve column headers and data types
**Output:** Anonymized CSV with same structure

#### 3.5 Excel (XLSX) Processing
**Functionality:**
- Parse Excel workbook (multiple sheets, cells, formulas)
- Detect PII in cell values
- Replace PII while preserving formulas, formatting, sheets
**Output:** Anonymized Excel file with original structure

#### 3.6 JSON Processing
**Functionality:**
- Parse JSON structure (nested objects, arrays)
- Detect PII in string values
- Replace PII while maintaining JSON structure
- Preserve data types and nesting
**Output:** Anonymized JSON with same structure

#### 3.7 Web Content Processing
**Functionality:**
- Accept URL or HTML content
- Extract text from HTML (handle Tavily web scraper output)
- Detect PII in extracted content
- Return anonymized text or HTML
**Output:** Anonymized web content

---

## PII Entity Detection

### Detected Entity Types (14 total):

1. **PERSON** - Names of individuals
2. **AGE** - Age mentions (e.g., "25 years old", "age: 30")
3. **GENDER** - Gender identifiers (male, female, non-binary, pronouns)
4. **ETHNICITY** - Ethnicity and race mentions
5. **PHONE_NUMBER** - Phone numbers (all formats)
6. **EMAIL_ADDRESS** - Email addresses
7. **LOCATION** - Cities, states, addresses
8. **ZIP_CODE** - US ZIP codes (5-digit and ZIP+4)
9. **US_SSN** - Social Security Numbers
10. **US_BANK_NUMBER** - Bank account numbers
11. **IP_ADDRESS** - IPv4 and IPv6 addresses
12. **COOKIE** - Session IDs, tokens, cookies
13. **CERTIFICATE_NUMBER** - Passports, licenses, certificates

### Detection Features:
- **Context-aware:** Uses surrounding words to improve accuracy
- **Validation:** Applies format validation to reduce false positives
- **Confidence scoring:** Each detection has a confidence score (0.0-1.0)
- **Overlap handling:** When multiple entities detected at same position, keeps highest confidence
- **False positive filtering:** Removes common false positives (e.g., Q1-Q4 as locations)

---

## Processing Behavior

### Overlap Resolution
When multiple recognizers detect the same text span:
- Compare confidence scores
- Keep entity with highest score
- Discard lower-scoring overlapping entities
- Example: "Washington" detected as both PERSON (0.60) and LOCATION (0.85) → Keep LOCATION

### False Positive Filtering
- **AGE:** Reject standalone numbers (page numbers)
- **COOKIE:** Reject URL paths, common words, underscore-only patterns
- **LOCATION:** Reject Q1, Q2, Q3, Q4 (quarter references)
- **PHONE_NUMBER:** Reject IP addresses
- **CERTIFICATE_NUMBER:** Reject common words (PAGE, SECTION, etc.)

### Format Preservation
- **PDF:** Use redaction annotations to replace text in place
- **DOCX:** Modify text runs while preserving styles
- **CSV/Excel:** Replace cell values while maintaining structure
- **JSON:** Replace string values while maintaining object structure

# Leave the security considerations untill we build and test the API
## Security Considerations

### Data Privacy
- Files are processed in memory when possible
- Temporary files deleted immediately after processing
- No logging of file contents or detected PII
- No data retention

### Input Validation
- File size limits enforced
- File type validation (magic bytes, not just extension)
- Malicious content detection
- Rate limiting per client

### Output Safety
- Sanitized error messages (no internal paths)
- No sensitive information in responses
- CORS configuration for web clients

---

## Use Cases

### 1. Document Redaction
**Scenario:** Legal team needs to redact PII from court documents before public release
**Flow:** Upload PDF → API detects names, addresses, SSNs → Returns redacted PDF

### 2. Data Compliance
**Scenario:** Company needs to anonymize customer data exports for GDPR compliance
**Flow:** Upload CSV with customer data → API anonymizes PII → Returns compliant CSV

### 3. Content Moderation
**Scenario:** Platform needs to detect PII in user-submitted content
**Flow:** Submit text via /analyze/text → Receive list of detected PII → Take action

### 4. Data Sharing
**Scenario:** Research team needs to share documents with external partners
**Flow:** Upload DOCX reports → API anonymizes sensitive info → Share anonymized version

### 5. Web Scraping
**Scenario:** Scrape web content and remove PII before storage
**Flow:** Submit Tavily scraped content → API anonymizes → Store clean data

---

## Success Criteria

### Accuracy
- **Precision:** > 90% (detected entities are actually PII)
- **Recall:** > 85% (most PII is detected)
- **False positive rate:** < 10%

### Performance
- **Response time:** < 5 seconds for typical documents
- **Throughput:** > 100 requests/minute
- **Availability:** > 99.5% uptime

### Format Preservation
- **PDF:** Tables, images, fonts preserved
- **DOCX:** Styles, formatting, structure preserved
- **Excel:** Formulas, sheets, formatting preserved
- **CSV/JSON:** Structure and data types preserved

---

## Future Enhancements (Not in Current Scope)

- Batch processing (multiple files in one request)
- Custom entity types (user-defined patterns)
- Multiple language support (currently English only)
- Reversible anonymization (pseudonymization with key)
- Audit logging (track what was anonymized)
- Webhook notifications (async processing)
- File format conversion (e.g., PDF to DOCX)

---

**Summary:** This API provides a comprehensive, format-aware PII detection and anonymization service that preserves document structure while protecting sensitive information across multiple file formats.
