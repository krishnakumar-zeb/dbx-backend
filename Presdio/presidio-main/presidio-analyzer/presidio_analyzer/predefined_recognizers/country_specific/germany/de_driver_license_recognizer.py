from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class DeDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize German driver's license numbers using regex.

    Format: 11 alphanumeric characters.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "DE Driver License (medium)",
            r"\b[0-9A-Z][0-9]{2}[0-9A-Z]{6}[0-9][0-9A-Z]\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "fuhrerschein",
        "führerschein",
        "driver",
        "license",
        "licence",
        "fahrerlaubnis",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "de",
        supported_entity: str = "DE_DRIVER_LICENSE",
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
