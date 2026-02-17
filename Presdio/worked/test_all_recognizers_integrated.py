"""Comprehensive integration test for all PII recognizers."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    AgeRecognizer,
    CookieRecognizer,
    EmailRecognizer,
    EthnicityRecognizer,
    GenderRecognizer,
    IpRecognizer,
    PhoneRecognizer,
    UsSsnRecognizer,
    UsBankRecognizer,
    ZipCodeRecognizer,
)


def test_comprehensive_pii_detection():
    """Test all recognizers together on a sample document."""
    
    # Create analyzer engine
    analyzer = AnalyzerEngine()
    
    # Add custom recognizers
    analyzer.registry.add_recognizer(AgeRecognizer())
    analyzer.registry.add_recognizer(GenderRecognizer())
    analyzer.registry.add_recognizer(EthnicityRecognizer(ethnicity_json_path="ethnicities.json"))
    analyzer.registry.add_recognizer(CookieRecognizer())
    analyzer.registry.add_recognizer(ZipCodeRecognizer())
    
    # Sample text with multiple PII types
    sample_text = """
    Patient Information:
    Name: John Smith
    Age: 45 years old
    Gender: male
    Ethnicity: African American
    
    Contact Details:
    Email: john.smith@example.com
    Phone: (555) 123-4567
    Address: 123 Main Street, New York, NY 10001
    ZIP Code: 10001-5555
    
    Financial Information:
    SSN: 123-45-6789
    Bank Account: 1234567890
    
    Technical Information:
    IP Address: 192.168.1.100
    IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    Session ID: abc123def456ghi789jkl012mno345pqr678
    Cookie: session_id=xyz789abc456def123ghi789jkl012mno345
    """
    
    # Analyze the text
    entities_to_detect = [
        "PERSON", "AGE", "GENDER", "ETHNICITY",
        "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION",
        "ZIP_CODE", "US_SSN", "US_BANK_NUMBER",
        "IP_ADDRESS", "COOKIE"
    ]
    
    print("=" * 80)
    print("COMPREHENSIVE PII DETECTION TEST")
    print("=" * 80)
    print(f"\nSample Text:\n{sample_text}")
    print("\n" + "=" * 80)
    print("DETECTED PII ENTITIES:")
    print("=" * 80)
    
    results = analyzer.analyze(
        text=sample_text,
        entities=entities_to_detect,
        language='en'
    )
    
    # Group results by entity type
    results_by_type = {}
    for result in results:
        entity_type = result.entity_type
        if entity_type not in results_by_type:
            results_by_type[entity_type] = []
        results_by_type[entity_type].append(result)
    
    # Display results
    for entity_type in sorted(results_by_type.keys()):
        print(f"\n{entity_type}:")
        for result in results_by_type[entity_type]:
            detected_text = sample_text[result.start:result.end]
            print(f"  - '{detected_text}' (score: {result.score:.2f}, pos: {result.start}-{result.end})")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: Detected {len(results)} PII entities across {len(results_by_type)} entity types")
    print("=" * 80)
    
    return results


def test_anonymization_tags():
    """Test that entities can be replaced with tags."""
    
    print("\n\n" + "=" * 80)
    print("ANONYMIZATION WITH TAGS TEST")
    print("=" * 80)
    
    # Create analyzer
    analyzer = AnalyzerEngine()
    analyzer.registry.add_recognizer(AgeRecognizer())
    analyzer.registry.add_recognizer(GenderRecognizer())
    analyzer.registry.add_recognizer(EthnicityRecognizer())
    analyzer.registry.add_recognizer(CookieRecognizer())
    analyzer.registry.add_recognizer(ZipCodeRecognizer())
    
    # Simple test text
    test_text = "John is 30 years old, male, Hispanic, lives in 90210, email: john@test.com"
    
    print(f"\nOriginal Text:\n{test_text}")
    
    # Analyze
    results = analyzer.analyze(
        text=test_text,
        entities=["PERSON", "AGE", "GENDER", "ETHNICITY", "ZIP_CODE", "EMAIL_ADDRESS"],
        language='en'
    )
    
    # Sort results by start position (reverse order for replacement)
    results_sorted = sorted(results, key=lambda x: x.start, reverse=True)
    
    # Replace with tags
    anonymized_text = test_text
    for result in results_sorted:
        tag = f"<{result.entity_type}>"
        anonymized_text = (
            anonymized_text[:result.start] + 
            tag + 
            anonymized_text[result.end:]
        )
    
    print(f"\nAnonymized Text:\n{anonymized_text}")
    
    print("\n" + "=" * 80)
    print("✅ Anonymization test completed!")
    print("=" * 80)


if __name__ == "__main__":
    # Run comprehensive detection test
    results = test_comprehensive_pii_detection()
    
    # Run anonymization test
    test_anonymization_tags()
    
    print("\n\n" + "=" * 80)
    print("✅ ALL INTEGRATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
