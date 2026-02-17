"""UK-specific recognizers package."""

from .uk_driver_license_recognizer import UkDriverLicenseRecognizer
from .uk_nhs_recognizer import NhsRecognizer
from .uk_nino_recognizer import UkNinoRecognizer
from .uk_postcode_recognizer import UkPostcodeRecognizer
from .uk_sort_code_recognizer import UkSortCodeRecognizer
from .uk_utr_recognizer import UkUtrRecognizer

__all__ = [
    "NhsRecognizer",
    "UkDriverLicenseRecognizer",
    "UkNinoRecognizer",
    "UkPostcodeRecognizer",
    "UkSortCodeRecognizer",
    "UkUtrRecognizer",
]
