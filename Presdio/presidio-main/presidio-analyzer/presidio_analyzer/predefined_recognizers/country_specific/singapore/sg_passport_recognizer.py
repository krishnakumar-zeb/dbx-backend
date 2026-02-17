from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class SgPassportRecognizer(PatternRecognizer):
    """
    Recognize Singapore passport numbers using regex.

    Format: 9 characters - starts with E or K, 7 digits, then a check letter.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SG Passport (medium)",
            r"\b[EK]\d{7}[A-Z]\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "passport",
        "travel document",
        "ica",
        "immigration",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "SG_PASSPORT",
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
