"""Test script for Certificate recognizer."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.generic.certificate_recognizer import CertificateRecognizer

def test_certificate_recognizer():
    """Test the Certificate recognizer with various formats."""
    
    recognizer = CertificateRecognizer()
    
    test_cases = [
        # Passport formats
        ("Passport: A-99823411", "Passport with letter prefix"),
        ("Passport Number: M12345678", "Diplomatic passport"),
        ("Passport: 123456789", "Regular 9-digit passport"),
        
        # Pilot's License
        ("Pilot License: FTL-990234-B", "Pilot license"),
        
        # Driver's License
        ("Driver's License: WDL-772-BBN-01", "Driver's license"),
        
        # Global Entry
        ("Global Entry: 982230415", "Global Entry certificate"),
        
        # Medical/Policy IDs
        ("Medical ID: MED-9920-X", "Medical ID"),
        ("Policy Number: LP-88902-11", "Life insurance policy"),
        ("Policy: POL-9910234-X", "Auto insurance policy"),
        ("Group Policy: GRP-44102", "Group policy"),
        
        # License Plate
        ("License Plate: WA-882-BBN", "License plate"),
        
        # Certificate Serial
        ("Certificate Serial: 77-88-99-AA-BB-CC-00-11", "Certificate serial"),
        
        # Should NOT detect
        ("The year 2020", "Should not detect year"),
        ("Page 123", "Should not detect page number"),
    ]
    
    print("=" * 70)
    print("CERTIFICATE RECOGNIZER TEST")
    print("=" * 70)
    
    for text, description in test_cases:
        results = recognizer.analyze(text, ["CERTIFICATE_NUMBER"])
        
        print(f"\nText: '{text}'")
        print(f"Description: {description}")
        
        if results:
            for result in results:
                detected = text[result.start:result.end]
                print(f"  ✓ Detected: '{detected}' (score: {result.score:.2f})")
        else:
            print("  ✗ No certificate detected")
        
        print("-" * 70)
    
    print("\n✅ Certificate Recognizer test completed!")

if __name__ == "__main__":
    test_certificate_recognizer()
