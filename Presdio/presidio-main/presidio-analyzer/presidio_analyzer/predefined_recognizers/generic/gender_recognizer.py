from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class GenderRecognizer(PatternRecognizer):
    """
    Recognize gender using deny list approach.

    Detects gender mentions including male, female, non-binary, and related terms.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    :param deny_list: List of gender terms to detect
    """

    # Comprehensive gender deny list
    DENY_LIST = [
        # Binary genders
        "male", "female","non-binary", "nonbinary", "non binary","transgender"
    ]

    PATTERNS = []

    CONTEXT = [
        "gender",
        "sex",
        "identify",
        "identifies as",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "GENDER",
        deny_list: Optional[List[str]] = None,
        name: Optional[str] = None,
    ):
        deny_list = deny_list if deny_list else self.DENY_LIST
        
        # Create patterns from deny list
        patterns = []
        for term in deny_list:
            # Escape special regex characters and create word boundary pattern
            escaped_term = term.replace(".", r"\.")
            # Use case-insensitive matching
            pattern = Pattern(
                f"Gender: {term}",
                rf"(?i)\b{escaped_term}\b",
                0.6,
            )
            patterns.append(pattern)
        
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
            name=name,
        )
