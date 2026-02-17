# PII Anonymization API - Integration Summary

## Completed Changes

### 1. Database Integration ✅
- **Updated to Databricks Postgres Lakebase**
  - OAuth token authentication
  - Connection pooling (pool_size=10, max_overflow=20)
  - Schema search path configuration
  - Token refresh functionality

### 2. Data Model Updates ✅
- **Added ProspectDetailsRecord** to ORM
- **Updated PIIDetailsRecord** with:
  - `prospect_id` field (FK to prospect_details)
  - `country` field (stores detected country)
  - `encrypted_key` field (for future AES-CBC encryption)

### 3. Pydantic Models ✅
- **Created `utility/models.py`** with:
  - `TavilySearchRequest` - Validates Tavily API requests
  - `TavilySearchResponse` - Validates Tavily API responses
  - `CountryDetectionResult` - Validates country detection results
  - `PIIRequest`, `PIIResponse`, `ErrorResponse` - API models
  - `AnonymizedResult`, `PIIEntity` - Presidio models

### 4. Tavily Country Search ✅
- **Created `utility/TavilyCountrySearch.py`**
  - Detects prospect country using Tavily API
  - Supports 14 countries:
    - Canada, Mexico, United States, United Kingdom
    - Germany, France, UAE, Saudi Arabia
    - South Africa, Japan, India, Australia
    - Singapore, Malaysia
  - **Relies only on Tavily's answer field** (no text parsing)
  - Returns confidence level (high, medium, low, none)
  - Handles special cases (USA, UK, UAE abbreviations)
  - Comprehensive error handling with fallback to US

### 5. API Integration ✅
- **Updated PIIController**:
  - Added `prospect_id` as required parameter
  - Integrated Tavily country detection
  - Fetches prospect details from database
  - Defaults to "United States" if country not detected
  - Passes detected country to services

- **Updated Repository**:
  - Added `get_prospect_by_assessment()` method
  - Updated `save_pii_details()` to include prospect_id and country

- **Updated Services** (example: PDFService):
  - Added `country` parameter to `process_document()`
  - Saves country to database

### 6. Testing ✅
- **Created `test_tavily_country_search.py`**
  - Tests country detection for multiple companies
  - Displays confidence levels and sources
  - Verifies supported country matching

## API Flow

```
1. Client sends request with:
   - assessment_id
   - prospect_id
   - caller_name
   - input_type
   - document

2. Controller validates input

3. Controller fetches prospect details from database

4. Controller calls Tavily to detect country:
   - Searches for prospect name
   - Gets country from Tavily answer
   - Matches against supported countries list
   - Defaults to "United States" if not found

5. Controller routes to appropriate service with country

6. Service processes document:
   - Extracts text
   - Detects PII (will use country-specific rules)
   - Anonymizes content
   - Creates output document
   - Saves to database with country

7. Controller returns response with:
   - request_id
   - processed_document
   - entities_detected
   - country
   - processing_time_ms
```

## Environment Variables

Required in `.env` file:

```bash
# Databricks Lakebase
LAKEBASE_USERNAME=your_client_id
LAKEBASE_PASSWORD=your_client_secret
LAKEBASE_HOST=your_lakebase_host
LAKEBASE_PORT=5432
DATABRICKS_SERVER_HOSTNAME=your_databricks_host
LAKEBASE_SCHEMA=default

# Tavily API
TAVILY_API_KEY=your_tavily_api_key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

## Next Steps

### 1. Country-Specific PII Detection 🔄
- Implement country-specific PII entity types
- Apply US entities as baseline for all countries
- Add country-specific entities on top of US entities

### 2. Indexed Contextual Mapping 🔄
- Implement smart tagging (person1, person2, location1, etc.)
- Track entity instances to avoid duplicate tags
- Map same entity to same tag across document

### 3. AES-CBC Encryption 🔄
- Generate unique encryption key per request
- Encrypt anonymization mapping
- Store encrypted_key in database
- Implement decryption for mapping retrieval

### 4. Update All Services 🔄
- Update remaining services (DOCX, TXT, CSV, XLSX, JSON, Tavily)
- Add country parameter to all process_document() methods
- Update repository calls to include prospect_id and country

### 5. Testing 🔄
- Test with US prospects
- Test with international prospects
- Verify country detection accuracy
- Test fallback to US default

## Files Modified

```
Development/
├── main.py                              # Updated startup
├── controllers/
│   └── PIIController.py                 # Added Tavily integration
├── services/
│   └── PDFService.py                    # Added country parameter
├── utility/
│   ├── database.py                      # Lakebase integration
│   ├── ORM.py                           # Added prospect_id, country
│   ├── models.py                        # NEW: Pydantic models
│   ├── TavilyCountrySearch.py          # NEW: Country detection
│   └── TAVILY_COUNTRY_SEARCH_README.md # NEW: Documentation
├── repository/
│   └── PIIRepository.py                 # Added prospect methods
├── requirements.txt                     # Added requests
├── .env.example                         # Added Lakebase/Tavily config
└── test_tavily_country_search.py       # NEW: Test script
```

## Testing the Integration

1. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test Tavily country search**:
   ```bash
   python test_tavily_country_search.py
   ```

4. **Run the API**:
   ```bash
   python main.py
   ```

5. **Test the endpoint**:
   ```bash
   curl -X POST "http://localhost:8000/v1/handle-pii" \
     -F "assessment_id=your-uuid" \
     -F "prospect_id=your-uuid" \
     -F "caller_name=test-service" \
     -F "input_type=pdf" \
     -F "document=@sample.pdf"
   ```

## Success Criteria

✅ Database connected to Lakebase
✅ Prospect country detected via Tavily
✅ Country stored in database
✅ Pydantic validation for all Tavily I/O
✅ Fallback to US when country not detected
✅ Comprehensive logging
✅ Error handling

## Notes

- Tavily country detection relies only on the `answer` field from Tavily API
- No text parsing or extraction is performed
- Country detection defaults to "United States" on any error
- All Tavily inputs/outputs are validated with Pydantic models
- The system is ready for country-specific PII detection implementation
