"""
Country-specific PII configuration.
Maps each supported country to its PII entity types (10 common + country-specific).
All entity detection is handled by Presidio's built-in and custom recognizers.

Common Entities (10): PERSON, EMAIL_ADDRESS, PHONE_NUMBER, LOCATION, AGE, GENDER,
                      ETHNICITY, IP_ADDRESS, COOKIE, CERTIFICATE_NUMBER
Country-Specific: Varies by country (e.g., US_SSN, ZIP_CODE, CA_SIN, etc.)

Note: Regex patterns and recognition logic are defined in Presidio recognizer classes,
not in this config file. This file only defines which entities to look for per country.
"""
from typing import Dict, List

SUPPORTED_COUNTRIES = [
    "Canada", "Mexico", "United States", "United Kingdom",
    "Germany", "France", "UAE", "Saudi Arabia",
    "South Africa", "Japan", "India", "Australia",
    "Singapore", "Malaysia",
]

DEFAULT_COUNTRY = "United States"

# ============================================================
# ENTITY LISTS PER COUNTRY
# ============================================================
# Total: 10 common entities + country-specific entities

# Common entities shared across all countries (10 total)
_COMMON_ENTITIES = [
    "PERSON",           # Person names
    "EMAIL_ADDRESS",    # Email addresses
    "PHONE_NUMBER",     # Phone numbers
    "LOCATION",         # Addresses, cities, states
    "AGE",              # Age mentions
    "GENDER",           # Gender mentions
    "ETHNICITY",        # Ethnicity/race
    "IP_ADDRESS",       # IP addresses
    "COOKIE",           # Session IDs, tokens, cookies
    "CERTIFICATE_NUMBER", # Certificates, licenses, policy numbers
]

# Country-specific entity overrides (merged with common)
# Entity names must match the supported_entity in the recognizer classes
_COUNTRY_SPECIFIC: Dict[str, List[str]] = {
    "United States": [
        "US_SSN", "US_DRIVER_LICENSE",
        "US_BANK_NUMBER", "ZIP_CODE",  
    ],
    "Canada": [
        "CA_SIN", "CA_BANK_NUMBER", "CA_DRIVER_LICENSE",
        "CA_POSTAL_CODE", "CA_GST_NUMBER",
    ],
    "Mexico": [
        "MX_CURP", "MX_RFC", "MX_DRIVER_LICENSE",
        "MX_POSTAL_CODE", "MX_CLABE",
    ],
    "United Kingdom": [
        "UK_NHS", "UK_NINO", "UK_DRIVER_LICENSE",
        "UK_POSTAL_CODE", "UK_BANK_SORT_CODE", "UK_UTR", "IBAN_CODE",
    ],
    "Germany": [
        "DE_DRIVER_LICENSE", "DE_TAX_NUMBER", "DE_PENSION_INSURANCE",
        "DE_POSTAL_CODE", "IBAN_CODE",
    ],
    "France": [
        "FR_INSEE", "FR_DRIVER_LICENSE", "FR_SPI",
        "FR_POSTAL_CODE", "IBAN_CODE",
    ],
    "UAE": [
        "AE_EMIRATES_ID", "AE_TRN", "AE_DRIVER_LICENSE",
        "AE_POSTAL_CODE", "IBAN_CODE",
    ],
    "Saudi Arabia": [
        "SA_NATIONAL_ID", "SA_POSTAL_CODE", "SA_TIN", "IBAN_CODE",
    ],
    "South Africa": [
        "ZA_ID_NUMBER", "ZA_TAX_NUMBER", "ZA_DRIVER_LICENSE",
        "ZA_POSTAL_CODE", "IBAN_CODE",
    ],
    "Japan": [
        "JP_MY_NUMBER", "JP_DRIVER_LICENSE", "JP_BANK_NUMBER",
        "JP_POSTAL_CODE", "JP_CORPORATE_NUMBER",
    ],
    "India": [
        "IN_AADHAAR", "IN_PAN",
        "IN_DRIVER_LICENSE",
        "IN_PIN_CODE", "IN_IFSC",
    ],
    "Australia": [
        "AU_TFN", "AU_MEDICARE", "AU_DRIVER_LICENSE",
        "AU_POSTAL_CODE", "AU_ABN", "AU_BSB",
    ],
    "Singapore": [
        "SG_NRIC_FIN", "SG_PASSPORT", "SG_BANK_NUMBER",
        "SG_UEN", "SG_POSTAL_CODE",
    ],
    "Malaysia": [
        "MY_NRIC", "MY_INCOME_TAX", "MY_BANK_NUMBER",
        "MY_POSTAL_CODE",
    ],
}


def get_entities_for_country(country: str) -> List[str]:
    """
    Return the full entity list (common + USA + country-specific) for a country.
    
    USA entities are ALWAYS included regardless of detected country, as documents
    from any country may contain US PII (SSN, ZIP codes, etc.).
    
    Args:
        country: Country name (e.g., "United States", "Canada")
        
    Returns:
        List of entity names to detect (10 common + USA + country-specific)
        
    Example:
        >>> get_entities_for_country("Canada")
        ['PERSON', 'EMAIL_ADDRESS', ..., 'US_SSN', 'ZIP_CODE', ..., 'CA_SIN', 'CA_BANK_NUMBER', ...]
        
        >>> get_entities_for_country("United States")
        ['PERSON', 'EMAIL_ADDRESS', ..., 'US_SSN', 'ZIP_CODE', ...]
    """
    # Get USA entities (always included)
    usa_entities = _COUNTRY_SPECIFIC.get("United States", [])
    
    # Get country-specific entities
    if country == "United States":
        # For USA, don't duplicate USA entities
        country_entities = []
    else:
        # For other countries, get their specific entities
        country_entities = _COUNTRY_SPECIFIC.get(country, [])
    
    # Combine: Common + USA + Country-specific
    # Use dict.fromkeys to deduplicate while preserving order
    all_entities = _COMMON_ENTITIES + usa_entities + country_entities
    return list(dict.fromkeys(all_entities))
