"""
LibreOffice Converter Service
Converts DOC/DOCX documents to PDF using LibreOffice headless mode.
"""
import subprocess
import os
import tempfile
from pathlib import Path
from typing import Optional

from utility.exceptions import DocumentProcessingException


class ConversionException(DocumentProcessingException):
    """Exception raised when document conversion fails."""
    pass


class LibreOfficeConverter:
    """
    Convert DOC/DOCX documents to PDF using LibreOffice headless mode.
    
    This converter is specifically designed for Word documents that need
    to be processed through the PDF pipeline for precise coordinate-based
    PII redaction.
    
    CSV and XLSX files should NOT use this converter - they should be
    processed directly by their respective services.
    """
    
    def __init__(self, libreoffice_path: Optional[str] = None):
        """
        Initialize converter.
        
        Args:
            libreoffice_path: Path to LibreOffice executable
                             If None, will attempt to auto-detect based on OS
        """
        self.libreoffice_path = libreoffice_path or self._detect_libreoffice()
    
    def _detect_libreoffice(self) -> str:
        """
        Auto-detect LibreOffice installation path based on OS.
        
        Returns:
            Path to LibreOffice executable
            
        Raises:
            ConversionException: If LibreOffice not found
        """
        import platform
        
        system = platform.system()
        
        # Common paths for different operating systems
        if system == "Windows":
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
        elif system == "Linux":
            possible_paths = [
                "/usr/bin/soffice",
                "/usr/bin/libreoffice",
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            ]
        else:
            possible_paths = []
        
        # Try each path - just check if file exists
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # If not found in common paths, try PATH
        try:
            result = subprocess.run(
                ["soffice", "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return "soffice"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        raise ConversionException(
            "LibreOffice not found. Please install LibreOffice or provide the path manually. "
            "Download from: https://www.libreoffice.org/download/"
        )
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Check if file format is supported for conversion.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file can be converted
        """
        ext = Path(file_path).suffix.lower()
        return ext in ['.doc', '.docx', '.csv']
    
    def convert_to_pdf(
        self, 
        input_path: str, 
        output_dir: Optional[str] = None,
        cleanup_on_error: bool = True
    ) -> str:
        """
        Convert DOC/DOCX document to PDF using LibreOffice.
        
        Args:
            input_path: Path to input document (.doc or .docx)
            output_dir: Directory for output PDF (default: temp directory)
            cleanup_on_error: Whether to clean up partial files on error
            
        Returns:
            Path to generated PDF file
            
        Raises:
            ConversionException: If conversion fails
        """
        # Validate input
        if not os.path.exists(input_path):
            raise ConversionException(f"Input file not found: {input_path}")
        
        ext = Path(input_path).suffix.lower()
        if ext not in ['.doc', '.docx']:
            raise ConversionException(
                f"Unsupported file format for PDF conversion: {ext}. "
                f"Only .doc and .docx files are supported."
            )
        
        # Use temp directory if output_dir not specified
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Build LibreOffice command
        cmd = [
            self.libreoffice_path,
            "--headless",              # No GUI
            "--invisible",             # Don't show splash screen
            "--nocrashreport",         # Don't show crash reports
            "--nodefault",             # Don't start with default document
            "--nofirststartwizard",    # Skip first start wizard
            "--nolockcheck",           # Don't check for lock files
            "--nologo",                # Don't show logo
            "--norestore",             # Don't restore previous session
            "--convert-to", "pdf",     # Output format
            "--outdir", output_dir,    # Output directory
            input_path                 # Input file
        ]
        
        try:
            # Run conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Unknown error"
                raise ConversionException(
                    f"LibreOffice conversion failed: {error_msg}"
                )
            
            # Calculate output PDF path
            input_name = Path(input_path).stem
            output_pdf = os.path.join(output_dir, f"{input_name}.pdf")
            
            if not os.path.exists(output_pdf):
                raise ConversionException(
                    f"PDF not created at expected location: {output_pdf}"
                )
            
            return output_pdf
            
        except subprocess.TimeoutExpired:
            raise ConversionException(
                "Conversion timeout (>5 minutes). "
                "The document may be too large or complex."
            )
        except ConversionException:
            raise
        except Exception as e:
            raise ConversionException(f"Conversion error: {e}")
    
    def convert_csv_to_xlsx(
        self,
        input_path: str,
        output_dir: Optional[str] = None,
        cleanup_on_error: bool = True
    ) -> str:
        """
        Convert CSV to XLSX using LibreOffice.
        
        Args:
            input_path: Path to input CSV file
            output_dir: Directory for output XLSX (default: temp directory)
            cleanup_on_error: Whether to clean up partial files on error
            
        Returns:
            Path to generated XLSX file
            
        Raises:
            ConversionException: If conversion fails
        """
        # Validate input
        if not os.path.exists(input_path):
            raise ConversionException(f"Input file not found: {input_path}")
        
        ext = Path(input_path).suffix.lower()
        if ext != '.csv':
            raise ConversionException(
                f"Unsupported file format for XLSX conversion: {ext}. "
                f"Only .csv files are supported."
            )
        
        # Use temp directory if output_dir not specified
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Build LibreOffice command
        cmd = [
            self.libreoffice_path,
            "--headless",              # No GUI
            "--invisible",             # Don't show splash screen
            "--nocrashreport",         # Don't show crash reports
            "--nodefault",             # Don't start with default document
            "--nofirststartwizard",    # Skip first start wizard
            "--nolockcheck",           # Don't check for lock files
            "--nologo",                # Don't show logo
            "--norestore",             # Don't restore previous session
            "--convert-to", "xlsx",    # Output format
            "--outdir", output_dir,    # Output directory
            input_path                 # Input file
        ]
        
        try:
            # Run conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Unknown error"
                raise ConversionException(
                    f"LibreOffice CSV to XLSX conversion failed: {error_msg}"
                )
            
            # Calculate output XLSX path
            input_name = Path(input_path).stem
            output_xlsx = os.path.join(output_dir, f"{input_name}.xlsx")
            
            if not os.path.exists(output_xlsx):
                raise ConversionException(
                    f"XLSX not created at expected location: {output_xlsx}"
                )
            
            return output_xlsx
            
        except subprocess.TimeoutExpired:
            raise ConversionException(
                "CSV to XLSX conversion timeout (>5 minutes). "
                "The file may be too large."
            )
        except ConversionException:
            raise
        except Exception as e:
            raise ConversionException(f"CSV to XLSX conversion error: {e}")
    
    def convert_to_pdf_bytes(self, input_path: str) -> bytes:
        """
        Convert DOC/DOCX to PDF and return as bytes.
        
        Useful for API responses where you want to return the PDF
        without saving it permanently.
        
        Args:
            input_path: Path to input document
            
        Returns:
            PDF file content as bytes
            
        Raises:
            ConversionException: If conversion fails
        """
        # Convert to temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = self.convert_to_pdf(input_path, output_dir=temp_dir)
            
            # Read PDF bytes
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
            
            return pdf_bytes
    
    def batch_convert(
        self,
        input_files: list,
        output_dir: str,
        continue_on_error: bool = True
    ) -> dict:
        """
        Convert multiple files to PDF.
        
        Args:
            input_files: List of input file paths
            output_dir: Directory for output PDFs
            continue_on_error: Continue processing if a file fails
            
        Returns:
            Dictionary with conversion results:
            {
                'success': [list of successful conversions],
                'failed': [list of failed conversions with errors]
            }
        """
        results = {
            'success': [],
            'failed': []
        }
        
        for input_file in input_files:
            try:
                output_pdf = self.convert_to_pdf(input_file, output_dir)
                results['success'].append({
                    'input': input_file,
                    'output': output_pdf
                })
            except Exception as e:
                results['failed'].append({
                    'input': input_file,
                    'error': str(e)
                })
                
                if not continue_on_error:
                    raise
        
        return results


# Convenience function for quick conversions
def convert_doc_to_pdf(input_path: str, output_dir: Optional[str] = None) -> str:
    """
    Quick conversion function for DOC/DOCX to PDF.
    
    Args:
        input_path: Path to DOC/DOCX file
        output_dir: Output directory (default: temp)
        
    Returns:
        Path to generated PDF
    """
    converter = LibreOfficeConverter()
    return converter.convert_to_pdf(input_path, output_dir)
