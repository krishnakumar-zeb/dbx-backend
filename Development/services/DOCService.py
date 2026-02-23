"""
DOC Service – Handle legacy .doc files by converting to PDF first.

This service converts .doc files to PDF using LibreOffice, then processes
them through the PDFService for precise coordinate-based PII redaction.
"""
from fastapi import UploadFile
import tempfile
import os

from services.BaseService import BaseService
from services.LibreOfficeConverter import LibreOfficeConverter, ConversionException
from services.PDFService import PDFService
from utility.exceptions import FileValidationException, DocumentProcessingException


class DOCService(BaseService):
    """
    Service for processing legacy .doc files.
    
    Workflow:
    1. Save uploaded .doc file to temp location
    2. Convert .doc to PDF using LibreOffice
    3. Process PDF through PDFService
    4. Return anonymized PDF
    """
    
    def __init__(self, repository, presidio):
        super().__init__(repository, presidio)
        self.converter = LibreOfficeConverter()
        self.pdf_service = PDFService(repository, presidio)
        self._temp_pdf_path = None  # Cache PDF path to avoid double conversion
    
    @staticmethod
    def _masked_filename(original: str) -> str:
        """Override to return PDF extension since DOC is converted to PDF."""
        name, _ = os.path.splitext(original)
        return f"{name}_masked.pdf"
    
    def _validate(self, document: UploadFile) -> None:
        """Validate that the file is a .doc file."""
        fn = (document.filename or "").lower()
        if not fn.endswith(".doc"):
            raise FileValidationException("File must be a .doc file")
    
    def _extract_text(self, raw: bytes, filename: str) -> str:
        """
        Extract text from .doc file by converting to PDF first.
        Caches the PDF for later use in _build_masked_output().
        
        Args:
            raw: Raw .doc file bytes
            filename: Original filename
            
        Returns:
            Extracted text
        """
        try:
            # Save .doc to temp file
            with tempfile.NamedTemporaryFile(
                suffix='.doc',
                delete=False
            ) as temp_doc:
                temp_doc.write(raw)
                temp_doc_path = temp_doc.name
            
            try:
                # Convert to PDF and CACHE the path
                self._temp_pdf_path = self.converter.convert_to_pdf(temp_doc_path)
                
                # Extract text from cached PDF
                with open(self._temp_pdf_path, 'rb') as f:
                    pdf_bytes = f.read()
                
                text = self.pdf_service._extract_text(pdf_bytes, filename)
                
                return text
                
            finally:
                # Clean up temp DOC (but keep PDF cached)
                if os.path.exists(temp_doc_path):
                    os.unlink(temp_doc_path)
                    
        except ConversionException as e:
            raise DocumentProcessingException(f"DOC to PDF conversion failed: {e}")
        except Exception as e:
            raise DocumentProcessingException(f"DOC text extraction failed: {e}")
    
    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """
        Build masked output using the CACHED PDF (no re-conversion).
        
        Args:
            raw: Original .doc file bytes (not used, PDF is cached)
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
            raise DocumentProcessingException(f"DOC masking failed: {e}")
        finally:
            # Clean up cached PDF after processing
            if self._temp_pdf_path and os.path.exists(self._temp_pdf_path):
                os.unlink(self._temp_pdf_path)
                self._temp_pdf_path = None
