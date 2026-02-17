"""TXT Service – plain text PII masking."""
from fastapi import UploadFile
from typing import Dict
from services.BaseService import BaseService
from utility.exceptions import FileValidationException


class TXTService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(".txt"):
            raise FileValidationException("File must be a .txt file")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(anonymized_text)
