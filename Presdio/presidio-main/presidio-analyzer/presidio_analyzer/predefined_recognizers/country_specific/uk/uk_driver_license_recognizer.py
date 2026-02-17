from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class UkDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize UK driving licence numbers using regex.

    Format: 16 characters encoding surname, DOB, and gender.
    First 5 chars from surname, digit encoding DOB/gender, remaining digits.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "UK Driving Licence (medium)",
            r"\b[A-Z9]{5}\d[0156]\d(?:[0][1-9]|[12]\d|3[01])\d[A-Z0-9]{3}[A-Z]{2}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "driving licence",
        "driver licence",
        "driving license",
        "driver license",
        "dvla",
        "licence number",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "UK_DRIVER_LICENSE",
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
