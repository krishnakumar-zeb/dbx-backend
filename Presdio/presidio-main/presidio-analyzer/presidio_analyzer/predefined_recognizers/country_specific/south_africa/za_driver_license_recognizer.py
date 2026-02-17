from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class ZaDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize South African driver's license numbers using regex.

    Format: 12-character alphanumeric code.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ZA Driver License (weak)",
            r"\b[A-Z0-9]{12}\b",
            0.2,
        ),
    ]

    CONTEXT = [
        "driver",
        "license",
        "licence",
        "driving",
        "dl",
        "traffic",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ZA_DRIVER_LICENSE",
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
