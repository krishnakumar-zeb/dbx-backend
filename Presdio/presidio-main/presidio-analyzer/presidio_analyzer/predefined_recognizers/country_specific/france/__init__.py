"""France-specific recognizers package."""

from .fr_postal_code_recognizer import FrPostalCodeRecognizer
from .fr_insee_recognizer import FrInseeRecognizer
from .fr_driver_license_recognizer import FrDriverLicenseRecognizer
from .fr_spi_recognizer import FrSpiRecognizer

__all__ = [
    "FrPostalCodeRecognizer",
    "FrInseeRecognizer",
    "FrDriverLicenseRecognizer",
    "FrSpiRecognizer",
]
