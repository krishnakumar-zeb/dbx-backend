from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class JpCorporateNumberRecognizer(PatternRecognizer):
    """
    Recognize Japanese corporate numbers using regex.

    Format: 13 digits (check digit + 12 digits).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "JP Corporate Number (weak)",
            r"\b\d{13}\b",
            0.2,
        ),
    ]

    CONTEXT = [
        "corporate number",
        "法人番号",
        "houjin",
        "company number",
        "business",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "JP_CORPORATE_NUMBER",
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
