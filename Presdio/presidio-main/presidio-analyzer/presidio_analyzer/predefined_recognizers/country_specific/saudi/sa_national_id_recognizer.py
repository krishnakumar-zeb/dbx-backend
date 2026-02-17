from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class SaNationalIdRecognizer(PatternRecognizer):
    """
    Recognize Saudi National ID and Iqama numbers using regex.

    Formats:
    - National ID: 10 digits starting with 1 (Saudi citizens)
    - Iqama: 10 digits starting with 2 (residents/expats)
    - Driver's License uses the same format as National ID.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Saudi National ID (medium)",
            r"\b1\d{9}\b",
            0.5,
        ),
        Pattern(
            "Iqama (medium)",
            r"\b2\d{9}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "national id",
        "iqama",
        "هوية",
        "إقامة",
        "resident",
        "citizen",
        "saudi id",
        "driver",
        "license",
        "licence",
        "رخصة",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "SA_NATIONAL_ID",
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
