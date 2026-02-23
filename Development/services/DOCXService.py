"""
DOCX Service – Handle .docx files by converting to PDF first.

This service converts .docx files to PDF using LibreOffice, then processes
them through the PDFService for precise coordinate-based PII redaction.
This ensures better formatting preservation and more accurate PII masking.
"""
from fastapi import UploadFile
import tempfile
import os
import time
import logging

from services.BaseService import BaseService
from services.LibreOfficeConverter import LibreOfficeConverter, ConversionException
from services.PDFService import PDFService
from utility.exceptions import FileValidationException, DocumentProcessingException

logger = logging.getLogger(__name__)


class DOCXService(BaseService):
    """
    Service for processing .docx files.
    
    Workflow:
    1. Save uploaded .docx file to temp location
    2. Convert .docx to PDF using LibreOffice
    3. Process PDF through PDFService
    4. Return anonymized PDF
    
    Note: Output will be PDF format, not DOCX. This is intentional
    to ensure precise coordinate-based redaction and formatting preservation.
    """
    
    def __init__(self, repository, presidio):
        super().__init__(repository, presidio)
        self.converter = LibreOfficeConverter()
        self.pdf_service = PDFService(repository, presidio)
        self._temp_pdf_path = None  # Cache PDF path to avoid double conversion
    
    @staticmethod
    def _masked_filename(original: str) -> str:
        """Override to return PDF extension since DOCX is converted to PDF."""
        name, _ = os.path.splitext(original)
        return f"{name}_masked.pdf"

    def _validate(self, document: UploadFile) -> None:
        """Validate that the file is a .docx file."""
        fn = (document.filename or "").lower()
        if not fn.endswith(".docx"):
            raise FileValidationException("File must be a .docx file")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        """
        Extract text from .docx file by converting to PDF first.
        Caches the PDF for later use in _build_masked_output().
        
        Args:
            raw: Raw .docx file bytes
            filename: Original filename
            
        Returns:
            Extracted text
        """
        start_time = time.time()
        logger.info(f"[TIMING] Starting DOCX text extraction for {filename} ({len(raw):,} bytes)")
        
        try:
            # Save .docx to temp file
            save_start = time.time()
            with tempfile.NamedTemporaryFile(
                suffix='.docx',
                delete=False
            ) as temp_docx:
                temp_docx.write(raw)
                temp_docx_path = temp_docx.name
            save_time = time.time() - save_start
            logger.info(f"[TIMING] Saved DOCX to temp file in {save_time:.2f}s")
            
            try:
                # Convert to PDF and CACHE the path
                convert_start = time.time()
                logger.info(f"[TIMING] Starting LibreOffice DOCX→PDF conversion...")
                self._temp_pdf_path = self.converter.convert_to_pdf(temp_docx_path)
                convert_time = time.time() - convert_start
                logger.info(f"[TIMING] LibreOffice conversion completed in {convert_time:.2f}s")
                
                # Extract text from cached PDF
                read_start = time.time()
                with open(self._temp_pdf_path, 'rb') as f:
                    pdf_bytes = f.read()
                read_time = time.time() - read_start
                logger.info(f"[TIMING] Read PDF file ({len(pdf_bytes):,} bytes) in {read_time:.2f}s")
                
                extract_start = time.time()
                logger.info(f"[TIMING] Starting PDF text extraction...")
                text = self.pdf_service._extract_text(pdf_bytes, filename)
                extract_time = time.time() - extract_start
                logger.info(f"[TIMING] PDF text extraction completed in {extract_time:.2f}s ({len(text):,} chars)")
                
                total_time = time.time() - start_time
                logger.info(f"[TIMING] Total DOCX text extraction: {total_time:.2f}s (save: {save_time:.2f}s, convert: {convert_time:.2f}s, read: {read_time:.2f}s, extract: {extract_time:.2f}s)")
                
                return text
                
            finally:
                # Clean up temp DOCX (but keep PDF cached)
                if os.path.exists(temp_docx_path):
                    os.unlink(temp_docx_path)
                    
        except ConversionException as e:
            raise DocumentProcessingException(f"DOCX to PDF conversion failed: {e}")
        except Exception as e:
            raise DocumentProcessingException(f"DOCX text extraction failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """
        Build masked output using the CACHED PDF (no re-conversion).
        
        Args:
            raw: Original .docx file bytes (not used, PDF is cached)
            mapping: PII mapping (not used directly)
            anonymized_text: Text with PII replaced by tags
            out_path: Output file path (will be PDF)
        """
        try:
            # Use cached PDF instead of converting again
            if not self._temp_pdf_path or not os.path.exists(self._temp_pdf_path):
                raise DocumentProcessingException("Cached PDF not found - conversion may have failed")
            
            # Read cached PDF bytes
            with open(self._temp_pdf_path, 'rb') as f:
                pdf_bytes = f.read()
            
            # Process through PDF service
            self.pdf_service._build_masked_output(
                pdf_bytes,
                mapping,
                anonymized_text,
                out_path
            )
            
        except Exception as e:
            raise DocumentProcessingException(f"DOCX masking failed: {e}")
        finally:
            # Clean up cached PDF after processing
            if self._temp_pdf_path and os.path.exists(self._temp_pdf_path):
                os.unlink(self._temp_pdf_path)
                self._temp_pdf_path = None
