"""UAE-specific recognizers package."""

from .ae_emirates_id_recognizer import AeEmiratesIdRecognizer
from .ae_postal_code_recognizer import AePostalCodeRecognizer
from .ae_driver_license_recognizer import AeDriverLicenseRecognizer
from .ae_trn_recognizer import AeTrnRecognizer

__all__ = [
    "AeEmiratesIdRecognizer",
    "AePostalCodeRecognizer",
    "AeDriverLicenseRecognizer",
    "AeTrnRecognizer",
]
