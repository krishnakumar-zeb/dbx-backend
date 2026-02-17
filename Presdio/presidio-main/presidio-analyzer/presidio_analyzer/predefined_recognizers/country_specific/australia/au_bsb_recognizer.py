from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AuBsbRecognizer(PatternRecognizer):
    """
    Recognize Australian BSB (Bank-State-Branch) numbers using regex.

    Format: 6 digits, often as 3 digits + hyphen/space + 3 digits.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "BSB with separator (medium)",
            r"\b\d{3}[-\s]\d{3}\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "bsb",
        "bank",
        "branch",
        "account",
        "transfer",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AU_BSB",
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
