from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class InDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize Indian driving licence numbers using regex.

    Format: 16 alphanumeric characters.
    2 letters (state) + 2 digits (RTO) + space/hyphen + 4 digits (year) + 7 digits.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "IN Driver License with separator (medium)",
            r"\b[A-Z]{2}[-\s]?\d{2}[-\s]?(?:19|20)\d{2}\d{7}\b",
            0.5,
        ),
        Pattern(
            "IN Driver License compact (weak)",
            r"\b[A-Z]{2}\d{13}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "driving licence",
        "driver license",
        "driving license",
        "dl",
        "rto",
        "licence number",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "IN_DRIVER_LICENSE",
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
