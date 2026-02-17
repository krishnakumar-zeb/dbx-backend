from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class InPinCodeRecognizer(PatternRecognizer):
    """
    Recognize Indian PIN codes using regex.

    Format: 6 digits with optional space after 3rd digit.
    First digit cannot be 0.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "IN PIN Code with space (medium)",
            r"\b[1-9]\d{2}\s\d{3}\b",
            0.4,
        ),
        Pattern(
            "IN PIN Code (weak)",
            r"\b[1-9]\d{5}\b",
            0.1,
        ),
    ]

    CONTEXT = [
        "pin code",
        "pincode",
        "pin",
        "postal code",
        "postcode",
        "address",
        "india",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "IN_PIN_CODE",
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
