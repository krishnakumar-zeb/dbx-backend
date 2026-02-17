"""Mexico-specific recognizers package."""

from .mx_curp_recognizer import MxCurpRecognizer
from .mx_clabe_recognizer import MxClabeRecognizer
from .mx_postal_code_recognizer import MxPostalCodeRecognizer
from .mx_rfc_recognizer import MxRfcRecognizer
from .mx_driver_license_recognizer import MxDriverLicenseRecognizer

__all__ = [
    "MxCurpRecognizer",
    "MxClabeRecognizer",
    "MxPostalCodeRecognizer",
    "MxRfcRecognizer",
    "MxDriverLicenseRecognizer",
]
