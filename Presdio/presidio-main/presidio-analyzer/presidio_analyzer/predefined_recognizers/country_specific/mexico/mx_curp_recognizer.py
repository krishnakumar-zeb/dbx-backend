from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class MxCurpRecognizer(PatternRecognizer):
    """
    Recognize Mexican CURP (Clave Única de Registro de Población) using regex.

    Format: 18 chars - 4 letters (name) + 6 digits (DOB) + H/M (gender)
    + 2 letters (state) + 3 consonants + check digits.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "CURP (medium)",
            r"(?-i)\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b",
            0.6,
        ),
    ]

    CONTEXT = [
        "curp",
        "clave unica",
        "registro de poblacion",
        "identificacion",
        "mexico",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "es",
        supported_entity: str = "MX_CURP",
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
