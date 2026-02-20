from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AuPostcodeRecognizer(PatternRecognizer):
    """
    Recognize Australian postcodes using regex.

    Format: 4 digits covering all state ranges (NSW, VIC, QLD, etc.).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "AU Postcode (weak)",
            r"\b(?:0[289]\d{2}|[1-7]\d{3})\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "postcode",
        "post code",
        "postal code",
        "address",
        "australia",
        "nsw",
        "vic",
        "qld",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AU_POSTCODE",
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
