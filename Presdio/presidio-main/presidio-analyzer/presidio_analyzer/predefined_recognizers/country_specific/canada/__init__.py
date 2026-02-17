"""Canada-specific recognizers package."""

from .ca_postal_code_recognizer import CaPostalCodeRecognizer
from .ca_sin_recognizer import CaSinRecognizer
from .ca_bank_recognizer import CaBankRecognizer
from .ca_driver_license_recognizer import CaDriverLicenseRecognizer
from .ca_gst_recognizer import CaGstRecognizer

__all__ = [
    "CaPostalCodeRecognizer",
    "CaSinRecognizer",
    "CaBankRecognizer",
    "CaDriverLicenseRecognizer",
    "CaGstRecognizer",
]
