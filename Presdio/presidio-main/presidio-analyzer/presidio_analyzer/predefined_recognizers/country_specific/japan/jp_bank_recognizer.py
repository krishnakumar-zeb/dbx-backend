from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class JpBankRecognizer(PatternRecognizer):
    """
    Recognize Japanese bank numbers (Zengin format) using regex.

    Format: 7 digits hyphenated as 4-3 (bank code + branch code).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "JP Bank Zengin (high)",
            r"\b\d{4}-\d{3}\b",
            0.75,
        ),
    ]

    CONTEXT = [
        "bank",
        "銀行",
        "zengin",
        "全銀",
        "branch",
        "支店",
        "account",
        "口座",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "JP_BANK_NUMBER",
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
