from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaSinRecognizer(PatternRecognizer):
    """
    Recognize Canadian Social Insurance Number (SIN) using regex.

    Format: 9 digits, often grouped as 123-456-789 or 123 456 789.
    Validated with Luhn checksum.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SIN with separators (medium)",
            r"\b\d{3}[-\s]\d{3}[-\s]\d{3}\b",
            0.5,
        ),
        Pattern(
            "SIN continuous (weak)",
            r"\b\d{9}\b",
            0.05,
        ),
    ]

    CONTEXT = [
        "sin",
        "social insurance",
        "social insurance number",
        "canada",
        "canadian",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_SIN",
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

    def validate_result(self, pattern_text: str) -> bool:
        """Validate using Luhn checksum."""
        digits = "".join(c for c in pattern_text if c.isdigit())
        if len(digits) != 9:
            return False
        # SIN cannot start with 0 or 8
        if digits[0] in ("0", "8"):
            return False
        return self._luhn_check(digits)

    @staticmethod
    def _luhn_check(digits: str) -> bool:
        """Perform Luhn checksum validation."""
        total = 0
        for i, d in enumerate(digits):
            n = int(d)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0
