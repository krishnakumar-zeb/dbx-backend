from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaGstRecognizer(PatternRecognizer):
    """
    Recognize Canadian GST/HST business numbers using regex.

    Format: 9-digit Business Number + RT + 4-digit reference (e.g., 123456789RT0001).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "GST/HST Number (high)",
            r"\b\d{9}RT\d{4}\b",
            0.8,
        ),
    ]

    CONTEXT = [
        "gst",
        "hst",
        "business number",
        "bn",
        "tax",
        "canada revenue",
        "cra",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_GST_NUMBER",
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
