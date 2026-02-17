"""PDF Service – extract text from PDF, mask PII, write new PDF."""
from fastapi import UploadFile
from typing import Dict
import PyPDF2
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException


class PDFService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(".pdf"):
            raise FileValidationException("File must be a PDF")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            ).strip()
        except Exception as e:
            raise DocumentProcessingException(f"PDF text extraction failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        try:
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            y = 750
            for line in anonymized_text.split("\n"):
                if y < 50:
                    c.showPage()
                    y = 750
                # Handle long lines by wrapping at 95 chars
                while line:
                    c.drawString(50, y, line[:95])
                    line = line[95:]
                    y -= 14
            c.save()
            with open(out_path, "wb") as f:
                f.write(buf.getvalue())
        except Exception as e:
            raise DocumentProcessingException(f"PDF creation failed: {e}")
