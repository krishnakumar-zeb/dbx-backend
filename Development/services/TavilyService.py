"""Tavily Service – mask PII in web/HTML content."""
from fastapi import UploadFile
from typing import Dict
from bs4 import BeautifulSoup

from services.BaseService import BaseService
from utility.exceptions import DocumentProcessingException


class TavilyService(BaseService):

    def _extract_text(self, raw: bytes, filename: str) -> str:
        try:
            content = raw.decode("utf-8")
            if "<html" in content.lower() or "<body" in content.lower():
                soup = BeautifulSoup(content, "html.parser")
                return soup.get_text(separator=" ", strip=True)
            return content
        except Exception as e:
            raise DocumentProcessingException(f"Tavily text extraction failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(anonymized_text)
