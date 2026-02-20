from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MxDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize Mexican driver's license (Licencia de Conducir) using regex.

    Format: 7-12 alphanumeric characters (varies by state).

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Licencia de Conducir (14 digits)",
            r"\b[A-Z0-9]{7,12}\b",
            0.9,
        ),
    ]

    CONTEXT = [
        "licencia",
        "conducir",
        "driver",
        "license",
        "licence",
        "driving",
        "permiso",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "MX_DRIVER_LICENSE",
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
        """
        Validate that the license contains both letters and digits.
        This prevents matching pure alphabetic words.
        """
        text = pattern_text.strip().upper()
        has_letter = any(c.isalpha() for c in text)
        has_digit = any(c.isdigit() for c in text)

        # Must have both letters and digits
        if not (has_letter and has_digit):
            return False

        # Must not be all digits (that would be other IDs)
        if text.isdigit():
            return False

        # Must not be all letters (that would be words)
        if text.isalpha():
            return False

        return True
