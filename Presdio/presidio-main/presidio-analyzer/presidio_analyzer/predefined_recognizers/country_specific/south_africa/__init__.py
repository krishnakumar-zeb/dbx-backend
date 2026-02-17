"""South Africa-specific recognizers package."""

from .za_id_recognizer import ZaIdRecognizer
from .za_postal_code_recognizer import ZaPostalCodeRecognizer
from .za_driver_license_recognizer import ZaDriverLicenseRecognizer
from .za_tax_number_recognizer import ZaTaxNumberRecognizer

__all__ = [
    "ZaIdRecognizer",
    "ZaPostalCodeRecognizer",
    "ZaDriverLicenseRecognizer",
    "ZaTaxNumberRecognizer",
]
