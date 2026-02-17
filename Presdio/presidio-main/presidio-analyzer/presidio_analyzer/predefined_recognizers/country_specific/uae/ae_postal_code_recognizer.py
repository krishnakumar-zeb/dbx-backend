from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AePostalCodeRecognizer(PatternRecognizer):
    """
    Recognize UAE P.O. Box and Makani ID using regex.

    Formats:
    - P.O. Box: 1-6 digits (P.O. Box 4567)
    - Makani ID: 10 digits as 5+5 (30032 95320)

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "P.O. Box (medium)",
            r"\b(?:P\.?O\.?\s?Box\s?)\d{1,6}\b",
            0.6,
        ),
        Pattern(
            "Makani ID (medium)",
            r"\b\d{5}\s\d{5}\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "p.o. box",
        "po box",
        "makani",
        "address",
        "عنوان",
        "صندوق بريد",
        "uae",
        "dubai",
        "abu dhabi",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AE_POSTAL_CODE",
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
