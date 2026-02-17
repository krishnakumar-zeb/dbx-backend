"""
PDF PII Detection and Anonymization with Formatting Preservation
Uses PyMuPDF (fitz) to preserve original document formatting.
"""


from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    AgeRecognizer,
    CertificateRecognizer,
    CookieRecognizer,
    EthnicityRecognizer,
    GenderRecognizer,
    ZipCodeRecognizer,
)
import sys
import os
import fitz  
sys.path.insert(0, 'presidio-main/presidio-analyzer')


def setup_analyzer():
    """Initialize analyzer with custom recognizers."""
    analyzer = AnalyzerEngine()
    
    # Add custom recognizers
    analyzer.registry.add_recognizer(AgeRecognizer())
    analyzer.registry.add_recognizer(GenderRecognizer())
    analyzer.registry.add_recognizer(EthnicityRecognizer(ethnicity_json_path="ethnicities.json"))
    analyzer.registry.add_recognizer(CookieRecognizer())
    analyzer.registry.add_recognizer(ZipCodeRecognizer())
    analyzer.registry.add_recognizer(CertificateRecognizer())
    
    return analyzer


# def filter_results(results, text):
#     """Filter out false positive detections."""
#     filtered_results = []
#     location_false_positives = ['q1', 'q2', 'q3', 'q4', 'q5']
    
#     for result in results:
#         if result.entity_type == "LOCATION":
#             detected_text = text[result.start:result.end].lower()
#             if detected_text in location_false_positives:
#                 continue
#         filtered_results.append(result)
    
#     return filtered_results


def anonymize_pdf_with_formatting(input_pdf_path, output_pdf_path):
    """
    Anonymize PDF while preserving formatting using PyMuPDF.
    Replaces PII text with entity tags in the original document.
    """
    
    
    # Open PDF
    doc = fitz.open(input_pdf_path)
    
    # Setup analyzer
    analyzer = setup_analyzer()
    
    entities_to_detect = [
        "PERSON", "AGE", "GENDER", "ETHNICITY",
        "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "ZIP_CODE",
        "US_SSN", "US_BANK_NUMBER", "IP_ADDRESS",
        "COOKIE", "CERTIFICATE_NUMBER"
    ]
    
    total_redactions = 0
    
    # Process each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract text with position information
        text = page.get_text()
        
        if not text.strip():
            continue
        
        print(f"\nProcessing page {page_num + 1}...")
        
        # Analyze text for PII
        results = analyzer.analyze(
            text=text,
            entities=entities_to_detect,
            language='en'
        )
        
        # Filter false positives
        results = filter_results(results, text)
        
        if not results:
            print(f"  No PII found on page {page_num + 1}")
            continue
        
        print(f"  Found {len(results)} PII entities on page {page_num + 1}")
        
        # Group results by entity type for reporting
        entity_counts = {}
        for result in results:
            entity_counts[result.entity_type] = entity_counts.get(result.entity_type, 0) + 1
        
        for entity_type, count in entity_counts.items():
            print(f"    - {entity_type}: {count}")
        
        # Redact PII by searching and replacing text
        for result in results:
            pii_text = text[result.start:result.end]
            replacement_tag = f"<{result.entity_type}>"
            
            # Search for text instances on the page
            text_instances = page.search_for(pii_text)
            
            for inst in text_instances:
                # Add redaction annotation
                page.add_redact_annot(inst, text=replacement_tag, fill=(1, 1, 1))
        
        # Apply all redactions on this page
        page.apply_redactions()
        total_redactions += len(results)
    
    # Save anonymized PDF
    doc.save(output_pdf_path)
    doc.close()
    
    print("\n" + "=" * 80)
    print("✅ PROCESSING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nTotal PII entities anonymized: {total_redactions}")
    print(f"Output saved to: {output_pdf_path}")
    
    return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Anonymize PDF while preserving formatting'
    )
    parser.add_argument(
        'input_pdf',
        help='Path to input PDF file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output PDF path (default: input_filename_anonymized.pdf)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_pdf):
        print(f"❌ Error: File not found: {args.input_pdf}")
        return
    
    # Generate output filename
    if args.output is None:
        base_name = os.path.splitext(args.input_pdf)[0]
        args.output = f"{base_name}_anonymized.pdf"
    
    # Process PDF
    anonymize_pdf_with_formatting(args.input_pdf, args.output)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        print("=" * 80)
        print("PDF PII ANONYMIZATION WITH FORMATTING PRESERVATION")
        print("=" * 80)
        print("\nUsage:")
        print("  python process_pdf_with_formatting.py <input.pdf> [-o output.pdf]")
        print("\nExample:")
        print("  python process_pdf_with_formatting.py document.pdf")
        print("  python process_pdf_with_formatting.py document.pdf -o anonymized.pdf")
