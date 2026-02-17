from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class SgBankRecognizer(PatternRecognizer):
    """
    Recognize Singapore bank account numbers using regex.

    Format: 7-14 digits (varies by bank: OCBC=7, DBS=10, POSB=9).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SG Account with hyphens (medium)",
            r"\b\d{3}-\d{6}-\d{3}\b",
            0.4,
        ),
        Pattern(
            "SG Account Number (weak)",
            r"\b\d{7,14}\b",
            0.05,
        ),
    ]

    CONTEXT = [
        "account",
        "bank",
        "dbs",
        "ocbc",
        "uob",
        "posb",
        "maybank",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "SG_BANK_NUMBER",
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
