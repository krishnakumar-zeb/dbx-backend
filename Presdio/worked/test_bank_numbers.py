"""Test bank account number detection."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.country_specific.us.us_bank_recognizer import UsBankRecognizer

def test_bank_numbers():
    """Test the bank account numbers from the sample."""
    
    recognizer = UsBankRecognizer()
    
    test_cases = [
        ("Account: 8829-1102-9930", "8829-1102-9930"),
        ("Account: 0044-9182-7731", "0044-9182-7731"),
        ("Account: 9910-0023-4412", "9910-0023-4412"),
        ("Account: 1100-9923-4456", "1100-9923-4456"),
        ("Funding Account: 0044-9182-7731 (Thorne & Associates)", "0044-9182-7731"),
        ("Secondary Account: 1100-9923-4456", "1100-9923-4456"),
        ("Acct 0044-9182-7731", "0044-9182-7731"),
        # Without dashes
        ("Account: 882911029930", "882911029930"),
        ("Account: 004491827731", "004491827731"),
    ]
    
    print("=" * 70)
    print("BANK ACCOUNT NUMBER DETECTION TEST")
    print("=" * 70)
    
    for text, expected in test_cases:
        results = recognizer.analyze(text, ["US_BANK_NUMBER"])
        
        print(f"\nText: '{text}'")
        print(f"Expected: {expected}")
        
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected}' (score: {result.score:.2f})")
        else:
            print("  ✗ NOT DETECTED")
        
        print("-" * 70)
    
    # Check the patterns
    print("\n" + "=" * 70)
    print("CURRENT PATTERNS:")
    print("=" * 70)
    for pattern in recognizer.patterns:
        print(f"  {pattern.name}: {pattern.regex} (score: {pattern.score})")

if __name__ == "__main__":
    test_bank_numbers()
