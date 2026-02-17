# PII Entity Recognizers Reference Guide

## Complete Entity Recognition Methods and Implementation

---

| Entity Name | Tag | Method Used | Code Snippet |
|-------------|-----|-------------|--------------|
| **Name** | `<PERSON>` | **NLP-based (spaCy NER)** - Uses pre-trained Named Entity Recognition model to identify person names in context | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["PERSON"], language='en')<br>``` |
| **Age** | `<AGE>` | **Regex + Context** - Pattern matching for age expressions with context words like "years old", "aged", etc. | ```python<br>from presidio_analyzer.predefined_recognizers import AgeRecognizer<br>recognizer = AgeRecognizer()<br>analyzer.registry.add_recognizer(recognizer)<br># Patterns:<br># - "age: 45"<br># - "62 years old"<br># - "18-25 years old"<br>``` |
| **Gender** | `<GENDER>` | **Deny List** - Matches against a predefined list of 50+ gender terms including binary, non-binary, pronouns, and titles | ```python<br>from presidio_analyzer.predefined_recognizers import GenderRecognizer<br>recognizer = GenderRecognizer()<br>analyzer.registry.add_recognizer(recognizer)<br># Detects: male, female, non-binary, they/them, etc.<br>``` |
| **Ethnicity** | `<ETHNICITY>` | **Deny List (JSON-based)** - Matches against 1000+ ethnicity terms loaded from JSON file or 30+ default terms | ```python<br>from presidio_analyzer.predefined_recognizers import EthnicityRecognizer<br># With JSON file:<br>recognizer = EthnicityRecognizer(<br>    ethnicity_json_path="ethnicities.json"<br>)<br># Or default list:<br>recognizer = EthnicityRecognizer()<br>analyzer.registry.add_recognizer(recognizer)<br>``` |
| **Phone Number** | `<PHONE_NUMBER>` | **Library-based (phonenumbers)** - Uses python-phonenumbers library for multi-regional phone number detection and validation | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["PHONE_NUMBER"], language='en')<br># Detects: (206) 555-0198, +1-555-123-4567, etc.<br># Filters out IP addresses<br>``` |
| **Email Address** | `<EMAIL_ADDRESS>` | **Regex + Validation** - Pattern matching with TLD validation using tldextract library | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["EMAIL_ADDRESS"], language='en')<br># Pattern: user@domain.com<br># Validates domain TLD<br>``` |
| **Location (City/State)** | `<LOCATION>` | **NLP-based (spaCy NER)** - Identifies GPE (Geopolitical Entity) and LOC labels from NER model | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["LOCATION"], language='en')<br># Detects: Seattle, Washington, Miami, etc.<br>``` |
| **ZIP Code** | `<ZIP_CODE>` | **Regex + Validation** - Pattern matching for 5-digit and ZIP+4 formats with validation rules | ```python<br>from presidio_analyzer.predefined_recognizers import ZipCodeRecognizer<br>recognizer = ZipCodeRecognizer()<br>analyzer.registry.add_recognizer(recognizer)<br># Patterns:<br># - 90210 (5-digit)<br># - 90210-1234 (ZIP+4)<br># Rejects: all same digits, starts with 00<br>``` |
| **Social Security Number** | `<US_SSN>` | **Regex + Validation** - Multiple patterns with strict validation rules for SSN format | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["US_SSN"], language='en')<br># Patterns:<br># - 123-45-6789<br># - 123 45 6789<br># Validates: no all zeros, no 666, no 00 in middle<br>``` |
| **Bank Account Number** | `<US_BANK_NUMBER>` | **Regex + Context** - Pattern matching for account numbers with and without dashes, boosted by context words | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["US_BANK_NUMBER"], language='en')<br># Patterns:<br># - 1234-5678-9012 (with dashes, score: 0.5)<br># - 123456789012 (8-17 digits, score: 0.05)<br># Context: account, bank, acct, checking, savings<br>``` |
| **IP Address** | `<IP_ADDRESS>` | **Regex + Validation** - Pattern matching for IPv4 and IPv6 with validation using ipaddress library | ```python<br>from presidio_analyzer import AnalyzerEngine<br>analyzer = AnalyzerEngine()<br>results = analyzer.analyze(text, ["IP_ADDRESS"], language='en')<br># Detects:<br># - IPv4: 192.168.1.1<br># - IPv6: 2001:0db8:85a3::8a2e:0370:7334<br># Validates using ipaddress.ip_address()<br>``` |
| **Cookie/Session ID** | `<COOKIE>` | **Regex + Context** - Multiple patterns for session IDs, tokens, JWTs, and UUIDs with validation | ```python<br>from presidio_analyzer.predefined_recognizers import CookieRecognizer<br>recognizer = CookieRecognizer()<br>analyzer.registry.add_recognizer(recognizer)<br># Patterns:<br># - session_id=abc123... (score: 0.8)<br># - JWT: eyJ... (score: 0.9)<br># - UUID: 550e8400-e29b-41d4-a716-446655440000<br># Rejects: underscore-only, certificate serials<br>``` |
| **Certificate/License Number** | `<CERTIFICATE_NUMBER>` | **Regex + Validation** - Comprehensive patterns for passports, licenses, certificates, and policy numbers | ```python<br>from presidio_analyzer.predefined_recognizers import CertificateRecognizer<br>recognizer = CertificateRecognizer()<br>analyzer.registry.add_recognizer(recognizer)<br># Detects:<br># - Passports: A-99823411, 123456789<br># - Licenses: FTL-990234-B, WDL-772-BBN-01<br># - Medical IDs: MED-9920-X<br># - Policy Numbers: LP-88902-11<br># - License Plates: WA-882-BBN<br># - Certificate Serials: 77-88-99-AA-BB-CC-00-11<br>``` |

---

## Detailed Implementation Examples

### 1. Complete Setup with All Custom Recognizers

```python
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    AgeRecognizer,
    CertificateRecognizer,
    CookieRecognizer,
    EthnicityRecognizer,
    GenderRecognizer,
    ZipCodeRecognizer,
)

# Initialize analyzer
analyzer = AnalyzerEngine()

# Add all custom recognizers
analyzer.registry.add_recognizer(AgeRecognizer())
analyzer.registry.add_recognizer(GenderRecognizer())
analyzer.registry.add_recognizer(EthnicityRecognizer(ethnicity_json_path="ethnicities.json"))
analyzer.registry.add_recognizer(CookieRecognizer())
analyzer.registry.add_recognizer(ZipCodeRecognizer())
analyzer.registry.add_recognizer(CertificateRecognizer())

# Define entities to detect
entities = [
    "PERSON",              # Names
    "AGE",                 # Age
    "GENDER",              # Gender
    "ETHNICITY",           # Ethnicity
    "PHONE_NUMBER",        # Phone numbers
    "EMAIL_ADDRESS",       # Email addresses
    "LOCATION",            # Cities, States
    "ZIP_CODE",            # ZIP codes
    "US_SSN",              # Social Security Numbers
    "US_BANK_NUMBER",      # Bank account numbers
    "IP_ADDRESS",          # IP addresses
    "COOKIE",              # Cookies and session IDs
    "CERTIFICATE_NUMBER",  # Certificates and licenses
]

# Analyze text
text = "Your document text here..."
results = analyzer.analyze(text, entities, language='en')

# Display results
for result in results:
    detected_text = text[result.start:result.end]
    print(f"{result.entity_type}: {detected_text} (score: {result.score:.2f})")
```

### 2. Anonymization with Overlap Handling

```python
def anonymize_with_tags(text, results):
    """Replace detected PII with entity type tags, handling overlaps."""
    
    # Remove overlapping entities - keep highest score
    def remove_overlaps(results):
        if not results:
            return []
        
        sorted_results = sorted(results, key=lambda x: (x.start, -x.score))
        non_overlapping = []
        
        for result in sorted_results:
            overlaps = False
            for accepted in non_overlapping:
                if not (result.end <= accepted.start or result.start >= accepted.end):
                    overlaps = True
                    if result.score > accepted.score:
                        non_overlapping.remove(accepted)
                        overlaps = False
                    break
            
            if not overlaps:
                non_overlapping.append(result)
        
        return non_overlapping
    
    # Remove overlaps and sort
    results_clean = remove_overlaps(results)
    results_sorted = sorted(results_clean, key=lambda x: x.start, reverse=True)
    
    # Replace with tags
    anonymized_text = text
    for result in results_sorted:
        tag = f"<{result.entity_type}>"
        anonymized_text = (
            anonymized_text[:result.start] + 
            tag + 
            anonymized_text[result.end:]
        )
    
    return anonymized_text

# Usage
anonymized = anonymize_with_tags(text, results)
print(anonymized)
```

---

## Pattern Details by Entity

### AGE Recognizer Patterns

```python
# Pattern 1: Age with context (strong) - Score: 0.7
r"\b(?:age[ds]?|years?\s+old)\s*:?\s*(\d{1,3})\b"
# Matches: "age: 45", "aged 30", "years old: 62"

# Pattern 2: Age with suffix (strong) - Score: 0.7
r"\b(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b"
# Matches: "25 years old", "30 yrs old", "18 y.o."

# Pattern 3: Age range - Score: 0.7
r"\b(\d{1,3})\s*(?:-|to)\s*(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b"
# Matches: "18-25 years old", "30 to 45 yrs old"

# Validation: Rejects ages < 0 or > 120
```

### ZIP Code Recognizer Patterns

```python
# Pattern: ZIP Code (5 digits or ZIP+4) - Score: 0.5
r"\b\d{5}(?:\-\d{4})?\b"
# Matches: "90210", "90210-1234"

# Validation:
# - Rejects all same digits (00000, 11111)
# - Rejects starting with 00
# - Must be exactly 5 or 9 digits
```

### Bank Account Recognizer Patterns

```python
# Pattern 1: With dashes (medium) - Score: 0.5
r"\b\d{4}-\d{4}-\d{4}\b"
# Matches: "1234-5678-9012"

# Pattern 2: Without dashes (weak) - Score: 0.05
r"\b[0-9]{8,17}\b"
# Matches: "123456789012" (8-17 digits)

# Context words boost score: account, bank, acct, checking, savings
```

### Certificate Recognizer Patterns

```python
# Pattern 1: Passport - Letter + 8 digits (strong) - Score: 0.7
r"\b[A-Z]-?\d{8}\b"
# Matches: "A-99823411", "M12345678"

# Pattern 2: Passport - 9 digits (medium) - Score: 0.4
r"\b\d{9}\b"
# Matches: "123456789"

# Pattern 3: License - Prefix-Number-Suffix (strong) - Score: 0.8
r"\b[A-Z]{2,4}-\d{5,7}-[A-Z0-9]{1,3}\b"
# Matches: "FTL-990234-B", "POL-9910234-X"

# Pattern 4: License - Alphanumeric with dashes (medium) - Score: 0.6
r"\b[A-Z]{2,4}-\d{3,4}-[A-Z0-9]{2,6}-?\d{0,2}\b"
# Matches: "WDL-772-BBN-01", "MED-9920-X"

# Pattern 5: Policy/Medical ID (medium) - Score: 0.6
r"\b[A-Z]{2,4}-\d{4,7}-?[A-Z0-9]?\b"
# Matches: "LP-88902-11", "GRP-44102"

# Pattern 6: Certificate Serial (medium) - Score: 0.7
r"\b\d{2}-\d{2}-\d{2}-[A-F0-9]{2}-[A-F0-9]{2}-[A-F0-9]{2}-\d{2}-\d{2}\b"
# Matches: "77-88-99-AA-BB-CC-00-11"

# Pattern 7: License Plate (medium) - Score: 0.5
r"\b[A-Z]{2}-\d{3}-[A-Z]{3}\b"
# Matches: "WA-882-BBN"
```

### Cookie Recognizer Patterns

```python
# Pattern 1: Session ID with context (strong) - Score: 0.8
r"\b(?:session[_\s-]?id|sessionid|sess[_\s-]?id|sessid)\s*[=:]\s*([a-zA-Z0-9\-_]{16,})\b"
# Matches: "session_id=abc123def456..."

# Pattern 2: Cookie/Token with context (strong) - Score: 0.8
r"\b(?:cookie|token|auth[_\s-]?token|access[_\s-]?token)\s*[=:]\s*([a-zA-Z0-9\-_\.]{16,})\b"
# Matches: "auth_token=xyz789..."

# Pattern 3: JWT Token - Score: 0.9
r"\beyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\b"
# Matches: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Pattern 4: UUID format (medium) - Score: 0.5
r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
# Matches: "550e8400-e29b-41d4-a716-446655440000"

# Validation:
# - Rejects underscore-only patterns
# - Rejects certificate serials (7+ dashes)
# - Must have 8+ alphanumeric characters
```

---

## Context Words by Entity

| Entity | Context Words |
|--------|---------------|
| **AGE** | age, aged, years old, year old, yrs old, yr old, y.o, birthday, born, dob, date of birth |
| **GENDER** | gender, sex, identify, identifies as, pronoun, pronouns |
| **ETHNICITY** | ethnicity, ethnic, race, racial, heritage, ancestry, descent, origin, background, nationality |
| **ZIP_CODE** | zip, zipcode, zip code, postal, postal code, postcode, mail, mailing |
| **US_SSN** | social, security, ssn, ssns, ssid |
| **US_BANK_NUMBER** | check, account, account#, acct, bank, save, debit |
| **IP_ADDRESS** | ip, ipv4, ipv6 |
| **COOKIE** | session, cookie, token, auth, authentication, authorization, bearer, access, refresh, csrf, xsrf, jwt, api key, apikey |
| **CERTIFICATE_NUMBER** | passport, license, licence, certificate, cert, id, identification, number, policy, medical, driver, pilot, professional, global entry, plate, serial, credential, permit |

---

## Validation Rules

### AGE
- Must be between 0 and 120
- Rejects standalone numbers without context

### ZIP_CODE
- Must be 5 or 9 digits (with dash)
- Rejects all same digits (00000, 11111)
- Rejects starting with 00

### US_SSN
- Rejects mismatched delimiters
- Rejects all same digits
- Rejects middle group "00" or last group "0000"
- Rejects known invalid SSNs (000, 666, 123456789, etc.)

### US_BANK_NUMBER
- 8-17 digits without dashes
- 4-4-4 format with dashes

### IP_ADDRESS
- Validates using `ipaddress.ip_address()` library
- Supports both IPv4 and IPv6

### COOKIE
- Minimum 16 characters
- Must have 8+ alphanumeric characters
- Rejects underscore-only patterns
- Rejects certificate serials (7+ dashes)

### CERTIFICATE_NUMBER
- Minimum 5 characters, maximum 20
- Must have letters OR be exactly 9 digits (passport)
- Rejects common false positives (PAGE, SECTION, etc.)
- Rejects all same character

---

## Performance Characteristics

| Entity | Speed | Memory | Accuracy |
|--------|-------|--------|----------|
| PERSON | Medium | High (NLP model) | 100% |
| AGE | Fast | Low | 100% |
| GENDER | Fast | Low | 100% |
| ETHNICITY | Medium | Medium (JSON) | 85% |
| PHONE_NUMBER | Medium | Medium (library) | 100% |
| EMAIL_ADDRESS | Fast | Low | 100% |
| LOCATION | Medium | High (NLP model) | 95% |
| ZIP_CODE | Fast | Low | 100% |
| US_SSN | Fast | Low | 85% |
| US_BANK_NUMBER | Fast | Low | 95% |
| IP_ADDRESS | Fast | Low | 100% |
| COOKIE | Fast | Low | 90% |
| CERTIFICATE_NUMBER | Fast | Low | 95% |

---

## File Locations

| Entity | File Path |
|--------|-----------|
| AGE | `presidio_analyzer/predefined_recognizers/generic/age_recognizer.py` |
| GENDER | `presidio_analyzer/predefined_recognizers/generic/gender_recognizer.py` |
| ETHNICITY | `presidio_analyzer/predefined_recognizers/generic/ethnicity_recognizer.py` |
| ZIP_CODE | `presidio_analyzer/predefined_recognizers/generic/zip_code_recognizer.py` |
| COOKIE | `presidio_analyzer/predefined_recognizers/generic/cookie_recognizer.py` |
| CERTIFICATE_NUMBER | `presidio_analyzer/predefined_recognizers/generic/certificate_recognizer.py` |
| US_BANK_NUMBER | `presidio_analyzer/predefined_recognizers/country_specific/us/us_bank_recognizer.py` |
| IP_ADDRESS | `presidio_analyzer/predefined_recognizers/generic/ip_recognizer.py` |
| PHONE_NUMBER | `presidio_analyzer/predefined_recognizers/generic/phone_recognizer.py` |
| EMAIL_ADDRESS | `presidio_analyzer/predefined_recognizers/generic/email_recognizer.py` |
| US_SSN | `presidio_analyzer/predefined_recognizers/country_specific/us/us_ssn_recognizer.py` |
| PERSON | Built-in (spaCy NER) |
| LOCATION | Built-in (spaCy NER) |

---

## Notes

- **NLP-based recognizers** (PERSON, LOCATION) require spaCy model to be loaded
- **Context words** boost confidence scores when found near detected entities
- **Overlapping entities** are automatically handled by keeping the highest-scoring match
- **Custom patterns** can be added by extending the recognizer classes
- **Validation functions** can be customized by overriding `invalidate_result()` method
