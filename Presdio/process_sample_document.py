"""
Process sample document with all PII recognizers and generate anonymized output.
This script is ready to process your sample.txt file.
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


def load_sample_text(filename="sample_input.txt"):
    """Load sample text from file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        print("Please create a sample_input.txt file with your test document.")
        return None


def analyze_document(text):
    """Analyze document for all PII entities."""
    
    # Create analyzer engine
    analyzer = AnalyzerEngine()
    
    # Add custom recognizers
    print("Loading custom recognizers...")
    analyzer.registry.add_recognizer(AgeRecognizer())
    analyzer.registry.add_recognizer(GenderRecognizer())
    analyzer.registry.add_recognizer(EthnicityRecognizer(ethnicity_json_path="ethnicities.json"))
    analyzer.registry.add_recognizer(CookieRecognizer())
    analyzer.registry.add_recognizer(ZipCodeRecognizer())
    analyzer.registry.add_recognizer(CertificateRecognizer())
    
    # Define all entities to detect
    entities_to_detect = [
        "PERSON",           # Names
        "AGE",              # Age
        "GENDER",           # Gender
        "ETHNICITY",        # Ethnicity
        "PHONE_NUMBER",     # Phone numbers
        "EMAIL_ADDRESS",    # Email addresses
        "LOCATION",         # Locations (City, State)
        "ZIP_CODE",         # ZIP codes
        "US_SSN",           # Social Security Numbers
        "US_BANK_NUMBER",   # Bank account numbers
        "IP_ADDRESS",       # IP addresses (IPv4 & IPv6)
        "COOKIE",           # Cookies and session IDs
        "CERTIFICATE_NUMBER", # Certificates, licenses, passports
    ]
    
    print(f"Analyzing document for {len(entities_to_detect)} entity types...")
    
    # Analyze the text
    results = analyzer.analyze(
        text=text,
        entities=entities_to_detect,
        language='en'
    )
    
    return results


def display_results(text, results):
    """Display detected PII entities grouped by type."""
    
    print("\n" + "=" * 80)
    print("DETECTED PII ENTITIES")
    print("=" * 80)
    
    if not results:
        print("\nNo PII entities detected.")
        return
    
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
            detected_text = text[result.start:result.end]
            # Truncate long values
            display_text = detected_text if len(detected_text) <= 50 else detected_text[:47] + "..."
            print(f"  - '{display_text}' (score: {result.score:.2f}, position: {result.start}-{result.end})")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: Detected {len(results)} PII entities across {len(results_by_type)} entity types")
    print("=" * 80)


def anonymize_with_tags(text, results):
    """Replace detected PII with entity type tags, handling overlaps."""
    
    # Remove overlapping entities - keep highest score for each position
    def remove_overlaps(results):
        """Remove overlapping results, keeping the one with highest score."""
        if not results:
            return []
        
        # Sort by start position, then by score (descending)
        sorted_results = sorted(results, key=lambda x: (x.start, -x.score))
        
        non_overlapping = []
        for result in sorted_results:
            # Check if this result overlaps with any already accepted result
            overlaps = False
            for accepted in non_overlapping:
                # Check for overlap
                if not (result.end <= accepted.start or result.start >= accepted.end):
                    overlaps = True
                    # If this result has higher score, replace the accepted one
                    if result.score > accepted.score:
                        non_overlapping.remove(accepted)
                        overlaps = False
                    break
            
            if not overlaps:
                non_overlapping.append(result)
        
        return non_overlapping
    
    # Remove overlapping entities
    results_clean = remove_overlaps(results)
    
    # Sort by start position (reverse order for replacement)
    results_sorted = sorted(results_clean, key=lambda x: x.start, reverse=True)
    
    # Replace with tags
    anonymized_text = text
    for result in results_sorted:
        tag = f"<{result.entity_type}>"
        anonymized_text = (
            anonymized_text[:result.start] + 
            tag + 
            anonymized_text[result.end:]
        )
    
    return anonymized_text


def save_results(original_text, anonymized_text, results, output_file="output_anonymized.txt"):
    """Save anonymized text and detection report."""
    
    # Save anonymized text
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANONYMIZED DOCUMENT\n")
        f.write("=" * 80 + "\n\n")
        f.write(anonymized_text)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("DETECTION REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        # Group results by entity type
        results_by_type = {}
        for result in results:
            entity_type = result.entity_type
            if entity_type not in results_by_type:
                results_by_type[entity_type] = []
            results_by_type[entity_type].append(result)
        
        # Write detection report
        for entity_type in sorted(results_by_type.keys()):
            f.write(f"\n{entity_type}:\n")
            for result in results_by_type[entity_type]:
                detected_text = original_text[result.start:result.end]
                f.write(f"  - '{detected_text}' (score: {result.score:.2f})\n")
        
        f.write(f"\n\nTotal: {len(results)} PII entities detected across {len(results_by_type)} types\n")
    
    print(f"\n✅ Results saved to: {output_file}")


def main():
    """Main function to process sample document."""
    
    print("=" * 80)
    print("PII DETECTION AND ANONYMIZATION TOOL")
    print("=" * 80)
    
    # Load sample text
    print("\nLoading sample document...")
    text = load_sample_text("sample_input.txt")
    
    if text is None:
        return
    
    print(f"✅ Loaded document ({len(text)} characters)")
    
    # Analyze document
    results = analyze_document(text)
    
    # Display results
    display_results(text, results)
    
    # Anonymize with tags
    print("\nGenerating anonymized version...")
    anonymized_text = anonymize_with_tags(text, results)
    
    print("\n" + "=" * 80)
    print("ANONYMIZED DOCUMENT (Preview - first 500 characters)")
    print("=" * 80)
    print(anonymized_text[:500])
    if len(anonymized_text) > 500:
        print("...")
    
    # Save results
    save_results(text, anonymized_text, results)
    
    print("\n" + "=" * 80)
    print("✅ PROCESSING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review the output_anonymized.txt file")
    print("2. Check if all PII entities were detected correctly")
    print("3. Adjust recognizer patterns if needed")
    print("4. Test with official company documents")


if __name__ == "__main__":
    main()
