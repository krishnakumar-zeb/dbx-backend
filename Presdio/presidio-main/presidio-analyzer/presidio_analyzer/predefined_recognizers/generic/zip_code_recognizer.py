from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class ZipCodeRecognizer(PatternRecognizer):
    """
    Recognize US ZIP codes using regex.

    Supports:
    - 3-digit ZIP code prefixes (sectional centers)
    - 5-digit ZIP codes
    - ZIP+4 format (5 digits + 4 digits)

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ZIP Code (5 digits or ZIP+4)",
            r"\b\d{5}(?:\-\d{4})?\b",
            0.5,
        ),
        Pattern(
            "ZIP Code (3-digit prefix)",
            r"\b\d{3}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "zip",
        "zipcode",
        "zip code",
        "postal",
        "postal code",
        "postcode",
        "mail",
        "mailing",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ZIP_CODE",
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
        Check if the pattern text cannot be validated as a ZIP code.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        # Remove hyphen to get just digits
        digits_only = pattern_text.replace("-", "")
        
        # ZIP code should be 3, 5, or 9 digits
        if len(digits_only) not in (3, 5, 9):
            return True
        
        # For 3-digit ZIP codes (prefixes)
        if len(digits_only) == 3:
            # Valid 3-digit ZIP prefixes range from 001 to 999
            # Reject 000
            if digits_only == "000":
                return True
            # Reject if all digits are the same (e.g., 111, 222)
            if len(set(digits_only)) == 1:
                return True
            return False
        
        # For 5 or 9 digit ZIP codes
        # Reject if all digits are the same (e.g., 00000, 11111)
        if len(set(digits_only[:5])) == 1:
            return True
        
        # Reject known invalid ZIP codes
        # 00000-00999 are not valid ZIP codes
        if digits_only[:5].startswith("00"):
            return True
        
        return False
