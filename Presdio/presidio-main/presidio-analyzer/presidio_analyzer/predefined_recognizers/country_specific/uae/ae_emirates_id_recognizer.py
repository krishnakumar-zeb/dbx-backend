from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AeEmiratesIdRecognizer(PatternRecognizer):
    """
    Recognize UAE Emirates ID using regex.

    Format: 15 digits as 784-YYYY-NNNNNNN-C
    (784 = UAE code, YYYY = birth year, NNNNNNN = unique ID, C = check digit).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Emirates ID (medium)",
            r"\b784-\d{4}-\d{7}-\d\b",
            0.6,
        ),
    ]

    CONTEXT = [
        "emirates id",
        "هوية إماراتية",
        "id card",
        "identity",
        "uae id",
        "resident",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AE_EMIRATES_ID",
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
