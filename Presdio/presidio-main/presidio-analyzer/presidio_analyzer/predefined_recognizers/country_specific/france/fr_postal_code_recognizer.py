from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class FrPostalCodeRecognizer(PatternRecognizer):
    """
    Recognize French postal codes (Code Postal) using regex.

    Format: 5 digits. First two digits are the department number.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "FR Postal Code (weak)",
            r"\b\d{5}\b",
            0.2,
        ),
    ]

    CONTEXT = [
        "code postal",
        "postal",
        "postcode",
        "adresse",
        "address",
        "france",
        "cedex",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "FR_POSTAL_CODE",
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
        """Validate French postal code (department 01-95 + DOM-TOM 97x, 98x)."""
        digits = pattern_text.strip()
        if not digits.isdigit() or len(digits) != 5:
            return True
        dept = int(digits[:2])
        if dept < 1:
            return True
        return False
