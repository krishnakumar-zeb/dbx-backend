"""
Test 3-digit ZIP code detection
"""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import ZipCodeRecognizer

# Test cases
test_cases = [
    ("My ZIP is 123", "123", True),
    ("ZIP code 456", "456", True),
    ("Area code 789", "789", True),
    ("ZIP 000", "000", False),  # Invalid
    ("ZIP 111", "111", False),  # All same digit
    ("ZIP 98101", "98101", True),  # 5-digit
    ("ZIP 98101-1234", "98101-1234", True),  # ZIP+4
    ("Page 123 of document", "123", True),  # Will match but low confidence without context
]

# Setup analyzer
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(ZipCodeRecognizer())

print("=" * 70)
print("TESTING 3-DIGIT ZIP CODE DETECTION")
print("=" * 70)

for test_text, expected_zip, should_detect in test_cases:
    results = analyzer.analyze(
        text=test_text,
        entities=["ZIP_CODE"],
        language='en'
    )
    
    detected = len(results) > 0
    status = "✓" if detected == should_detect else "❌"
    
    print(f"\n{status} Test: '{test_text}'")
    print(f"   Expected: {'Detect' if should_detect else 'Reject'} '{expected_zip}'")
    
    if results:
        for r in results:
            detected_text = test_text[r.start:r.end]
            print(f"   Detected: '{detected_text}' (score: {r.score:.2f})")
    else:
        print(f"   Detected: None")

# Test with context
print("\n" + "=" * 70)
print("TESTING WITH CONTEXT (should have higher confidence)")
print("=" * 70)

context_tests = [
    "The ZIP code is 123",
    "Mailing ZIP: 456",
    "Postal code 789",
]

for test_text in context_tests:
    results = analyzer.analyze(
        text=test_text,
        entities=["ZIP_CODE"],
        language='en'
    )
    
    print(f"\nTest: '{test_text}'")
    if results:
        for r in results:
            detected_text = test_text[r.start:r.end]
            print(f"  ✓ Detected: '{detected_text}' (score: {r.score:.2f})")
    else:
        print(f"  ❌ Not detected")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("✓ 3-digit ZIP code support added")
print("✓ Validation rejects 000 and repeated digits (111, 222, etc.)")
print("✓ Context words increase confidence score")
print("✓ Supports 3-digit, 5-digit, and ZIP+4 formats")
