from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class SgPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize Singapore postal codes using regex.

    Format: 6 digits. First two digits range from 01 to 82 (sector codes).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SG Postal Code (weak)",
            r"\b(?:[0-7]\d|8[0-2])\d{4}\b",
            0.2,
        ),
    ]

    CONTEXT = [
        "postal code",
        "postcode",
        "singapore",
        "address",
        "blk",
        "block",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "SG_POSTAL_CODE",
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
