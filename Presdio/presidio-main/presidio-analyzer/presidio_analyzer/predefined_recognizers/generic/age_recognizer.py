from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AgeRecognizer(PatternRecognizer):
    """
    Recognize age using regex and context.

    Detects age mentions in various formats like "25 years old", "age 30", "aged 45", etc.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Age with context (strong)",
            r"\b(?:age[ds]?|years?\s+old)\s*:?\s*(\d{1,3})\b",
            0.7,
        ),
        Pattern(
            "Age with context (strong)",
            r"\b(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b",
            0.7,
        ),
        Pattern(
            "Age hyphenated format (strong)",
            r"\b(\d{1,3})-year-old\b",
            0.7,
        ),
        Pattern(
            "Age range",
            r"\b(\d{1,3})\s*(?:-|to)\s*(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b",
            0.7,
        ),
        # Removed standalone pattern to avoid false positives with page numbers
    ]

    CONTEXT = [
        "age",
        "aged",
        "years old",
        "year old",
        "yrs old",
        "yr old",
        "y.o",
        "birthday",
        "born",
        "dob",
        "date of birth",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AGE",
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
        """
        Check if the pattern text cannot be validated as an age.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        # Extract just the digits from the pattern
        import re
        digits = re.findall(r'\d+', pattern_text)

        if not digits:
            return True

        # Check each number found
        for digit_str in digits:
            age = int(digit_str)

            # Age should be between 0 and 120 (reasonable human age range)
            if age < 0 or age > 120:
                return True

        return False

 