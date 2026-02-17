from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class FrDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize French driving licence numbers using regex.

    Formats:
    - Modern (post-2013): 12 numeric digits
    - Old (pre-2013): 2 digits + 2 letters + 5 digits (e.g., 12AB12345)

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "FR Modern License (weak)",
            r"\b\d{12}\b",
            0.2,
        ),
        Pattern(
            "FR Old License (medium)",
            r"\b\d{2}[A-Z]{2}\d{5}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "permis de conduire",
        "permis",
        "driving licence",
        "driver license",
        "licence",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "FR_DRIVER_LICENSE",
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
