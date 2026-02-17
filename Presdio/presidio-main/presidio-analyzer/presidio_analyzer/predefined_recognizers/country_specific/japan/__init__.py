"""Japan-specific recognizers package."""

from .jp_postal_code_recognizer import JpPostalCodeRecognizer
from .jp_my_number_recognizer import JpMyNumberRecognizer
from .jp_bank_recognizer import JpBankRecognizer
from .jp_driver_license_recognizer import JpDriverLicenseRecognizer
from .jp_corporate_number_recognizer import JpCorporateNumberRecognizer

__all__ = [
    "JpPostalCodeRecognizer",
    "JpMyNumberRecognizer",
    "JpBankRecognizer",
    "JpDriverLicenseRecognizer",
    "JpCorporateNumberRecognizer",
]
