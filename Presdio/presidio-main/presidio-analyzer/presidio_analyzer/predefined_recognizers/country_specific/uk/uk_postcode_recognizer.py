from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class UkPostcodeRecognizer(PatternRecognizer):
    """
    Recognize UK postcodes using regex.

    Supports all six UK postcode formats:
    A1 1AA, A11 1AA, AA1 1AA, AA11 1AA, A1A 1AA, AA1A 1AA.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "UK Postcode (medium)",
            r"\b[A-Z][A-HJ-Y]?\d[A-Z\d]?\s?\d[A-Z]{2}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "postcode",
        "post code",
        "postal code",
        "address",
        "uk",
        "united kingdom",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "UK_POSTCODE",
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
