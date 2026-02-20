from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MyPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize Malaysian postal codes using regex.

    Format: 5 digits. First two digits indicate the state.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "MY Postal Code (weak)",
            r"\b\d{5}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "poskod",
        "postal code",
        "postcode",
        "address",
        "alamat",
        "malaysia",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "MY_POSTAL_CODE",
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
