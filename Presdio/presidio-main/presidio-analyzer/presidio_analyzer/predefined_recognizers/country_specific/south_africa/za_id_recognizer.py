from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class ZaIdRecognizer(PatternRecognizer):
    """
    Recognize South African ID numbers using regex.

    Format: 13 digits - YYMMDD (DOB) + SSSS (gender) + C (citizenship)
    + 8 (race, deprecated) + Z (check digit).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ZA ID Number (medium)",
            r"\b\d{2}[01]\d[0-3]\d\s?\d{4}\s?[01]8\d\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "id number",
        "identity",
        "south african id",
        "sa id",
        "id book",
        "smart card",
        "citizen",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ZA_ID_NUMBER",
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
