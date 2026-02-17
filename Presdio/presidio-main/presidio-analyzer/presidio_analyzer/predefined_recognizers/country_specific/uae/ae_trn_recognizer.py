from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AeTrnRecognizer(PatternRecognizer):
    """
    Recognize UAE Tax Registration Number (TRN) using regex.

    Format: 15 digits, always starts with 100 (Federal Tax Authority code).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "TRN (medium)",
            r"\b100\d{12}\b",
            0.6,
        ),
    ]

    CONTEXT = [
        "trn",
        "tax registration",
        "vat",
        "fta",
        "ضريبة",
        "رقم ضريبي",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AE_TRN",
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
