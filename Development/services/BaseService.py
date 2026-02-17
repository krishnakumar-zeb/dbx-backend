"""
Base service with shared logic for all document processors.
Handles: read bytes, detect PII, anonymize, save to DB, cleanup.
"""
from fastapi import UploadFile
from typing import Dict, Optional
import os
import tempfile
import logging

from repository.PIIRepository import PIIRepository
from utility.PresidioUtility import PresidioUtility
from utility.exceptions import DocumentProcessingException
from utility.helpers import generate_request_id

logger = logging.getLogger(__name__)


class BaseService:
    """Abstract base for every document-type service."""

    def __init__(self, repository: PIIRepository, presidio: PresidioUtility):
        self.repository = repository
        self.presidio = presidio

    # -- subclasses MUST implement these --
    def _validate(self, document: UploadFile) -> None:
        """Raise FileValidationException if invalid."""
        pass

    def _extract_text(self, raw: bytes, filename: str) -> str:
        raise NotImplementedError

    def _build_masked_output(
        self, raw: bytes, mapping: Dict, anonymized_text: str, out_path: str
    ) -> None:
        """Write the masked file to *out_path*."""
        raise NotImplementedError

    @staticmethod
    def _masked_filename(original: str) -> str:
        """'report.pdf' -> 'report_masked.pdf'"""
        name, ext = os.path.splitext(original)
        return f"{name}_masked{ext}"

    def process_document(
        self,
        assessment_id: str,
        prospect_id: str,
        caller_name: str,
        document: UploadFile,
        country: str,
        created_by: str,
    ) -> Dict:
        temp_path: Optional[str] = None
        out_path: Optional[str] = None
        try:
            request_id = generate_request_id()
            self._validate(document)

            raw = document.file.read()
            document.file.seek(0)

            original_name = document.filename or "document"
            ext = os.path.splitext(original_name)[1]
            
            # Use system temp directory (works on Windows and Unix)
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"{request_id}_original{ext}")
            
            with open(temp_path, "wb") as f:
                f.write(raw)

            # Extract text
            text = self._extract_text(raw, original_name)

            # Detect & anonymize
            entities = self.presidio.detect_pii(text, country=country)
            anon = self.presidio.anonymize_text(text, entities)

            # Build masked output
            masked_name = self._masked_filename(original_name)
            out_path = os.path.join(temp_dir, f"{request_id}_{masked_name}")
            self._build_masked_output(raw, anon["mapping"], anon["anonymized_text"], out_path)

            # Persist
            self.repository.save_pii_details(
                request_id=request_id,
                assessment_id=assessment_id,
                prospect_id=prospect_id,
                input_type=ext.lstrip(".") or "txt",
                caller_name=caller_name,
                country=country,
                processed_document=out_path,
                output_text=anon["anonymized_text"],
                anonymizing_mapping=anon["mapping"],
                encrypted_key=anon["encryption_key"],
                created_by=created_by,
            )

            # Cleanup temp
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

            return {
                "request_id": request_id,
                "processed_document": out_path,
                "entities_detected": anon["entities_count"],
            }
        except Exception as e:
            for p in (temp_path, out_path):
                if p and os.path.exists(p):
                    os.remove(p)
            if isinstance(e, DocumentProcessingException):
                raise
            raise DocumentProcessingException(f"Processing failed: {e}")
