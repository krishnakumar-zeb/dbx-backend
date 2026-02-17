"""
PDF PII Detection and Anonymization Tool
Extracts text from PDF, detects PII, and outputs anonymized text.
"""

import sys
import os
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


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using multiple methods."""
    
    print(f"Extracting text from: {pdf_path}")
    
    # Try pdfplumber first (better text extraction)
    try:
        import pdfplumber
        
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n\n--- Page {i} ---\n\n"
                    text += page_text
        
        if text.strip():
            print(f"✅ Extracted {len(text)} characters using pdfplumber")
            return text
    except ImportError:
        print("⚠️  pdfplumber not installed, trying PyPDF2...")
    except Exception as e:
        print(f"⚠️  pdfplumber failed: {e}, trying PyPDF2...")
    
    # Fallback to PyPDF2
    try:
        import PyPDF2
        
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n\n--- Page {i} ---\n\n"
                    text += page_text
        
        if text.strip():
            print(f"✅ Extracted {len(text)} characters using PyPDF2")
            return text
    except ImportError:
        print("❌ PyPDF2 not installed")
        print("\nPlease install one of the following:")
        print("  pip install pdfplumber")
        print("  pip install PyPDF2")
        return None
    except Exception as e:
        print(f"❌ PyPDF2 failed: {e}")
        return None
    
    print("❌ Failed to extract text from PDF")
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
        "PERSON",              # Names
        "AGE",                 # Age
        "GENDER",              # Gender
        "ETHNICITY",           # Ethnicity
        "PHONE_NUMBER",        # Phone numbers
        "EMAIL_ADDRESS",       # Email addresses
        "LOCATION",            # Locations (City, State)
        "ZIP_CODE",            # ZIP codes
        "US_SSN",              # Social Security Numbers
        "US_BANK_NUMBER",      # Bank account numbers
        "IP_ADDRESS",          # IP addresses (IPv4 & IPv6)
        "COOKIE",              # Cookies and session IDs
        "CERTIFICATE_NUMBER",  # Certificates, licenses, passports
    ]
    
    print(f"Analyzing document for {len(entities_to_detect)} entity types...")
    
    # Analyze the text
    results = analyzer.analyze(
        text=text,
        entities=entities_to_detect,
        language='en'
    )
    
    return results


def anonymize_with_tags(text, results):
    """Replace detected PII with entity type tags, handling overlaps."""
    
    # Remove overlapping entities - keep highest score
    def remove_overlaps(results):
        if not results:
            return []
        
        sorted_results = sorted(results, key=lambda x: (x.start, -x.score))
        non_overlapping = []
        
        for result in sorted_results:
            overlaps = False
            for accepted in non_overlapping:
                if not (result.end <= accepted.start or result.start >= accepted.end):
                    overlaps = True
                    if result.score > accepted.score:
                        non_overlapping.remove(accepted)
                        overlaps = False
                    break
            
            if not overlaps:
                non_overlapping.append(result)
        
        return non_overlapping
    
    # Remove overlaps and sort
    results_clean = remove_overlaps(results)
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
    
    return anonymized_text, results_clean


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
        print(f"\n{entity_type}: {len(results_by_type[entity_type])} instances")
        # Show first 3 examples
        for i, result in enumerate(results_by_type[entity_type][:3], 1):
            detected_text = text[result.start:result.end]
            display_text = detected_text if len(detected_text) <= 50 else detected_text[:47] + "..."
            print(f"  {i}. '{display_text}' (score: {result.score:.2f})")
        
        if len(results_by_type[entity_type]) > 3:
            print(f"  ... and {len(results_by_type[entity_type]) - 3} more")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: Detected {len(results)} PII entities across {len(results_by_type)} entity types")
    print("=" * 80)


def save_results(original_text, anonymized_text, results, output_file, input_file):
    """Save input text, anonymized text, and detection report in separate files."""
    
    # Save original extracted text
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(original_text)
    print(f"\n✅ Input text saved to: {input_file}")
    
    # Save anonymized text with detection report
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
            f.write(f"\n{entity_type} ({len(results_by_type[entity_type])} instances):\n")
            for result in results_by_type[entity_type]:
                detected_text = original_text[result.start:result.end]
                f.write(f"  - '{detected_text}' (score: {result.score:.2f})\n")
        
        f.write(f"\n\nTotal: {len(results)} PII entities detected across {len(results_by_type)} types\n")
    
    print(f"✅ Anonymized output saved to: {output_file}")


def process_pdf(pdf_path, output_file=None, input_file=None):
    """Main function to process PDF document."""
    
    print("=" * 80)
    print("PDF PII DETECTION AND ANONYMIZATION TOOL")
    print("=" * 80)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"\n❌ Error: File not found: {pdf_path}")
        return
    
    # Generate default filenames if not provided
    base_name = os.path.splitext(pdf_path)[0]
    if output_file is None:
        output_file = f"{base_name}_anonymized.txt"
    if input_file is None:
        input_file = f"{base_name}_input.txt"
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if not text or not text.strip():
        print("\n❌ Error: No text could be extracted from PDF")
        print("The PDF might be:")
        print("  - Image-based (scanned document)")
        print("  - Encrypted or password-protected")
        print("  - Corrupted")
        return
    
    print(f"✅ Loaded document ({len(text)} characters)")
    
    # Analyze document
    results = analyze_document(text)
    
    # Display results
    display_results(text, results)
    
    # Anonymize with tags
    print("\nGenerating anonymized version...")
    anonymized_text, results_clean = anonymize_with_tags(text, results)
    
    print("\n" + "=" * 80)
    print("ANONYMIZED DOCUMENT (Preview - first 500 characters)")
    print("=" * 80)
    print(anonymized_text[:500])
    if len(anonymized_text) > 500:
        print("...")
    
    # Save results
    save_results(text, anonymized_text, results_clean, output_file, input_file)
    
    print("\n" + "=" * 80)
    print("✅ PROCESSING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nOutput files:")
    print(f"  - Input text: {input_file}")
    print(f"  - Anonymized text: {output_file}")
    print("\nNext steps:")
    print("1. Review both files for comparison")
    print("2. Check if all PII entities were detected correctly")
    print("3. Process additional documents as needed")


def main():
    """Main entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extract text from PDF and anonymize PII entities'
    )
    parser.add_argument(
        'pdf_file',
        help='Path to PDF file to process'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path for anonymized text (default: input_filename_anonymized.txt)',
        default=None
    )
    parser.add_argument(
        '-i', '--input-output',
        help='Output file path for extracted input text (default: input_filename_input.txt)',
        default=None
    )
    
    args = parser.parse_args()
    
    process_pdf(args.pdf_file, args.output, args.input_output)


if __name__ == "__main__":
    # Check if running with arguments
    if len(sys.argv) > 1:
        main()
    else:
        # Interactive mode
        print("=" * 80)
        print("PDF PII DETECTION AND ANONYMIZATION TOOL")
        print("=" * 80)
        print("\nUsage:")
        print("  python process_pdf_document.py <pdf_file> [-o output_file] [-i input_file]")
        print("\nExample:")
        print("  python process_pdf_document.py document.pdf")
        print("  python process_pdf_document.py document.pdf -o anonymized.txt -i extracted.txt")
        print("\nOr enter PDF file path now:")
        
        pdf_path = input("\nPDF file path: ").strip().strip('"').strip("'")
        
        if pdf_path and os.path.exists(pdf_path):
            process_pdf(pdf_path)
        elif pdf_path:
            print(f"\n❌ Error: File not found: {pdf_path}")
        else:
            print("\n❌ No file path provided")
