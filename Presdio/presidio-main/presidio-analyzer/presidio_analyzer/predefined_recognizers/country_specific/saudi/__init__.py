"""Saudi Arabia-specific recognizers package."""

from .sa_national_id_recognizer import SaNationalIdRecognizer
from .sa_postal_code_recognizer import SaPostalCodeRecognizer
from .sa_tin_recognizer import SaTinRecognizer

__all__ = [
    "SaNationalIdRecognizer",
    "SaPostalCodeRecognizer",
    "SaTinRecognizer",
]
