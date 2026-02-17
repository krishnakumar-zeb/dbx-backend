from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class FrInseeRecognizer(PatternRecognizer):
    """
    Recognize French INSEE number (NIR / Social Security Number) using regex.

    Format: 15 digits encoding gender, DOB, and place of birth.
    Starts with 1 (male) or 2 (female), followed by YY MM department commune serial key.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "INSEE with spaces (medium)",
            r"\b[12]\s?\d{2}\s?(?:0[1-9]|1[0-2])\s?\d{2,3}\s?\d{3}\s?\d{3}\s?\d{2}\b",
            0.5,
        ),
        Pattern(
            "INSEE continuous (weak)",
            r"\b[12]\d{14}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "insee",
        "nir",
        "securite sociale",
        "social security",
        "numero de securite",
        "secu",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "FR_INSEE",
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
