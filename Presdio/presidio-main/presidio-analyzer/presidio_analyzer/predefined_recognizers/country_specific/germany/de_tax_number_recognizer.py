from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class DeTaxNumberRecognizer(PatternRecognizer):
    """
    Recognize German tax numbers (Steuernummer) using regex.

    Format: 10-11 characters as 2-3 digits / 3 digits / 5 digits
    (e.g., 11/123/12345 or 111/123/12345).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "DE Tax Number (medium)",
            r"\b\d{2,3}\/\d{3}\/\d{5}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "steuernummer",
        "steuer",
        "tax number",
        "tax id",
        "finanzamt",
        "tin",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "de",
        supported_entity: str = "DE_TAX_NUMBER",
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
