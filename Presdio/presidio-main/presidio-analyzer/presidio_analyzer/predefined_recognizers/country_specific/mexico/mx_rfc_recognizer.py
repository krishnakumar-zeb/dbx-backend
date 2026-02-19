from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MxRfcRecognizer(PatternRecognizer):
    """
    Recognize Mexican RFC (Registro Federal de Contribuyentes) using regex.

    Formats:
    - Individual: 13 chars - 4 letters (name) + 6 digits (DOB) + 3 (homoclave)
    - Business: 12 chars - 3 letters (name) + 6 digits (DOB) + 3 (homoclave)

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "RFC Individual (high)",
            r"\b[A-Z&Ññ]{4}\d{6}[A-Z0-9]{3}\b",
            0.9,
        ),
        Pattern(
            "RFC Business (high)",
            r"\b[A-Z&Ññ]{3}\d{6}[A-Z0-9]{3}\b",
            0.9,
        ),
    ]

    CONTEXT = [
        "rfc",
        "registro federal",
        "contribuyentes",
        "fiscal",
        "tax",
        "sat",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "MX_RFC",
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
