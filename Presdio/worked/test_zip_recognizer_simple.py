"""Simple test script to verify ZIP code recognizer works."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.generic.zip_code_recognizer import ZipCodeRecognizer

def test_zip_recognizer():
    """Test the ZIP code recognizer with various inputs."""
    
    recognizer = ZipCodeRecognizer()
    
    test_cases = [
        ("My ZIP is 90210", "90210"),
        ("Send to 10001-5555", "10001-5555"),
        ("From 90210 to 10001", "90210, 10001"),
        ("ZIP code: 12345", "12345"),
        ("Invalid: 00000", "None (all zeros)"),
        ("Invalid: 11111", "None (all same)"),
        ("Invalid: 00123", "None (starts with 00)"),
    ]
    
    print("=" * 60)
    print("ZIP CODE RECOGNIZER TEST")
    print("=" * 60)
    
    for text, expected in test_cases:
        results = recognizer.analyze(text, ["ZIP_CODE"])
        
        print(f"\nText: '{text}'")
        print(f"Expected: {expected}")
        
        if results:
            detected = []
            for result in results:
                zip_code = text[result.start:result.end]
                detected.append(f"{zip_code} (score: {result.score:.2f})")
            print(f"Detected: {', '.join(detected)}")
        else:
            print("Detected: None")
        
        print("-" * 60)
    
    print("\n✅ ZIP Code Recognizer test completed!")

if __name__ == "__main__":
    test_zip_recognizer()
