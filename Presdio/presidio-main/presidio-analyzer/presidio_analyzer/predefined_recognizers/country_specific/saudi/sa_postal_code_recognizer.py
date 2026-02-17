from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class SaPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize Saudi postal codes using regex.

    Format: 5 digits, optionally with a 4-digit extension.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SA Postal Code with extension (medium)",
            r"\b\d{5}-\d{4}\b",
            0.5,
        ),
        Pattern(
            "SA Postal Code (weak)",
            r"\b\d{5}\b",
            0.2,
        ),
    ]

    CONTEXT = [
        "postal code",
        "postcode",
        "رمز بريدي",
        "بريد",
        "address",
        "عنوان",
        "saudi",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "SA_POSTAL_CODE",
        name: Optional[str] = None,
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
            name=name,
        )
