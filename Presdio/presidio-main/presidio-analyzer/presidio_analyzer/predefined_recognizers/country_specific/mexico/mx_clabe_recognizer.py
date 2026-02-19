from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MxClabeRecognizer(PatternRecognizer):
    """
    Recognize Mexican CLABE (Clave Bancaria Estandarizada) using regex.

    Format: 18 digits - 3 (bank) + 3 (branch) + 11 (account) + 1 (check digit).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "CLABE (high)",
            r"\b\d{18}\b",
            0.8,
        ),
    ]

    CONTEXT = [
        "clabe",
        "cuenta",
        "banco",
        "bank",
        "account",
        "transferencia",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "MX_CLABE",
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
