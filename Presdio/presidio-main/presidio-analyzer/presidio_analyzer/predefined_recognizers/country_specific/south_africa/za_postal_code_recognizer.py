from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class ZaPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize South African postal codes using regex.

    Format: 4 digits ranging from 0001 to 9999.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ZA Postal Code (weak)",
            r"\b\d{4}\b",
            0.1,
        ),
    ]

    CONTEXT = [
        "postal code",
        "postcode",
        "post code",
        "address",
        "south africa",
        "sa",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ZA_POSTAL_CODE",
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

    def invalidate_result(self, pattern_text: str) -> bool:
        """Validate South African postal code (0001-9999)."""
        digits = pattern_text.strip()
        if not digits.isdigit() or len(digits) != 4:
            return True
        code = int(digits)
        if code < 1:
            return True
        return False
