from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class JpDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize Japanese driver's license numbers using regex.

    Format: 12 digits.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "JP Driver License (weak)",
            r"\b\d{12}\b",
            0.1,
        ),
    ]

    CONTEXT = [
        "driver",
        "license",
        "licence",
        "運転免許",
        "免許証",
        "driving",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "JP_DRIVER_LICENSE",
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
