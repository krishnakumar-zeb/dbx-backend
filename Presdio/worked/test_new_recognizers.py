"""Test script for all new custom recognizers."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.generic.age_recognizer import AgeRecognizer
from presidio_analyzer.predefined_recognizers.generic.gender_recognizer import GenderRecognizer
from presidio_analyzer.predefined_recognizers.generic.ethnicity_recognizer import EthnicityRecognizer
from presidio_analyzer.predefined_recognizers.generic.cookie_recognizer import CookieRecognizer


def test_age_recognizer():
    """Test the Age recognizer."""
    print("\n" + "=" * 70)
    print("AGE RECOGNIZER TEST")
    print("=" * 70)
    
    recognizer = AgeRecognizer()
    
    test_cases = [
        "John is 25 years old",
        "Patient age: 45",
        "She is aged 30",
        "The child is 5 yrs old",
        "Age range: 18-25 years old",
        "He turned 65 y.o. last month",
        "Invalid: 150 years old",  # Should be rejected
        "The year 2020",  # Should not detect without context
    ]
    
    for text in test_cases:
        results = recognizer.analyze(text, ["AGE"])
        print(f"\nText: '{text}'")
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected}' (score: {result.score:.2f})")
        else:
            print("  ✗ No age detected")


def test_gender_recognizer():
    """Test the Gender recognizer."""
    print("\n" + "=" * 70)
    print("GENDER RECOGNIZER TEST")
    print("=" * 70)
    
    recognizer = GenderRecognizer()
    
    test_cases = [
        "Gender: male",
        "She identifies as female",
        "Patient is a woman",
        "The man walked in",
        "They are non-binary",
        "Pronouns: they/them",
        "Title: Mr. Smith",
        "Gender: prefer not to say",
        "The transgender community",
    ]
    
    for text in test_cases:
        results = recognizer.analyze(text, ["GENDER"])
        print(f"\nText: '{text}'")
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected}' (score: {result.score:.2f})")
        else:
            print("  ✗ No gender detected")


def test_ethnicity_recognizer():
    """Test the Ethnicity recognizer."""
    print("\n" + "=" * 70)
    print("ETHNICITY RECOGNIZER TEST")
    print("=" * 70)
    
    # Test with default deny list first
    recognizer = EthnicityRecognizer()
    
    test_cases = [
        "Ethnicity: African American",
        "Patient is Hispanic",
        "Race: Caucasian",
        "Asian heritage",
        "Native American ancestry",
        "Latino background",
        "Middle Eastern descent",
        "Pacific Islander origin",
    ]
    
    for text in test_cases:
        results = recognizer.analyze(text, ["ETHNICITY"])
        print(f"\nText: '{text}'")
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected}' (score: {result.score:.2f})")
        else:
            print("  ✗ No ethnicity detected")
    
    # Test with JSON file
    print("\n--- Testing with ethnicities.json ---")
    recognizer_json = EthnicityRecognizer(ethnicity_json_path="ethnicities.json")
    
    json_test_cases = [
        "He is Samoan",
        "Korean heritage",
        "Vietnamese background",
        "Moroccan descent",
    ]
    
    for text in json_test_cases:
        results = recognizer_json.analyze(text, ["ETHNICITY"])
        print(f"\nText: '{text}'")
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected}' (score: {result.score:.2f})")
        else:
            print("  ✗ No ethnicity detected")


def test_cookie_recognizer():
    """Test the Cookie recognizer."""
    print("\n" + "=" * 70)
    print("COOKIE RECOGNIZER TEST")
    print("=" * 70)
    
    recognizer = CookieRecognizer()
    
    test_cases = [
        "session_id=abc123def456ghi789jkl012mno345pqr678",
        "cookie: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r",
        "auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
        "Session ID: 550e8400-e29b-41d4-a716-446655440000",
        "token=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
        "Invalid: test",  # Too short
        "Just some text",  # No cookie pattern
    ]
    
    for text in test_cases:
        results = recognizer.analyze(text, ["COOKIE"])
        print(f"\nText: '{text}'")
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected[:50]}...' (score: {result.score:.2f})")
        else:
            print("  ✗ No cookie detected")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("TESTING ALL NEW CUSTOM RECOGNIZERS")
    print("=" * 70)
    
    test_age_recognizer()
    test_gender_recognizer()
    test_ethnicity_recognizer()
    test_cookie_recognizer()
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
