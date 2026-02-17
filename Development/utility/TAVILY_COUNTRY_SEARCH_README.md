# Tavily Country Search Utility

## Overview

The Tavily Country Search utility uses the Tavily API to detect a prospect's country from their company name and optional additional context. It validates all inputs and outputs using Pydantic models for type safety.

## Supported Countries

The utility searches for prospects in the following 14 countries:

1. Canada
2. Mexico
3. United States
4. United Kingdom
5. Germany
6. France
7. UAE
8. Saudi Arabia
9. South Africa
10. Japan
11. India
12. Australia
13. Singapore
14. Malaysia

## Features

- **Pydantic Validation**: All inputs and outputs are validated using Pydantic models
- **Confidence Scoring**: Returns confidence level (high, medium, low, none)
- **Source Tracking**: Tracks where the country information was found
- **Special Case Handling**: Handles abbreviations (USA, UK, UAE, etc.)
- **Error Handling**: Graceful fallback when country cannot be detected

## Usage

### Basic Usage

```python
from utility.TavilyCountrySearch import detect_prospect_country

# Simple detection
result = detect_prospect_country("Microsoft")

print(f"Country: {result.country}")
print(f"Confidence: {result.confidence}")
print(f"Matched from list: {result.matched_from_list}")
```

### With Additional Context

```python
from utility.TavilyCountrySearch import detect_prospect_country

# Detection with context for better accuracy
result = detect_prospect_country(
    prospect_name="Toyota",
    additional_context="Automotive manufacturer"
)

print(f"Country: {result.country}")
print(f"Confidence: {result.confidence}")
print(f"Source: {result.source}")
```

### Using the Class

```python
from utility.TavilyCountrySearch import TavilyCountrySearch

# Initialize
tavily_search = TavilyCountrySearch()

# Search for country
result = tavily_search.search_prospect_country(
    prospect_name="Siemens",
    additional_context="Engineering company"
)

# Get supported countries list
countries = tavily_search.get_supported_countries()
```

## Pydantic Models

### TavilySearchRequest

Input validation for Tavily API requests:

```python
class TavilySearchRequest(BaseModel):
    query: str  # 1-500 characters
    search_depth: str  # "basic" or "advanced"
    max_results: int  # 1-10
    include_domains: Optional[List[str]]
    exclude_domains: Optional[List[str]]
```

### TavilySearchResponse

Validation for Tavily API responses:

```python
class TavilySearchResponse(BaseModel):
    query: str
    results: List[dict]
    answer: Optional[str]
    images: Optional[List[str]]
    response_time: Optional[float]
```

### CountryDetectionResult

Output model for country detection:

```python
class CountryDetectionResult(BaseModel):
    country: Optional[str]  # Detected country name
    confidence: str  # "high", "medium", "low", or "none"
    source: Optional[str]  # Source URL or identifier
    matched_from_list: bool  # True if in supported countries
```

## Confidence Levels

- **high**: Country found in Tavily answer or first result title
- **medium**: Country found in first 2 results content
- **low**: Country found in results 3-5
- **none**: Country not detected

## Environment Variables

Required environment variable:

```bash
TAVILY_API_KEY=your_tavily_api_key_here
```

## Error Handling

The utility handles errors gracefully:

- Missing API key: Raises `PIIException` with code 500
- API request failure: Raises `PIIException` with code 503
- Network timeout: Returns result with confidence "none"
- Invalid response: Returns result with confidence "none"

## Testing

Run the test script to verify functionality:

```bash
python test_tavily_country_search.py
```

The test script will:
1. Display all supported countries
2. Test detection for multiple companies
3. Show confidence levels and sources
4. Verify if detected countries are in the supported list

## Integration Example

```python
from utility.TavilyCountrySearch import detect_prospect_country
from repository.PIIRepository import PIIRepository

# Detect country
country_result = detect_prospect_country(
    prospect_name=prospect_name,
    additional_context="Technology company"
)

# Use in PII processing
if country_result.matched_from_list:
    # Apply country-specific PII detection
    country = country_result.country
    print(f"Applying PII rules for: {country}")
else:
    # Use default US rules
    country = "United States"
    print("Using default US PII rules")

# Save to database
repository.save_pii_details(
    request_id=request_id,
    assessment_id=assessment_id,
    prospect_id=prospect_id,
    country=country,
    # ... other fields
)
```

## Special Cases

The utility handles common abbreviations and variations:

- **United States**: Matches "USA", "U.S.", "US"
- **United Kingdom**: Matches "UK", "U.K."
- **UAE**: Matches "United Arab Emirates", "UAE"
- **Saudi Arabia**: Matches "Saudi", "KSA"

## Logging

The utility logs important events:

```python
import logging

logger = logging.getLogger(__name__)

# Logs include:
# - Search queries
# - Detection results
# - Confidence levels
# - Errors and warnings
```

## Best Practices

1. **Provide Context**: Include additional context for better accuracy
2. **Check Confidence**: Use high/medium confidence results
3. **Validate Results**: Check `matched_from_list` flag
4. **Handle Failures**: Always have a fallback (default to US)
5. **Cache Results**: Consider caching country results per prospect

## Limitations

- Requires active internet connection
- Depends on Tavily API availability
- Limited to 14 supported countries
- May not detect country for very small/local companies
- Accuracy depends on publicly available information
