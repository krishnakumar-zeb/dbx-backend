"""Singapore-specific recognizers package."""

from .sg_bank_recognizer import SgBankRecognizer
from .sg_fin_recognizer import SgFinRecognizer
from .sg_passport_recognizer import SgPassportRecognizer
from .sg_postal_code_recognizer import SgPostalCodeRecognizer
from .sg_uen_recognizer import SgUenRecognizer

__all__ = [
    "SgBankRecognizer",
    "SgFinRecognizer",
    "SgPassportRecognizer",
    "SgPostalCodeRecognizer",
    "SgUenRecognizer",
]
