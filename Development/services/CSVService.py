"""
CSV Service – Handle CSV files by converting to XLSX first.

This service converts CSV files to XLSX using LibreOffice, then processes
them through the XLSXService for cell-by-cell PII masking.
This ensures better formatting preservation and consistent handling.
"""
from fastapi import UploadFile
import tempfile
import os

from services.BaseService import BaseService
from services.LibreOfficeConverter import LibreOfficeConverter, ConversionException
from services.XLSXService import XLSXService
from utility.exceptions import FileValidationException, DocumentProcessingException


class CSVService(BaseService):
    """
    Service for processing CSV files.
    
    Workflow:
    1. Save uploaded CSV file to temp location
    2. Convert CSV to XLSX using LibreOffice
    3. Process XLSX through XLSXService
    4. Return anonymized XLSX
    
    Note: Output will be XLSX format, not CSV. This is intentional
    to ensure better formatting preservation and consistent cell-based masking.
    """
    
    def __init__(self, repository, presidio):
        super().__init__(repository, presidio)
        self.converter = LibreOfficeConverter()
        self.xlsx_service = XLSXService(repository, presidio)

    def _validate(self, document: UploadFile) -> None:
        """Validate that the file is a CSV file."""
        fn = (document.filename or "").lower()
        if not fn.endswith(".csv"):
            raise FileValidationException("File must be a .csv file")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        """
        Extract text from CSV file by converting to XLSX first.
        
        Args:
            raw: Raw CSV file bytes
            filename: Original filename
            
        Returns:
            Extracted text
        """
        try:
            # Save CSV to temp file
            with tempfile.NamedTemporaryFile(
                suffix='.csv',
                delete=False
            ) as temp_csv:
                temp_csv.write(raw)
                temp_csv_path = temp_csv.name
            
            try:
                # Convert to XLSX
                temp_xlsx_path = self.converter.convert_csv_to_xlsx(temp_csv_path)
                
                try:
                    # Extract text from XLSX
                    with open(temp_xlsx_path, 'rb') as f:
                        xlsx_bytes = f.read()
                    
                    text = self.xlsx_service._extract_text(xlsx_bytes, filename)
                    
                    return text
                    
                finally:
                    # Clean up temp XLSX
                    if os.path.exists(temp_xlsx_path):
                        os.unlink(temp_xlsx_path)
            finally:
                # Clean up temp CSV
                if os.path.exists(temp_csv_path):
                    os.unlink(temp_csv_path)
                    
        except ConversionException as e:
            raise DocumentProcessingException(f"CSV to XLSX conversion failed: {e}")
        except Exception as e:
            raise DocumentProcessingException(f"CSV text extraction failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """
        Build masked output by converting to XLSX and masking.
        
        Args:
            raw: Original CSV file bytes
            mapping: PII mapping (not used directly)
            anonymized_text: Text with PII replaced by tags
            out_path: Output file path (will be XLSX)
        """
        try:
            # Save CSV to temp file
            with tempfile.NamedTemporaryFile(
                suffix='.csv',
                delete=False
            ) as temp_csv:
                temp_csv.write(raw)
                temp_csv_path = temp_csv.name
            
            try:
                # Convert to XLSX
                temp_xlsx_path = self.converter.convert_csv_to_xlsx(temp_csv_path)
                
                try:
                    # Read XLSX bytes
                    with open(temp_xlsx_path, 'rb') as f:
                        xlsx_bytes = f.read()
                    
                    # Process through XLSX service
                    self.xlsx_service._build_masked_output(
                        xlsx_bytes,
                        mapping,
                        anonymized_text,
                        out_path
                    )
                    
                finally:
                    # Clean up temp XLSX
                    if os.path.exists(temp_xlsx_path):
                        os.unlink(temp_xlsx_path)
            finally:
                # Clean up temp CSV
                if os.path.exists(temp_csv_path):
                    os.unlink(temp_csv_path)
                    
        except ConversionException as e:
            raise DocumentProcessingException(f"CSV to XLSX conversion failed: {e}")
        except Exception as e:
            raise DocumentProcessingException(f"CSV masking failed: {e}")
