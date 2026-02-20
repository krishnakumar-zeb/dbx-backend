from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MyNricRecognizer(PatternRecognizer):
    """
    Recognize Malaysian NRIC/MyKad numbers using regex.

    Format: 12 digits as YYMMDD-SS-NNNN (DOB + state code + serial).
    Also used as driver's license (differentiated by context).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "NRIC with separators (medium)",
            r"\b\d{6}[-\s]\d{2}[-\s]\d{4}\b",
            0.5,
        ),
        Pattern(
            "NRIC continuous (weak)",
            r"\b\d{12}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "nric",
        "mykad",
        "ic",
        "identity card",
        "kad pengenalan",
        "driver",
        "license",
        "licence",
        "lesen memandu",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "MY_NRIC",
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
