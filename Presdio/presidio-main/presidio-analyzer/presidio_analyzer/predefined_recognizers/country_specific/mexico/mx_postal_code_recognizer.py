from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MxPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize Mexican postal codes using regex.

    Format: 5 digits. First two digits indicate the state.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "MX Postal Code (medium)",
            r"\b\d{5}\b",
            0.6,
        ),
    ]

    CONTEXT = [
        "codigo postal",
        "c.p.",
        "cp",
        "postal",
        "postcode",
        "direccion",
        "address",
        "mexico",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "MX_POSTAL_CODE",
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
        """Validate Mexican postal code range (01000-99999)."""
        digits = pattern_text.strip()
        if not digits.isdigit() or len(digits) != 5:
            return True
        code = int(digits)
        if code < 1000:
            return True
        return False
