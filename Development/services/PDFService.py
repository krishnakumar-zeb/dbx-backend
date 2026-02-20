"""PDF Service – mask PII in PDF while preserving formatting using PyMuPDF."""
from fastapi import UploadFile
from typing import Dict, List
import io

from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


class PDFService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(".pdf"):
            raise FileValidationException("File must be a PDF")
        if fitz is None:
            raise DocumentProcessingException(
                "PyMuPDF (fitz) is required for PDF processing. "
                "Install with: pip install PyMuPDF"
            )

    def _extract_text(self, raw: bytes, filename: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(stream=raw, filetype="pdf")
            text_parts = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                if page_text:
                    text_parts.append(page_text)
            doc.close()
            return "\n".join(text_parts).strip()
        except Exception as e:
            raise DocumentProcessingException(f"PDF text extraction failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """
        Redact PII in original PDF while preserving formatting.
        Uses PyMuPDF to find and redact PII text in-place.

        Args:
            raw: Original PDF bytes
            mapping: Not used directly (we use anonymized_text to find replacements)
            anonymized_text: Text with PII replaced by tags
            out_path: Output file path
        """
        try:
            # Open the original PDF
            doc = fitz.open(stream=raw, filetype="pdf")

            # Extract original text to compare with anonymized text
            original_text = self._extract_text(raw, "")

            # Build replacement map by comparing original and anonymized text
            replacements = self._build_replacement_map_from_diff(
                original_text, anonymized_text
            )

            if not replacements:
                # No PII found, just save the original
                doc.save(out_path)
                doc.close()
                return

            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]

                # For each PII value, find and redact it
                for original_value, tag in replacements.items():
                    if not original_value or not original_value.strip():
                        continue

                    # Search for the text on the page
                    text_instances = page.search_for(original_value)

                    # Redact each instance
                    for inst in text_instances:
                        # Add redaction annotation with the tag as replacement text
                        page.add_redact_annot(
                            inst, 
                            text=tag,
                            fill=(1, 1, 1),  # White background
                            text_color=(0, 0, 0)  # Black text
                        )

                # Apply all redactions on this page
                page.apply_redactions()

            # Save the anonymized PDF
            doc.save(out_path)
            doc.close()

        except Exception as e:
            raise DocumentProcessingException(f"PDF redaction failed: {e}")

    def _build_replacement_map_from_diff(
        self, original_text: str, anonymized_text: str
    ) -> Dict[str, str]:
        """
        Compare original and anonymized text to extract {original_value: tag} pairs.

        This method aligns the two texts and identifies where tags replaced original values.

        Args:
            original_text: Original text with PII
            anonymized_text: Text with PII replaced by tags like <PERSON_1>

        Returns:
            Dictionary mapping original PII values to their replacement tags
        """
        import re

        replacements: Dict[str, str] = {}

        # Find all tags in anonymized text
        tag_pattern = re.compile(r"<[A-Z_]+_\d+>")
        tags = list(tag_pattern.finditer(anonymized_text))

        if not tags:
            return replacements

        # Walk through both texts to align and extract replacements
        anon_pos = 0
        orig_pos = 0

        for match in tags:
            tag_start = match.start()
            tag_end = match.end()
            tag = match.group()

            # Characters before this tag should be the same in both texts
            prefix_len = tag_start - anon_pos

            # Skip matching prefix in original text
            orig_pos += prefix_len

            # Move anonymized position past the tag
            anon_pos = tag_end

            # Find the original value that was replaced by this tag
            # Look ahead to find the next common text after the tag
            if anon_pos < len(anonymized_text):
                # Find next tag or end of text
                next_tag = tag_pattern.search(anonymized_text, anon_pos)

                if next_tag:
                    # Text between current tag and next tag
                    next_common = anonymized_text[anon_pos:next_tag.start()]
                else:
                    # Text from current tag to end
                    next_common = anonymized_text[anon_pos:]

                # Find where this common text appears in original
                if next_common and orig_pos < len(original_text):
                    # Look for the common text in original
                    common_idx = original_text.find(next_common, orig_pos)

                    if common_idx != -1:
                        # Extract the original value between current position and common text
                        orig_value = original_text[orig_pos:common_idx]

                        if orig_value.strip():
                            replacements[orig_value] = tag

                        # Move original position past the common text
                        orig_pos = common_idx
                    else:
                        # Common text not found, skip ahead
                        orig_pos += len(tag)
                else:
                    # No more common text, skip
                    orig_pos += len(tag)
            else:
                # Tag is at the end, remaining text is the original value
                if orig_pos < len(original_text):
                    orig_value = original_text[orig_pos:]
                    if orig_value.strip():
                        replacements[orig_value] = tag
                orig_pos = len(original_text)

        return replacements
 