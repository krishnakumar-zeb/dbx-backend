from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class JpPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize Japanese postal codes using regex.

    Format: 7 digits with a hyphen after the first 3 (e.g., 123-4567).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "JP Postal Code (medium)",
            r"\b\d{3}-\d{4}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "postal code",
        "postcode",
        "〒",
        "郵便番号",
        "address",
        "住所",
        "japan",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "JP_POSTAL_CODE",
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
