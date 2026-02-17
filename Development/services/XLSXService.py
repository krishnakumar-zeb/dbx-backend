"""XLSX Service – mask PII in Excel workbooks cell-by-cell."""
from fastapi import UploadFile
from typing import Dict
import openpyxl
import io

from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException


class XLSXService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(".xlsx"):
            raise FileValidationException("File must be an .xlsx file")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        try:
            wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
            parts = []
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    parts.extend(
                        str(cell.value) for cell in row if cell.value is not None
                    )
            return " ".join(parts)
        except Exception as e:
            raise DocumentProcessingException(f"XLSX parse failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """Replace PII in each cell of the workbook."""
        try:
            wb = openpyxl.load_workbook(io.BytesIO(raw))
            # Build original->tag from the CSV-style diff approach
            orig_text = self._extract_text(raw, "")
            from services.CSVService import CSVService
            replacements = CSVService._build_replacement_pairs(orig_text, anonymized_text)

            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for cell in row:
                        if cell.value is not None:
                            val = str(cell.value)
                            masked = CSVService._apply_replacements(val, replacements)
                            if masked != val:
                                cell.value = masked
            wb.save(out_path)
        except Exception as e:
            raise DocumentProcessingException(f"XLSX masking failed: {e}")
