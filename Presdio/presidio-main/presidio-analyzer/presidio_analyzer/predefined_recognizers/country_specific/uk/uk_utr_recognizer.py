from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class UkUtrRecognizer(PatternRecognizer):
    """
    Recognize UK Unique Taxpayer Reference (UTR) and PAYE numbers using regex.

    Formats:
    - UTR: 10 digits
    - PAYE: 3 digits / alphanumeric (e.g., 123/AB12345)

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "UTR (weak)",
            r"\b\d{10}\b",
            0.1,
        ),
        Pattern(
            "PAYE Reference (medium)",
            r"\b\d{3}\/[A-Z0-9]{1,10}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "utr",
        "unique taxpayer",
        "taxpayer reference",
        "paye",
        "hmrc",
        "tax reference",
        "self assessment",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "UK_UTR",
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
