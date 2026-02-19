"""Generic recognizers package."""

from .age_recognizer import AgeRecognizer
from .certificate_recognizer import CertificateRecognizer
from .cookie_recognizer import CookieRecognizer
from .credit_card_recognizer import CreditCardRecognizer
from .crypto_recognizer import CryptoRecognizer
from .date_recognizer import DateRecognizer
from .email_recognizer import EmailRecognizer
from .ethnicity_recognizer import EthnicityRecognizer
from .gender_recognizer import GenderRecognizer
from .iban_recognizer import IbanRecognizer
from .ip_recognizer import IpRecognizer
from .mac_recognizer import MacAddressRecognizer
from .phone_recognizer import PhoneRecognizer
from .url_recognizer import UrlRecognizer

__all__ = [
    "AgeRecognizer",
    "CertificateRecognizer",
    "CookieRecognizer",
    "CreditCardRecognizer",
    "CryptoRecognizer",
    "DateRecognizer",
    "EmailRecognizer",
    "EthnicityRecognizer",
    "GenderRecognizer",
    "IbanRecognizer",
    "IpRecognizer",
    "PhoneRecognizer",
    "UrlRecognizer",
    "MacAddressRecognizer",
]
