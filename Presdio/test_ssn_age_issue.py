"""
Test to identify why SSN 123-45-6789 and age 45 are not detected
"""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import AgeRecognizer
from presidio_analyzer.predefined_recognizers.country_specific.us import UsSsnRecognizer

# Test SSN
print("=" * 60)
print("TESTING SSN: 123-45-6789")
print("=" * 60)

ssn_recognizer = UsSsnRecognizer()
test_ssn = "123-45-6789"

# Check if it matches pattern
import re
for pattern in ssn_recognizer.patterns:
    match = re.search(pattern.regex, test_ssn)
    if match:
        print(f"✓ Pattern '{pattern.name}' matched: {match.group()}")
        
        # Check validation
        is_invalid = ssn_recognizer.invalidate_result(test_ssn)
        print(f"  Validation result: {'INVALID ❌' if is_invalid else 'VALID ✓'}")
        
        if is_invalid:
            # Debug why it's invalid
            only_digits = "".join(c for c in test_ssn if c.isdigit())
            print(f"  Digits only: {only_digits}")
            
            # Check each validation rule
            if all(only_digits[0] == c for c in only_digits):
                print(f"  ❌ Failed: All same digit")
            
            if only_digits[3:5] == "00" or only_digits[5:] == "0000":
                print(f"  ❌ Failed: Groups cannot be all zeros")
            
            for sample_ssn in ("000", "666", "123456789", "98765432", "078051120"):
                if only_digits.startswith(sample_ssn):
                    print(f"  ❌ Failed: Starts with invalid pattern '{sample_ssn}'")
                    break

# Test with analyzer
analyzer = AnalyzerEngine()
text_with_ssn = "My SSN is 123-45-6789"
results = analyzer.analyze(text=text_with_ssn, entities=["US_SSN"], language='en')
print(f"\nAnalyzer results: {len(results)} detections")
for r in results:
    print(f"  - {r.entity_type}: '{text_with_ssn[r.start:r.end]}' (score: {r.score})")

print("\n" + "=" * 60)
print("TESTING AGE: 'age 45'")
print("=" * 60)

age_recognizer = AgeRecognizer()

# Check if it matches pattern
test_age_texts = [
    "age 45",
    "aged 45",
    "45 years old",
    "Dr. Chen, age 45, is a physician"
]

for test_text in test_age_texts:
    print(f"\nTesting: '{test_text}'")
    for pattern in age_recognizer.patterns:
        match = re.search(pattern.regex, test_text, re.IGNORECASE)
        if match:
            print(f"  ✓ Pattern '{pattern.name}' matched: {match.group()}")
            is_invalid = age_recognizer.invalidate_result(match.group())
            print(f"    Validation: {'INVALID ❌' if is_invalid else 'VALID ✓'}")
        else:
            print(f"  ✗ Pattern '{pattern.name}' did not match")

# Test with analyzer
analyzer.registry.add_recognizer(AgeRecognizer())
text_with_age = "Dr. Chen, age 45, is a physician"
results = analyzer.analyze(text=text_with_age, entities=["AGE"], language='en')
print(f"\nAnalyzer results for '{text_with_age}': {len(results)} detections")
for r in results:
    print(f"  - {r.entity_type}: '{text_with_age[r.start:r.end]}' (score: {r.score})")
