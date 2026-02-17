from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class ZaTaxNumberRecognizer(PatternRecognizer):
    """
    Recognize South African tax numbers using regex.

    Format: 10 digits starting with 0, 1, 2, 3, 4 (VAT), or 9.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ZA Tax Number (medium)",
            r"\b[012349]\d{9}\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "tax number",
        "tax",
        "sars",
        "income tax",
        "vat",
        "taxpayer",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ZA_TAX_NUMBER",
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
