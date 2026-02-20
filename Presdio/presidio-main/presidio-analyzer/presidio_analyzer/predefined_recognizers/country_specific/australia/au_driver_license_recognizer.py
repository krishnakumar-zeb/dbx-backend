from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AuDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize Australian driver licence numbers using regex.

    Format: 6-10 digits (varies by state: NSW=8, VIC=9, etc.).
    Low confidence due to similarity with account numbers.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "AU Driver Licence (weak)",
            r"\b\d{6,10}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "driver licence",
        "driver license",
        "driving licence",
        "licence number",
        "license number",
        "dl",
        "rms",
        "vicroads",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AU_DRIVER_LICENSE",
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
