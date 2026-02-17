from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CertificateRecognizer(PatternRecognizer):
    """
    Recognize certificate numbers, license numbers, and identification numbers.

    Detects various alphanumeric certificate formats including:
    - Passport numbers (9 digits or letter + 8 digits)
    - Driver's licenses (state-specific formats)
    - Professional licenses (pilot, medical, etc.)
    - Policy numbers (insurance, medical, etc.)
    - Certificate serials and other identification numbers

    All detected as CERTIFICATE_NUMBER entity type.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        # Passport formats
        Pattern(
            "Passport - Letter + 8 digits (strong)",
            r"\b[A-Z]-?\d{8}\b",
            0.7,
        ),
        Pattern(
            "Passport - 9 digits (medium)",
            r"\b\d{9}\b",
            0.4,
        ),
        
        # License/Certificate with prefix and suffix
        Pattern(
            "License/Certificate - Prefix-Number-Suffix (strong)",
            r"\b[A-Z]{2,4}-\d{5,7}-[A-Z0-9]{1,3}\b",
            0.8,
        ),
        
        # License/Certificate with dashes
        Pattern(
            "License/Certificate - Alphanumeric with dashes (medium)",
            r"\b[A-Z]{2,4}-\d{3,4}-[A-Z0-9]{2,6}-?\d{0,2}\b",
            0.6,
        ),
        
        # Policy/Medical ID numbers
        Pattern(
            "Policy/Medical ID - Prefix-Number (medium)",
            r"\b[A-Z]{2,4}-\d{4,7}-?[A-Z0-9]?\b",
            0.6,
        ),
        
        # Certificate serial numbers (hex-like)
        Pattern(
            "Certificate Serial - Hex format (medium)",
            r"\b\d{2}-\d{2}-\d{2}-[A-F0-9]{2}-[A-F0-9]{2}-[A-F0-9]{2}-\d{2}-\d{2}\b",
            0.7,
        ),
        
        # License plate format
        Pattern(
            "License Plate - State format (medium)",
            r"\b[A-Z]{2}-\d{3}-[A-Z]{3}\b",
            0.5,
        ),
        
        # Generic alphanumeric certificate (weak - requires context)
        Pattern(
            "Generic Certificate - Alphanumeric (weak)",
            r"\b[A-Z]{2,5}\d{5,9}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "passport",
        "license",
        "licence",
        "certificate",
        "cert",
        "id",
        "identification",
        "number",
        "policy",
        "medical",
        "driver",
        "pilot",
        "professional",
        "global entry",
        "plate",
        "serial",
        "credential",
        "permit",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CERTIFICATE_NUMBER",
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
        Check if the pattern text cannot be validated as a certificate number.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        # Remove common separators for validation
        cleaned = pattern_text.replace("-", "").replace(" ", "")
        
        # Must have at least some letters or be exactly 9 digits (passport)
        has_letters = any(c.isalpha() for c in cleaned)
        is_nine_digits = cleaned.isdigit() and len(cleaned) == 9
        
        if not has_letters and not is_nine_digits:
            # If no letters and not 9 digits, likely not a certificate
            return True
        
        # Reject if too short
        if len(cleaned) < 5:
            return True
        
        # Reject if too long
        if len(cleaned) > 20:
            return True
        
        # Reject common false positives
        false_positives = [
            "PAGE", "SECTION", "CHAPTER", "ARTICLE", "PARAGRAPH",
            "FIGURE", "TABLE", "APPENDIX", "EXHIBIT",
        ]
        
        upper_text = pattern_text.upper()
        for fp in false_positives:
            if fp in upper_text:
                return True
        
        # Reject if it's all the same character
        if len(set(cleaned)) == 1:
            return True
        
        return False
