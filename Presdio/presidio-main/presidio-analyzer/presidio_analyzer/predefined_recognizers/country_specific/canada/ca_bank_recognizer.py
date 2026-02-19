from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaBankRecognizer(PatternRecognizer):
    """
    Recognize Canadian bank transit/institution numbers using regex.

    Formats: 5-digit transit + 3-digit institution (e.g., 12345-001)
    or 9-digit electronic format prefixed with 0.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Transit-Institution (high)",
            r"\b\d{5}[-]\d{3}\b",
            0.7,
        ),
        Pattern(
            "Electronic format (medium)",
            r"\b0\d{8}\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "transit",
        "institution",
        "bank",
        "account",
        "routing",
        "branch",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_BANK_NUMBER",
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
