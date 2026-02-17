"""
Image Service – OCR text from images, mask PII, return masked text file.
Supports: PNG, JPG, JPEG, TIFF, BMP.
Uses pytesseract for OCR (requires Tesseract installed on the system).
"""
from fastapi import UploadFile
from typing import Dict
import io
import os
from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException
from PIL import Image
import pytesseract

SUPPORTED_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp")


class ImageService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(SUPPORTED_IMAGE_EXTS):
            raise FileValidationException(
                f"Image must be one of: {', '.join(SUPPORTED_IMAGE_EXTS)}"
            )

    def _extract_text(self, raw: bytes, filename: str) -> str:
        """OCR the image to extract text."""
        try:

            img = Image.open(io.BytesIO(raw))
            text = pytesseract.image_to_string(img)
            if not text or not text.strip():
                raise DocumentProcessingException("No text could be extracted from image")
            return text.strip()
        except ImportError:
            raise DocumentProcessingException(
                "pytesseract and Pillow are required for image processing. "
                "Install with: pip install pytesseract Pillow"
            )
        except Exception as e:
            raise DocumentProcessingException(f"Image OCR failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """Write masked text to a .txt file (images can't be re-rendered with masked text)."""
        # Change extension to .txt for the output
        base, _ = os.path.splitext(out_path)
        txt_path = base + ".txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(anonymized_text)
        # Rename out_path reference (caller uses the path we write to)
        # Since BaseService uses out_path, we write to out_path directly
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(anonymized_text)
