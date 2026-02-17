"""Test the fixes for cookie and overlapping issues."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.generic.cookie_recognizer import CookieRecognizer
from presidio_analyzer import RecognizerResult

def test_cookie_fix():
    """Test that underscores are no longer detected as cookies."""
    print("=" * 70)
    print("COOKIE RECOGNIZER FIX TEST")
    print("=" * 70)
    
    recognizer = CookieRecognizer()
    
    test_cases = [
        ("________________________________________", "Should NOT detect (underscores only)"),
        ("_auth_session_id_772fb", "Should detect (valid session ID)"),
        ("_SECURE_AUTH_TOKEN_9921_", "Should detect (valid token)"),
        ("77-88-99-AA-BB-CC-00-11", "Should NOT detect (not enough alphanumeric)"),
    ]
    
    for text, description in test_cases:
        results = recognizer.analyze(text, ["COOKIE"])
        
        print(f"\nText: '{text}'")
        print(f"Description: {description}")
        
        if results:
            print(f"  ✓ Detected: {len(results)} cookie(s)")
        else:
            print("  ✗ No cookie detected")
    
    print("\n" + "=" * 70)


def test_overlap_handling():
    """Test that overlapping entities are handled correctly."""
    print("\nOVERLAPPING ENTITIES TEST")
    print("=" * 70)
    
    # Simulate overlapping results
    text = "John Smith is 45 years old"
    
    # Create mock results with overlaps
    results = [
        RecognizerResult(entity_type="PERSON", start=0, end=10, score=0.85),  # "John Smith"
        RecognizerResult(entity_type="PERSON", start=0, end=4, score=0.70),   # "John" (overlap)
        RecognizerResult(entity_type="AGE", start=14, end=26, score=0.70),    # "45 years old"
        RecognizerResult(entity_type="AGE", start=14, end=16, score=0.10),    # "45" (overlap)
    ]
    
    print(f"\nOriginal text: '{text}'")
    print(f"Total results: {len(results)}")
    print("\nResults:")
    for r in results:
        print(f"  {r.entity_type}: '{text[r.start:r.end]}' (score: {r.score:.2f})")
    
    # Import the anonymize function
    from process_sample_document import anonymize_with_tags
    
    anonymized = anonymize_with_tags(text, results)
    
    print(f"\nAnonymized: '{anonymized}'")
    print(f"Expected: '<PERSON> is <AGE>'")
    
    # Check if it's correct
    if anonymized == "<PERSON> is <AGE>":
        print("\n✅ Overlap handling PASSED!")
    else:
        print("\n❌ Overlap handling FAILED!")
    
    print("=" * 70)


def test_account_number_overlap():
    """Test specific case from the sample document."""
    print("\nACCOUNT NUMBER OVERLAP TEST")
    print("=" * 70)
    
    text = "Acct 0044-9182-7731"
    
    # Simulate what might be detected
    results = [
        RecognizerResult(entity_type="US_BANK_NUMBER", start=5, end=19, score=0.50),
        RecognizerResult(entity_type="ZIP_CODE", start=5, end=9, score=0.50),  # "0044" might be detected
    ]
    
    print(f"\nOriginal text: '{text}'")
    print("Detected entities:")
    for r in results:
        print(f"  {r.entity_type}: '{text[r.start:r.end]}' (score: {r.score:.2f})")
    
    from process_sample_document import anonymize_with_tags
    
    anonymized = anonymize_with_tags(text, results)
    
    print(f"\nAnonymized: '{anonymized}'")
    print(f"Expected: 'Acct <US_BANK_NUMBER>' (should keep longer match)")
    
    print("=" * 70)


if __name__ == "__main__":
    test_cookie_fix()
    test_overlap_handling()
    test_account_number_overlap()
    print("\n✅ All fix tests completed!")
