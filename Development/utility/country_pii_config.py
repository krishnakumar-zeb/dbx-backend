"""
Country-specific PII configuration.
Maps each supported country to its PII entity types (11 common + 5 country-specific = 16 total).
All entity detection is handled by Presidio's built-in and custom recognizers.

Common Entities (11): PERSON, EMAIL_ADDRESS, PHONE_NUMBER, LOCATION, AGE, GENDER,
                      ETHNICITY, IP_ADDRESS, COOKIE, CERTIFICATE_NUMBER, ZIP_CODE
Country-Specific (5): Varies by country (e.g., US_SSN, CA_SIN, etc.)

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
# ENTITY LISTS PER COUNTRY (14 per country)
# ============================================================
# Total: 9 common entities + 5 country-specific entities = 14 per country

# Common entities shared across all countries (11 total)
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
    "CERTIFICATE_NUMBER", # Certificates, licenses, policy numbers       # ZIP/postal codes
]

# Country-specific entity overrides (merged with common)
# Each country has exactly 5 country-specific entities
# Entity names must match the supported_entity in the recognizer classes
_COUNTRY_SPECIFIC: Dict[str, List[str]] = {
    "United States": [
        "US_SSN", "US_PASSPORT", "US_DRIVER_LICENSE",
        "US_BANK_NUMBER", "US_ITIN", "ZIP_CODE",  
    ],
    "Canada": [
        "CA_SIN",  # Not CA_SOCIAL_INSURANCE_NUMBER
        "CA_BANK_NUMBER",  # Not CA_BANK_ACCOUNT
        "CA_DRIVER_LICENSE",
        # Note: CA_PASSPORT and CA_HEALTH_CARD don't have recognizers yet
    ],
    "Mexico": [
        "MX_CURP", "MX_RFC", "MX_DRIVER_LICENSE",
        # Note: MX_PASSPORT and MX_BANK_ACCOUNT don't have recognizers yet
    ],
    "United Kingdom": [
        "UK_NHS", "UK_NINO", "UK_DRIVER_LICENSE",
        "IBAN_CODE",  # For UK_IBAN
        # Note: UK_PASSPORT doesn't have a recognizer yet
    ],
    "Germany": [
        "DE_DRIVER_LICENSE", "DE_TAX_NUMBER",
        "IBAN_CODE",  # For DE_IBAN
        # Note: DE_ID_CARD, DE_PASSPORT don't have recognizers yet
    ],
    "France": [
        "FR_INSEE", "FR_DRIVER_LICENSE",
        "IBAN_CODE",  # For FR_IBAN
        # Note: FR_PASSPORT, FR_TAX_ID don't have recognizers yet
    ],
    "UAE": [
        "AE_EMIRATES_ID", "AE_TRN", "AE_DRIVER_LICENSE",
        # Note: UAE_PASSPORT, UAE_BANK_ACCOUNT don't have recognizers yet
    ],
    "Saudi Arabia": [
        "SA_NATIONAL_ID",
        "IBAN_CODE",  # For SA_IBAN
        # Note: SA_PASSPORT, SA_DRIVER_LICENSE, SA_IQAMA don't have recognizers yet
    ],
    "South Africa": [
        "ZA_ID_NUMBER", "ZA_TAX_NUMBER", "ZA_DRIVER_LICENSE",
        # Note: ZA_PASSPORT, ZA_BANK_ACCOUNT don't have recognizers yet
    ],
    "Japan": [
        "JP_MY_NUMBER", "JP_DRIVER_LICENSE", "JP_BANK_NUMBER",
        # Note: JP_PASSPORT, JP_RESIDENCE_CARD don't have recognizers yet
    ],
    "India": [
        "IN_AADHAAR", "IN_PAN", "IN_PASSPORT",
        "IN_DRIVER_LICENSE", "IN_VOTER",  # Not IN_VOTER_ID
    ],
    "Australia": [
        "AU_TFN", "AU_MEDICARE", "AU_DRIVER_LICENSE",
        # Note: AU_PASSPORT, AU_BANK_ACCOUNT don't have recognizers yet
    ],
    "Singapore": [
        "SG_NRIC_FIN", "SG_PASSPORT", "SG_BANK_NUMBER",  # Not SG_BANK_ACCOUNT
        "SG_UEN",
        # Note: SG_DRIVER_LICENSE doesn't have a recognizer yet
    ],
    "Malaysia": [
        "MY_NRIC", "MY_INCOME_TAX",  # Not MY_TAX_ID
        "MY_BANK_NUMBER",  # Not MY_BANK_ACCOUNT
        # Note: MY_PASSPORT, MY_DRIVER_LICENSE don't have recognizers yet
    ],
}


def get_entities_for_country(country: str) -> List[str]:
    """
    Return the full entity list (common + country-specific) for a country.
    
    Args:
        country: Country name (e.g., "United States", "Canada")
        
    Returns:
        List of entity names to detect (16 total: 11 common + 5 country-specific)
        
    Example:
        >>> get_entities_for_country("Canada")
        ['PERSON', 'EMAIL_ADDRESS', ..., 'CA_SIN', 'CA_BANK_NUMBER', ...]
    """
    specific = _COUNTRY_SPECIFIC.get(country, _COUNTRY_SPECIFIC[DEFAULT_COUNTRY])
    return list(dict.fromkeys(_COMMON_ENTITIES + specific))  # deduplicated, order preserved
