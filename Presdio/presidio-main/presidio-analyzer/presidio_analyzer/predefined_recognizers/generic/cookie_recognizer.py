from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CookieRecognizer(PatternRecognizer):
    """
    Recognize cookies and session identifiers using regex.

    Detects session IDs, tokens, and cookie values with context words.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Session ID with context (strong)",
            r"\b(?:session[_\s-]?id|sessionid|sess[_\s-]?id|sessid)\s*[=:]\s*([a-zA-Z0-9\-_]{16,})\b",
            0.8,
        ),
        Pattern(
            "Cookie with context (strong)",
            r"\b(?:cookie|token|auth[_\s-]?token|access[_\s-]?token)\s*[=:]\s*([a-zA-Z0-9\-_\.]{16,})\b",
            0.8,
        ),
        Pattern(
            "JWT Token",
            r"\beyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\b",
            0.9,
        ),
        Pattern(
            "Generic session token (medium)",
            r"\b[a-zA-Z0-9]{32,}\b",
            0.3,
        ),
        Pattern(
            "UUID format (medium)",
            r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
            0.5,
        ),
        Pattern(
            "Alphanumeric token with dashes/underscores (weak)",
            r"\b[a-zA-Z0-9\-_]{20,}\b",
            0.2,
        ),
    ]

    CONTEXT = [
        "session",
        "cookie",
        "token",
        "auth",
        "authentication",
        "authorization",
        "bearer",
        "access",
        "refresh",
        "csrf",
        "xsrf",
        "jwt",
        "api key",
        "apikey",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "COOKIE",
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
        Check if the pattern text cannot be validated as a cookie/token.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        # Remove common prefixes/suffixes for validation
        text = pattern_text.lower()
        
        # Reject if it's only underscores or dashes
        cleaned = pattern_text.replace("_", "").replace("-", "").replace(" ", "")
        if len(cleaned) == 0:
            return True
        
        # Reject if it's a common word or number-only
        if text.isdigit():
            return True
        
        # Reject if too short (after removing context)
        if len(pattern_text) < 16:
            return True
        
        # Must have at least some alphanumeric characters
        alphanumeric_count = sum(c.isalnum() for c in pattern_text)
        if alphanumeric_count < 8:
            return True
        
        # Reject common false positives
        false_positives = [
            "example", "test", "sample", "placeholder",
            "undefined", "null", "none", "default"
        ]
        
        for fp in false_positives:
            if fp in text:
                return True
        
        return False
