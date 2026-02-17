"""Quick test of certificate recognizer on sample document."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers.generic.certificate_recognizer import CertificateRecognizer

# Load sample text
with open('sample_input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Create analyzer
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(CertificateRecognizer())

print("Analyzing sample document for certificates...")
results = analyzer.analyze(text, ["CERTIFICATE_NUMBER"], language='en')

print(f"\n✅ Found {len(results)} certificate numbers:\n")

# Group by unique values
unique_certs = {}
for result in results:
    cert = text[result.start:result.end]
    if cert not in unique_certs:
        unique_certs[cert] = []
    unique_certs[cert].append(result.score)

# Display
for cert, scores in sorted(unique_certs.items(), key=lambda x: max(x[1]), reverse=True):
    max_score = max(scores)
    count = len(scores)
    print(f"  {cert:<30} (score: {max_score:.2f}, occurrences: {count})")

print(f"\n✅ Total unique certificates: {len(unique_certs)}")
