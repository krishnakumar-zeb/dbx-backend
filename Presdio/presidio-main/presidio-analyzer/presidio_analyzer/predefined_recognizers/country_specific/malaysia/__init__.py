"""Malaysia-specific recognizers package."""

from .my_nric_recognizer import MyNricRecognizer
from .my_postal_code_recognizer import MyPostalCodeRecognizer
from .my_bank_recognizer import MyBankRecognizer
from .my_income_tax_recognizer import MyIncomeTaxRecognizer

__all__ = [
    "MyNricRecognizer",
    "MyPostalCodeRecognizer",
    "MyBankRecognizer",
    "MyIncomeTaxRecognizer",
]
