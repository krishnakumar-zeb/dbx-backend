from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class SaTinRecognizer(PatternRecognizer):
    """
    Recognize Saudi TIN/VAT ID using regex.

    Format: 15 digits starting with 3 (GCC code).
    Includes 8-digit TIN + 3-digit branch + tax type.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SA TIN/VAT (medium)",
            r"\b3\d{14}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "tin",
        "vat",
        "tax",
        "ضريبة",
        "رقم ضريبي",
        "zatca",
        "gazt",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "SA_TIN",
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
