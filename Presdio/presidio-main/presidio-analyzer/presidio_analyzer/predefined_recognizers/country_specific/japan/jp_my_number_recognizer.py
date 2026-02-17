from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class JpMyNumberRecognizer(PatternRecognizer):
    """
    Recognize Japanese My Number (Individual Number) using regex.

    Format: 12 digits, often separated at every 4 digits by hyphens or spaces.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "My Number with separators (medium)",
            r"\b\d{4}[-\s]\d{4}[-\s]\d{4}\b",
            0.5,
        ),
        Pattern(
            "My Number continuous (weak)",
            r"\b\d{12}\b",
            0.1,
        ),
    ]

    CONTEXT = [
        "my number",
        "マイナンバー",
        "個人番号",
        "individual number",
        "mynumber",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "JP_MY_NUMBER",
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
