from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class FrSpiRecognizer(PatternRecognizer):
    """
    Recognize French SPI (tax identification) number using regex.

    Format: 13 digits grouped as 2-2-3-3-3 (e.g., 12 34 567 890 123).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SPI with spaces (medium)",
            r"\b\d{2}\s\d{2}\s\d{3}\s\d{3}\s\d{3}\b",
            0.5,
        ),
        Pattern(
            "SPI continuous (weak)",
            r"\b\d{13}\b",
            0.1,
        ),
    ]

    CONTEXT = [
        "spi",
        "numero fiscal",
        "fiscal",
        "impot",
        "tax",
        "contribuable",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "FR_SPI",
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
