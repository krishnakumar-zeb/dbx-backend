from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize Canadian postal codes using regex.

    Format: A9A 9A9 (letter-digit-letter space digit-letter-digit).
    Excludes invalid starting letters (D, F, I, O, Q, U, W, Z).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "CA Postal Code (high)",
            r"\b[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ][ -]?\d[ABCEGHJKLMNPRSTVWXYZ]\d\b",
            0.7,
        ),
    ]

    CONTEXT = [
        "postal code",
        "postcode",
        "postal",
        "zip",
        "mailing",
        "address",
        "canada",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_POSTAL_CODE",
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
