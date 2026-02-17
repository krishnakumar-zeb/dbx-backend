# Presidio Existing Recognizers Analysis

## Overview
This document analyzes how Presidio's existing recognizers work for the entities required in our POC.

---

## 1. PERSON (Name Detection)
**Entity Type:** `PERSON`  
**Recognizer:** `SpacyRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/nlp_engine_recognizers/spacy_recognizer.py`

### Detection Method:
- **NLP-Based (Named Entity Recognition)**
- Uses spaCy's pre-trained NER models
- Extracts entities labeled as "PERSON" or "PER" from NLP artifacts
- Default confidence score: 0.85

### How it Works:
1. Text is processed by spaCy NLP engine
2. SpacyRecognizer extracts entities from NLP artifacts
3. Returns entities with label "PERSON"
4. No regex patterns - fully relies on ML model

### Strengths:
- Context-aware
- Handles various name formats
- Works with different languages (if model supports)

### Limitations:
- Requires NLP model to be loaded
- Performance depends on model quality
- May miss uncommon names

---

## 2. PHONE_NUMBER
**Entity Type:** `PHONE_NUMBER`  
**Recognizer:** `PhoneRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/generic/phone_recognizer.py`

### Detection Method:
- **Library-Based (python-phonenumbers)**
- Uses phonenumbers library for validation
- Supports multiple regions

### How it Works:
1. Iterates through supported regions (US, UK, DE, FE, IL, IN, CA, BR by default)
2. Uses `PhoneNumberMatcher` to find phone numbers
3. Validates and parses each match
4. Returns results with region information

### Configuration:
- **Score:** 0.4
- **Context words:** phone, number, telephone, cell, cellphone, mobile, call
- **Leniency:** 1 (0-3 scale, where 0 is lenient, 3 is strict)

### Strengths:
- Multi-regional support
- Robust validation
- Handles various formats

---

## 3. US_SSN (Social Security Number)
**Entity Type:** `US_SSN`  
**Recognizer:** `UsSsnRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/country_specific/us/us_ssn_recognizer.py`

### Detection Method:
- **Regex Pattern Matching + Validation**

### Patterns:
1. `[0-9]{5}-[0-9]{4}` - Score: 0.05 (very weak)
2. `[0-9]{3}-[0-9]{6}` - Score: 0.05 (very weak)
3. `[0-9]{3}-[0-9]{2}-[0-9]{4}` - Score: 0.05 (very weak)
4. `[0-9]{9}` - Score: 0.05 (very weak)
5. `[0-9]{3}[- .][0-9]{2}[- .][0-9]{4}` - Score: 0.5 (medium)

### Context Words:
social, security, ssn, ssns, ssid

### Validation Logic:
- Checks delimiter consistency
- Rejects all same digits
- Rejects groups with all zeros
- Rejects known invalid SSNs (000, 666, 123456789, etc.)

### Strengths:
- Multiple pattern support
- Strong validation rules
- Context-aware scoring

---

## 4. US_BANK_NUMBER
**Entity Type:** `US_BANK_NUMBER`  
**Recognizer:** `UsBankRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/country_specific/us/us_bank_recognizer.py`

### Detection Method:
- **Regex Pattern Matching**

### Patterns:
- `[0-9]{8,17}` - Score: 0.05 (weak)

### Context Words:
check, account, account#, acct, bank, save, debit

### Strengths:
- Simple pattern
- Context-aware

### Limitations:
- Very weak pattern (any 8-17 digit number)
- Relies heavily on context for accuracy

---

## 5. LOCATION
**Entity Type:** `LOCATION`  
**Recognizer:** `SpacyRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/nlp_engine_recognizers/spacy_recognizer.py`

### Detection Method:
- **NLP-Based (Named Entity Recognition)**
- Uses spaCy's NER to identify GPE (Geopolitical Entity) and LOC labels
- Default confidence score: 0.85

### How it Works:
- Same as PERSON entity
- Extracts entities labeled as "LOCATION", "GPE", or "LOC"
- Context-aware through NLP understanding

### Note:
- This covers general locations but doesn't distinguish between City, State, Zip Code
- For specific location types, custom recognizers will be needed

---

## 6. EMAIL_ADDRESS
**Entity Type:** `EMAIL_ADDRESS`  
**Recognizer:** `EmailRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/generic/email_recognizer.py`

### Detection Method:
- **Regex Pattern Matching + Validation**

### Pattern:
```regex
\b((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b
```
- Score: 0.5 (medium)

### Context Words:
email

### Validation:
- Uses `tldextract` library to validate domain
- Checks if FQDN (Fully Qualified Domain Name) is valid

### Strengths:
- Comprehensive regex
- Domain validation
- Handles various email formats

---

## 7. IP_ADDRESS
**Entity Type:** `IP_ADDRESS`  
**Recognizer:** `IpRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/generic/ip_recognizer.py`

### Detection Method:
- **Regex Pattern Matching + Validation**

### Patterns:
1. **IPv4:** 
   - Regex: `\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b`
   - Score: 0.6

2. **IPv6:**
   - Complex regex covering all IPv6 formats
   - Score: 0.6

3. **IPv6 shorthand:**
   - Pattern: `::`
   - Score: 0.1

### Context Words:
ip, ipv4, ipv6

### Validation:
- Uses Python's `ipaddress` library to validate
- Calls `ipaddress.ip_address()` to ensure valid IP

### Strengths:
- **Already supports both IPv4 and IPv6!**
- Strong validation
- Context-aware

### Note:
**The IP recognizer already supports IPv6**, so we may not need to replace it. We should test it first.

---

## 8. MEDICAL_LICENSE (Certificate Numbers)
**Entity Type:** `MEDICAL_LICENSE`  
**Recognizer:** `MedicalLicenseRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/country_specific/us/medical_license_recognizer.py`

### Detection Method:
- **Regex Pattern Matching**

### Pattern:
- USA DEA Certificate Number: `[abcdefghjklmprstuxABCDEFGHJKLMPRSTUX]{1}[a-zA-Z]{1}\d{7}|[abcdefghjklmprstuxABCDEFGHJKLMPRSTUX]{1}9\d{7}`
- Score: 0.3 (weak)

### Context Words:
medical, certificate, DEA

### Note:
- This is specific to DEA certificates
- May need extension for other certificate types

---

## 9. US_DRIVER_LICENSE
**Entity Type:** `US_DRIVER_LICENSE`  
**Recognizer:** `UsLicenseRecognizer`  
**Location:** `presidio_analyzer/predefined_recognizers/country_specific/us/us_driver_license_recognizer.py`

### Detection Method:
- **Regex Pattern Matching**

### Patterns:
1. Alphanumeric (various state formats) - Score: 0.3 (weak)
2. Digits only (6-14 or 16 digits) - Score: 0.01 (very weak)

### Context Words:
driver, license, permit, lic, dl, id

### Note:
- Covers US driver licenses
- Can be used as reference for other license types

---

## Summary Table

| Entity | Presidio Support | Detection Method | Confidence | Notes |
|--------|-----------------|------------------|------------|-------|
| Name | ✅ PERSON | NLP (spaCy NER) | 0.85 | Context-aware |
| Phone Number | ✅ PHONE_NUMBER | Library (phonenumbers) | 0.4 | Multi-regional |
| Government IDs | ✅ US_SSN | Regex + Validation | 0.05-0.5 | Multiple patterns |
| Account Numbers | ✅ US_BANK_NUMBER | Regex + Context | 0.05 | Weak pattern |
| Age | ❌ | - | - | Need custom |
| Gender | ❌ | - | - | Need custom |
| Ethnicity | ❌ | - | - | Need custom |
| City | ⚠️ LOCATION | NLP (spaCy NER) | 0.85 | Generic location |
| State | ⚠️ LOCATION | NLP (spaCy NER) | 0.85 | Generic location |
| Zip/Postal Code | ❌ | - | - | Need custom |
| Email Address | ✅ EMAIL_ADDRESS | Regex + Validation | 0.5 | Domain validated |
| IP Address | ✅ IP_ADDRESS | Regex + Validation | 0.6 | **IPv4 & IPv6 supported** |
| Cookies | ❌ | - | - | Need custom |
| Certificate/License | ⚠️ MEDICAL_LICENSE | Regex | 0.3 | DEA only, need extension |

---

## Key Findings

### Detection Methods Used:
1. **NLP-Based (spaCy NER):** PERSON, LOCATION
2. **Library-Based:** PHONE_NUMBER (phonenumbers)
3. **Regex + Validation:** IP_ADDRESS, EMAIL_ADDRESS, US_SSN
4. **Regex + Context:** US_BANK_NUMBER, MEDICAL_LICENSE, US_DRIVER_LICENSE

### Pattern for Custom Recognizers:
All custom recognizers extend either:
- `PatternRecognizer` (for regex-based)
- `LocalRecognizer` (for custom logic)

### Next Steps:
1. ✅ Test existing IP_ADDRESS recognizer with IPv6 samples
2. Create ZIP_CODE recognizer (regex-based)
3. Create custom recognizers for: Age, Gender, Ethnicity, Cookies
4. Extend LOCATION to distinguish City/State/Zip
5. Extend certificate recognizer for non-DEA certificates
