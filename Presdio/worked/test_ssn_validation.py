"""Test SSN validation to understand why 551-00-1234 is rejected."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.country_specific.us.us_ssn_recognizer import UsSsnRecognizer

def test_ssn():
    recognizer = UsSsnRecognizer()
    
    test_cases = [
        ("442-88-8902", "Elena's SSN - should detect"),
        ("551-00-1234", "Julian's SSN - currently rejected (middle group is 00)"),
        ("123-45-6789", "Valid format"),
        ("000-12-3456", "Invalid - starts with 000"),
        ("666-12-3456", "Invalid - starts with 666"),
        ("123-00-4567", "Invalid - middle group is 00"),
    ]
    
    print("=" * 70)
    print("SSN VALIDATION TEST")
    print("=" * 70)
    
    for ssn, description in test_cases:
        results = recognizer.analyze(ssn, ["US_SSN"])
        
        # Also test validation directly
        is_invalid = recognizer.invalidate_result(ssn)
        
        print(f"\nSSN: {ssn}")
        print(f"Description: {description}")
        print(f"Validation says invalid: {is_invalid}")
        print(f"Detected: {'YES' if results else 'NO'}")
        if results:
            print(f"  Score: {results[0].score:.2f}")

if __name__ == "__main__":
    test_ssn()
