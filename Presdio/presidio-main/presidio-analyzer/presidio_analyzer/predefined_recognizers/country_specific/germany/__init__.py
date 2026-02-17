"""Germany-specific recognizers package."""

from .de_postal_code_recognizer import DePostalCodeRecognizer
from .de_pension_insurance_recognizer import DePensionInsuranceRecognizer
from .de_driver_license_recognizer import DeDriverLicenseRecognizer
from .de_tax_number_recognizer import DeTaxNumberRecognizer

__all__ = [
    "DePostalCodeRecognizer",
    "DePensionInsuranceRecognizer",
    "DeDriverLicenseRecognizer",
    "DeTaxNumberRecognizer",
]
