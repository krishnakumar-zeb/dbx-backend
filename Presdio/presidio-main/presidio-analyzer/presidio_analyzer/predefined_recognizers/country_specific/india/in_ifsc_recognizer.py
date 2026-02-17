from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class InIfscRecognizer(PatternRecognizer):
    """
    Recognize Indian IFSC codes and bank account numbers using regex.

    IFSC Format: 4 letters (bank) + 0 + 6 alphanumeric (branch).
    Account numbers: 9-18 digits (no fixed format, low confidence).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "IFSC Code (medium)",
            r"(?-i)\b[A-Z]{4}0[A-Z0-9]{6}\b",
            0.6,
        ),
        Pattern(
            "IN Account Number (weak)",
            r"\b\d{9,18}\b",
            0.05,
        ),
    ]

    CONTEXT = [
        "ifsc",
        "bank",
        "account",
        "branch",
        "neft",
        "rtgs",
        "imps",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "IN_IFSC",
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
