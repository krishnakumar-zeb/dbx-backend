from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AeDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize UAE driver's license numbers using regex.

    Formats: 7-9 digits (Dubai area) or 10-15 digits (other emirates).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "AE Driver License short (weak)",
            r"\b\d{7,9}\b",
            0.1,
        ),
        Pattern(
            "AE Driver License long (weak)",
            r"\b\d{10,15}\b",
            0.1,
        ),
    ]

    CONTEXT = [
        "driver",
        "license",
        "licence",
        "driving",
        "رخصة قيادة",
        "رخصة",
        "rta",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AE_DRIVER_LICENSE",
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
