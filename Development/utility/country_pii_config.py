"""
Country-specific PII configuration.
Maps each supported country to its 14 PII entity types with regex patterns
and Presidio entity mappings based on the PII_Define_Documentation.xlsx.
"""
import re
from typing import Dict, List, Tuple

# ============================================================
# SUPPORTED COUNTRIES
# ============================================================
SUPPORTED_COUNTRIES = [
    "Canada", "Mexico", "United States", "United Kingdom",
    "Germany", "France", "UAE", "Saudi Arabia",
    "South Africa", "Japan", "India", "Australia",
    "Singapore", "Malaysia",
]

DEFAULT_COUNTRY = "United States"

# ============================================================
# COUNTRY -> PRESIDIO ENTITY LIST  (14 per country)
# ============================================================
# These are the Presidio built-in + custom entity names we ask
# the analyzer to look for per country.

# Common entities shared across all countries
_COMMON_ENTITIES = [
    "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "IP_ADDRESS",
    "LOCATION", "DATE_TIME", "URL", "CREDIT_CARD",
]

# Country-specific entity overrides (merged with common)
_COUNTRY_SPECIFIC: Dict[str, List[str]] = {
    "United States": [
        "US_SSN", "US_PASSPORT", "US_DRIVER_LICENSE",
        "US_BANK_NUMBER", "US_ITIN", "MEDICAL_LICENSE",
    ],
    "Canada": [
        "CA_SOCIAL_INSURANCE_NUMBER", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "HEALTH_CARD", "MEDICAL_LICENSE",
    ],
    "Mexico": [
        "CURP", "RFC", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "MEDICAL_LICENSE",
    ],
    "United Kingdom": [
        "UK_NHS", "UK_NINO", "PASSPORT", "DRIVER_LICENSE",
        "IBAN_CODE", "MEDICAL_LICENSE",
    ],
    "Germany": [
        "DE_ID_CARD", "PASSPORT", "DRIVER_LICENSE",
        "IBAN_CODE", "DE_TAX_ID", "MEDICAL_LICENSE",
    ],
    "France": [
        "FR_INSEE", "PASSPORT", "DRIVER_LICENSE",
        "IBAN_CODE", "FR_TAX_ID", "MEDICAL_LICENSE",
    ],
    "UAE": [
        "EMIRATES_ID", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "UAE_TRN", "MEDICAL_LICENSE",
    ],
    "Saudi Arabia": [
        "SA_NATIONAL_ID", "PASSPORT", "DRIVER_LICENSE",
        "IBAN_CODE", "SA_IQAMA", "MEDICAL_LICENSE",
    ],
    "South Africa": [
        "ZA_ID_NUMBER", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "ZA_TAX_NUMBER", "MEDICAL_LICENSE",
    ],
    "Japan": [
        "JP_MY_NUMBER", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "JP_RESIDENCE_CARD", "MEDICAL_LICENSE",
    ],
    "India": [
        "IN_AADHAAR", "IN_PAN", "PASSPORT", "DRIVER_LICENSE",
        "IN_VOTER_ID", "MEDICAL_LICENSE",
    ],
    "Australia": [
        "AU_TFN", "AU_MEDICARE", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "MEDICAL_LICENSE",
    ],
    "Singapore": [
        "SG_NRIC_FIN", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "SG_UEN", "MEDICAL_LICENSE",
    ],
    "Malaysia": [
        "MY_NRIC", "PASSPORT", "DRIVER_LICENSE",
        "BANK_ACCOUNT", "MY_TAX_ID", "MEDICAL_LICENSE",
    ],
}


def get_entities_for_country(country: str) -> List[str]:
    """Return the full entity list (common + country-specific) for a country."""
    specific = _COUNTRY_SPECIFIC.get(country, _COUNTRY_SPECIFIC[DEFAULT_COUNTRY])
    return list(dict.fromkeys(_COMMON_ENTITIES + specific))  # deduplicated, order preserved


# ============================================================
# COUNTRY-SPECIFIC REGEX PATTERNS
# ============================================================
# Each entry: (entity_name, compiled_regex, context_words, score)

_US_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("US_SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), ["ssn", "social security"], 0.85),
    ("US_SSN", re.compile(r"\b\d{9}\b"), ["ssn", "social security"], 0.6),
    ("US_ITIN", re.compile(r"\b9\d{2}-[7-9]\d-\d{4}\b"), ["itin", "tax"], 0.85),
    ("US_BANK_NUMBER", re.compile(r"\b\d{8,17}\b"), ["account", "bank", "routing"], 0.5),
    ("US_PASSPORT", re.compile(r"\b[A-Z]?\d{8,9}\b"), ["passport"], 0.6),
    ("US_DRIVER_LICENSE", re.compile(r"\b[A-Z]\d{7,14}\b"), ["driver", "license", "dl"], 0.6),
]

_CA_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("CA_SOCIAL_INSURANCE_NUMBER", re.compile(r"\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b"), ["sin", "social insurance"], 0.85),
    ("HEALTH_CARD", re.compile(r"\b\d{4}[\s-]?\d{3}[\s-]?\d{3}[\s-]?[A-Z]{2}\b"), ["health card", "ohip"], 0.8),
    ("PASSPORT", re.compile(r"\b[A-Z]{2}\d{6}\b"), ["passport"], 0.7),
]

_MX_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("CURP", re.compile(r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b"), ["curp"], 0.95),
    ("RFC", re.compile(r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b"), ["rfc", "tax"], 0.9),
]

_UK_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("UK_NINO", re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]\b", re.I), ["nino", "national insurance"], 0.9),
    ("UK_NHS", re.compile(r"\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b"), ["nhs"], 0.8),
    ("PASSPORT", re.compile(r"\b\d{9}\b"), ["passport"], 0.6),
]

_DE_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("DE_TAX_ID", re.compile(r"\b\d{11}\b"), ["steuer", "tax", "tin"], 0.7),
    ("DE_ID_CARD", re.compile(r"\b[CFGHJKLMNPRTVWXYZ0-9]{9}\b"), ["personalausweis", "id card"], 0.6),
]

_FR_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("FR_INSEE", re.compile(r"\b[12]\d{2}(0[1-9]|1[0-2])\d{2}\d{3}\d{3}\d{2}\b"), ["insee", "securite sociale"], 0.9),
    ("FR_TAX_ID", re.compile(r"\b\d{13}\b"), ["fiscal", "tax"], 0.6),
]

_UAE_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("EMIRATES_ID", re.compile(r"\b784-\d{4}-\d{7}-\d\b"), ["emirates id", "eid"], 0.95),
    ("UAE_TRN", re.compile(r"\b\d{15}\b"), ["trn", "tax registration"], 0.6),
]

_SA_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("SA_NATIONAL_ID", re.compile(r"\b[12]\d{9}\b"), ["national id", "huwiyya"], 0.8),
    ("SA_IQAMA", re.compile(r"\b2\d{9}\b"), ["iqama", "residence"], 0.7),
]

_ZA_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("ZA_ID_NUMBER", re.compile(r"\b\d{13}\b"), ["id number", "identity"], 0.7),
    ("ZA_TAX_NUMBER", re.compile(r"\b\d{10}\b"), ["tax", "sars"], 0.6),
]

_JP_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("JP_MY_NUMBER", re.compile(r"\b\d{12}\b"), ["my number", "マイナンバー"], 0.8),
    ("JP_RESIDENCE_CARD", re.compile(r"\b[A-Z]{2}\d{8}[A-Z]{2}\b"), ["residence card", "在留カード"], 0.85),
]

_IN_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("IN_AADHAAR", re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"), ["aadhaar", "aadhar", "uid"], 0.85),
    ("IN_PAN", re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), ["pan", "permanent account"], 0.9),
    ("IN_VOTER_ID", re.compile(r"\b[A-Z]{3}\d{7}\b"), ["voter", "epic"], 0.8),
]

_AU_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("AU_TFN", re.compile(r"\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b"), ["tfn", "tax file"], 0.8),
    ("AU_MEDICARE", re.compile(r"\b\d{4}[\s-]?\d{5}[\s-]?\d[\s-]?\d?\b"), ["medicare"], 0.8),
]

_SG_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("SG_NRIC_FIN", re.compile(r"\b[STFGM]\d{7}[A-Z]\b"), ["nric", "fin"], 0.9),
    ("SG_UEN", re.compile(r"\b\d{8,9}[A-Z]\b"), ["uen", "business"], 0.7),
]

_MY_PATTERNS: List[Tuple[str, re.Pattern, List[str], float]] = [
    ("MY_NRIC", re.compile(r"\b\d{6}-\d{2}-\d{4}\b"), ["nric", "ic", "mykad"], 0.9),
    ("MY_TAX_ID", re.compile(r"\b(IG|SG|OG|C|D)\d{10}\b"), ["tax", "lhdn"], 0.8),
]

COUNTRY_REGEX_MAP: Dict[str, List[Tuple[str, re.Pattern, List[str], float]]] = {
    "United States": _US_PATTERNS,
    "Canada": _CA_PATTERNS,
    "Mexico": _MX_PATTERNS,
    "United Kingdom": _UK_PATTERNS,
    "Germany": _DE_PATTERNS,
    "France": _FR_PATTERNS,
    "UAE": _UAE_PATTERNS,
    "Saudi Arabia": _SA_PATTERNS,
    "South Africa": _ZA_PATTERNS,
    "Japan": _JP_PATTERNS,
    "India": _IN_PATTERNS,
    "Australia": _AU_PATTERNS,
    "Singapore": _SG_PATTERNS,
    "Malaysia": _MY_PATTERNS,
}


def get_regex_patterns_for_country(
    country: str,
) -> List[Tuple[str, re.Pattern, List[str], float]]:
    """Return regex patterns for a given country (defaults to US)."""
    return COUNTRY_REGEX_MAP.get(country, COUNTRY_REGEX_MAP[DEFAULT_COUNTRY])
