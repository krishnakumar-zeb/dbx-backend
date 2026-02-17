"""
Test the full documentation text to see what's detected
"""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    AgeRecognizer,
    CertificateRecognizer,
    CookieRecognizer,
    EthnicityRecognizer,
    GenderRecognizer,
    ZipCodeRecognizer,
)

FULL_TEXT = """Sarah Johnson, a 34-year-old female software engineer, recently relocated to Seattle, Washington. She can be reached at sarah.johnson@techcorp.com or by phone at (206) 555-0147. Her new address is 1234 Pine Street, Seattle, WA 98101. Sarah's Social Security Number is 123-45-6789, and her primary bank account number is 9876-5432-1098. Dr. Michael Chen, age 45, is an Asian-American physician practicing in New York City. His office is located at 567 Madison Avenue, New York, NY 10022. For appointments, patients can call (212) 555-0198 or email dr.chen@healthclinic.org. Dr. Chen's medical license number is MED-2024-NY-8765, and his passport number is A12345678. He recently accessed the patient portal using session ID a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 from IP address 192.168.1.100."""

# Setup analyzer
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(AgeRecognizer())
analyzer.registry.add_recognizer(GenderRecognizer())
analyzer.registry.add_recognizer(EthnicityRecognizer(ethnicity_json_path="ethnicities.json"))
analyzer.registry.add_recognizer(CookieRecognizer())
analyzer.registry.add_recognizer(ZipCodeRecognizer())
analyzer.registry.add_recognizer(CertificateRecognizer())

entities_to_detect = [
    "PERSON", "AGE", "GENDER", "ETHNICITY",
    "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "ZIP_CODE",
    "US_SSN", "US_BANK_NUMBER", "IP_ADDRESS",
    "COOKIE", "CERTIFICATE_NUMBER"
]

# Analyze
results = analyzer.analyze(
    text=FULL_TEXT,
    entities=entities_to_detect,
    language='en'
)

print(f"Total detections: {len(results)}\n")

# Group by entity type
from collections import defaultdict
by_type = defaultdict(list)
for r in results:
    by_type[r.entity_type].append((FULL_TEXT[r.start:r.end], r.score))

# Print results
for entity_type in sorted(by_type.keys()):
    print(f"\n{entity_type} ({len(by_type[entity_type])} instances):")
    for text, score in by_type[entity_type]:
        print(f"  - '{text}' (score: {score:.2f})")

# Check specifically for AGE and SSN
print("\n" + "=" * 60)
print("SPECIFIC CHECKS:")
print("=" * 60)

# Check for "age 45"
if "age 45" in FULL_TEXT:
    print("\n✓ Text contains 'age 45'")
    age_results = [r for r in results if r.entity_type == "AGE"]
    if age_results:
        print(f"  AGE detections: {len(age_results)}")
        for r in age_results:
            print(f"    - '{FULL_TEXT[r.start:r.end]}'")
    else:
        print("  ❌ But AGE was not detected!")

# Check for SSN
if "123-45-6789" in FULL_TEXT:
    print("\n✓ Text contains '123-45-6789'")
    ssn_results = [r for r in results if r.entity_type == "US_SSN"]
    if ssn_results:
        print(f"  US_SSN detections: {len(ssn_results)}")
        for r in ssn_results:
            print(f"    - '{FULL_TEXT[r.start:r.end]}'")
    else:
        print("  ❌ But US_SSN was not detected!")
        print("  Reason: 123-45-6789 is a known invalid/test SSN")
