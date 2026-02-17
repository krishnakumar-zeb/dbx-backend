from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class DePensionInsuranceRecognizer(PatternRecognizer):
    """
    Recognize German pension insurance numbers (Rentenversicherungsnummer) using regex.

    Format: 12 characters - 2-digit area code + 6-digit DOB (DDMMYY)
    + 1 letter (initial) + 3-digit serial.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Pension Insurance with spaces (medium)",
            r"\b\d{2}\s?\d{6}\s?[A-Z]\s?\d{3}\b",
            0.5,
        ),
        Pattern(
            "Pension Insurance continuous (medium)",
            r"\b\d{8}[A-Z]\d{3}\b",
            0.5,
        ),
    ]

    CONTEXT = [
        "rentenversicherung",
        "pension",
        "versicherungsnummer",
        "sozialversicherung",
        "rvnr",
        "insurance number",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "de",
        supported_entity: str = "DE_PENSION_INSURANCE",
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
