import json
import os
from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class EthnicityRecognizer(PatternRecognizer):
    """
    Recognize ethnicity using deny list approach.

    Detects ethnicity mentions from a comprehensive list of ethnic groups.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    :param deny_list: List of ethnicity terms to detect
    """

    # Default ethnicity deny list (subset for performance)
    # Full list can be loaded from JSON file
    DENY_LIST = [
        "African American", "Asian", "Caucasian", "Hispanic", "Latino", "Latina",
        "White", "Black", "Native American", "Pacific Islander", "Indigenous",
        "European", "African", "Middle Eastern", "South Asian", "East Asian",
        "Southeast Asian", "Arab", "Jewish", "Indian", "Chinese", "Japanese",
        "Korean", "Vietnamese", "Filipino", "Mexican", "Puerto Rican", "Cuban",
        "American Indian", "Alaska Native", "Native Hawaiian", "Samoan"
    ]

    CONTEXT = [
        "ethnicity",
        "ethnic",
        "race",
        "racial",
        "heritage",
        "ancestry",
        "descent",
        "origin",
        "background",
        "nationality",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "ETHNICITY",
        deny_list: Optional[List[str]] = None,
        ethnicity_json_path: Optional[str] = None,
        name: Optional[str] = None,
    ):
        # Load from JSON if path provided
        if ethnicity_json_path and os.path.exists(ethnicity_json_path):
            try:
                with open(ethnicity_json_path, 'r', encoding='utf-8') as f:
                    deny_list = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load ethnicity JSON: {e}")
                deny_list = deny_list if deny_list else self.DENY_LIST
        else:
            deny_list = deny_list if deny_list else self.DENY_LIST
        
        # Create patterns from deny list
        patterns = []
        for term in deny_list:
            # Escape special regex characters
            escaped_term = term.replace("(", r"\(").replace(")", r"\)").replace("/", r"\/")
            escaped_term = escaped_term.replace(".", r"\.").replace("-", r"\-")
            escaped_term = escaped_term.replace("'", r"\'")
            
            pattern = Pattern(
                f"Ethnicity: {term}",
                rf"\b{escaped_term}\b",
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
