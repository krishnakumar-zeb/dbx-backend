"""PDF Service – mask PII in PDF while preserving formatting using PyMuPDF."""
from fastapi import UploadFile
from typing import Dict, List
import io
import re
import time
import logging
from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException

logger = logging.getLogger(__name__)

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
        start_time = time.time()
        logger.info(f"[TIMING] Starting PDF text extraction for {filename} ({len(raw):,} bytes)")
        
        try:
            open_start = time.time()
            doc = fitz.open(stream=raw, filetype="pdf")
            open_time = time.time() - open_start
            page_count = len(doc)
            logger.info(f"[TIMING] Opened PDF in {open_time:.2f}s ({page_count} pages)")
            
            text_parts = []
            extract_start = time.time()
            for page_num in range(page_count):
                page = doc[page_num]
                page_text = page.get_text()
                if page_text:
                    text_parts.append(page_text)
                
                # Log progress every 10 pages for large documents
                if (page_num + 1) % 10 == 0:
                    elapsed = time.time() - extract_start
                    logger.info(f"[TIMING] Extracted {page_num + 1}/{page_count} pages in {elapsed:.2f}s")
            
            extract_time = time.time() - extract_start
            logger.info(f"[TIMING] Extracted text from all {page_count} pages in {extract_time:.2f}s")
            
            doc.close()
            result = "\n".join(text_parts).strip()
            
            total_time = time.time() - start_time
            logger.info(f"[TIMING] Total PDF text extraction: {total_time:.2f}s ({len(result):,} chars, {len(result)/total_time:.0f} chars/sec)")
            
            return result
        except Exception as e:
            raise DocumentProcessingException(f"PDF text extraction failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """
        Redact PII in original PDF while preserving formatting.
        Uses PyMuPDF's get_text("dict") for efficient text position lookup.

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

            # Process each page using efficient dictionary-based approach
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get text with position information
                text_dict = page.get_text("dict")
                
                # Find positions for all PII values on this page
                pii_positions = self._find_text_positions(text_dict, replacements)
                
                # Add redaction annotations for all found PII
                for pii_value, tag, bbox in pii_positions:
                    page.add_redact_annot(
                        bbox,
                        text=tag,
                        fill=None,  # No fill - transparent background
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

                        # CRITICAL: Only add if value is non-empty and has actual content
                        if orig_value and orig_value.strip() and len(orig_value.strip()) > 0:
                            # Additional validation: value should not be just whitespace or newlines
                            if not orig_value.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', ''):
                                # Skip whitespace-only values
                                pass
                            else:
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
                    # CRITICAL: Only add if value is non-empty and has actual content
                    if orig_value and orig_value.strip() and len(orig_value.strip()) > 0:
                        if not orig_value.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', ''):
                            # Skip whitespace-only values
                            pass
                        else:
                            replacements[orig_value] = tag
                orig_pos = len(original_text)

        return replacements

    def _find_text_positions(
        self, text_dict: Dict, replacements: Dict[str, str]
    ) -> List[tuple]:
        """
        Find precise bounding boxes for all PII values in the page.
        
        Uses character-level precision to avoid removing entire lines.
        
        Args:
            text_dict: Page text dictionary from get_text("dict")
            replacements: Dictionary mapping PII values to their tags
            
        Returns:
            List of tuples: (pii_value, tag, bbox)
        """
        positions = []
        
        # Build a list of all text spans with their positions
        text_spans = []
        
        for block in text_dict.get("blocks", []):
            if block.get("type") != 0:  # Skip non-text blocks
                continue
                
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    bbox = span.get("bbox")
                    font_size = span.get("size", 12)
                    
                    if text and bbox:
                        text_spans.append({
                            "text": text,
                            "bbox": fitz.Rect(bbox),
                            "font_size": font_size
                        })
        
        # For each PII value, find matching spans with precise bbox calculation
        for pii_value, tag in replacements.items():
            # CRITICAL: Validate PII value before processing
            if not pii_value or not pii_value.strip():
                continue
            
            # Skip if value is only whitespace/newlines
            cleaned_value = pii_value.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
            if not cleaned_value:
                continue
            
            pii_len = len(pii_value)
            found = False  # Track if we found this PII in the PDF
            
            # Search through spans
            for i, span in enumerate(text_spans):
                span_text = span["text"]
                
                # Check if PII value is in this span
                if pii_value in span_text:
                    # Calculate precise bbox for just the PII text within the span
                    pii_start_idx = span_text.index(pii_value)
                    pii_end_idx = pii_start_idx + pii_len
                    
                    # Calculate character width (approximate)
                    span_bbox = span["bbox"]
                    span_width = span_bbox.width
                    char_width = span_width / len(span_text) if len(span_text) > 0 else span_width
                    
                    # Calculate precise bbox for the PII text only
                    pii_x0 = span_bbox.x0 + (pii_start_idx * char_width)
                    pii_x1 = span_bbox.x0 + (pii_end_idx * char_width)
                    
                    # Use the same y-coordinates as the span (height)
                    precise_bbox = fitz.Rect(pii_x0, span_bbox.y0, pii_x1, span_bbox.y1)
                    
                    positions.append((pii_value, tag, precise_bbox))
                    found = True
                    break  # Found it, move to next PII value
                    
                elif pii_value.startswith(span_text):
                    # PII might span multiple spans - build it carefully
                    combined_text = span_text
                    span_list = [span]
                    
                    # Look ahead to next spans
                    for j in range(i + 1, min(i + 10, len(text_spans))):
                        next_span = text_spans[j]
                        combined_text += next_span["text"]
                        span_list.append(next_span)
                        
                        if pii_value in combined_text:
                            # Found the complete PII across multiple spans
                            # Calculate minimal bbox that covers only the PII text
                            
                            # Start from first span
                            first_bbox = span_list[0]["bbox"]
                            last_bbox = span_list[-1]["bbox"]
                            
                            # Calculate how much of the last span is used
                            pii_start_in_combined = combined_text.index(pii_value)
                            pii_end_in_combined = pii_start_in_combined + pii_len
                            
                            # Calculate x0 from first span
                            first_span_text = span_list[0]["text"]
                            first_char_width = first_bbox.width / len(first_span_text) if len(first_span_text) > 0 else first_bbox.width
                            pii_x0 = first_bbox.x0 + (pii_start_in_combined * first_char_width)
                            
                            # Calculate x1 from last span
                            chars_in_last_span = pii_end_in_combined - sum(len(s["text"]) for s in span_list[:-1])
                            last_span_text = span_list[-1]["text"]
                            last_char_width = last_bbox.width / len(last_span_text) if len(last_span_text) > 0 else last_bbox.width
                            pii_x1 = last_bbox.x0 + (chars_in_last_span * last_char_width)
                            
                            # Use min/max y-coordinates to cover all spans
                            pii_y0 = min(s["bbox"].y0 for s in span_list)
                            pii_y1 = max(s["bbox"].y1 for s in span_list)
                            
                            precise_bbox = fitz.Rect(pii_x0, pii_y0, pii_x1, pii_y1)
                            positions.append((pii_value, tag, precise_bbox))
                            found = True
                            break
                        
                        if len(combined_text) > pii_len + 10:
                            # Gone too far, stop looking
                            break
                
                if found:
                    break  # Found this PII, move to next one
        
        return positions
 