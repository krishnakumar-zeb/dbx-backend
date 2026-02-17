from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize Canadian provincial driver's license numbers using regex.

    Formats vary by province:
    - Ontario: 1 letter + 14 digits (grouped by hyphens)
    - Quebec: 1 letter + 12 digits

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Ontario format (medium)",
            r"\b[A-Z]\d{4}[ -]?\d{5}[ -]?\d{5}\b",
            0.4,
        ),
        Pattern(
            "Quebec format (medium)",
            r"\b[A-Z]\d{12}\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "driver",
        "licence",
        "license",
        "driving",
        "dl",
        "permit",
        "ontario",
        "quebec",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_DRIVER_LICENSE",
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
