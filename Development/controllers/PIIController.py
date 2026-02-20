"""
Controller for PII Anonymization API.
Accepts documents in multiple formats, detects country via Tavily,
applies country-specific PII detection, masks content, and returns
the masked file renamed as <original_name>_masked.<ext>.
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime
import uuid
import os
import logging

from utility.database import get_db_session
from utility.exceptions import (
    PIIException,
    InvalidInputTypeException,
    FileValidationException,
    PayloadTooLargeException,
)
from utility.country_pii_config import DEFAULT_COUNTRY, SUPPORTED_COUNTRIES
from repository.PIIRepository import PIIRepository
from repository.CSVRepository import CSVRepository
from utility.storage_config import is_csv_mode
from utility.PresidioUtility import PresidioUtility
from utility.TavilyCountrySearch import TavilyCountrySearch

from services.PDFService import PDFService
from services.DOCService import DOCService
from services.DOCXService import DOCXService
from services.TXTService import TXTService
from services.CSVService import CSVService
from services.XLSXService import XLSXService
from services.JSONService import JSONService
from services.TavilyService import TavilyService
from services.ImageService import ImageService
from services.UnmaskService import UnmaskService

logger = logging.getLogger(__name__)
router = APIRouter()

SUPPORTED_INPUT_TYPES = [
    "pdf", "doc", "docx", "txt", "csv", "xlsx", "json",
    "tavily", "png", "jpg", "jpeg", "tiff", "bmp",
]
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))


from utility.helpers import generate_request_id  # noqa: E402 – avoid circular imports


def _get_repository(db_session=None):
    """
    Get appropriate repository based on storage mode
    
    Args:
        db_session: Database session (only used in database mode)
        
    Returns:
        CSVRepository or PIIRepository
    """
    if is_csv_mode():
        return CSVRepository()
    else:
        return PIIRepository(db_session)


def _detect_country(
    company_name: Optional[str],
    company_website: Optional[str],
    request_id: str,
) -> str:
    """Use Tavily to resolve company -> country. Falls back to US."""
    if not company_name:
        logger.info(f"[{request_id}] No company_name provided, defaulting to {DEFAULT_COUNTRY}")
        return DEFAULT_COUNTRY
    try:
        tavily = TavilyCountrySearch()
        ctx = company_website if company_website else None
        result = tavily.search_prospect_country(company_name, ctx)
        if result.matched_from_list and result.country:
            logger.info(f"[{request_id}] Country detected: {result.country}")
            return result.country
    except Exception as e:
        logger.error(f"[{request_id}] Tavily country detection error: {e}")
    logger.info(f"[{request_id}] Defaulting to {DEFAULT_COUNTRY}")
    return DEFAULT_COUNTRY


def _resolve_input_type(input_type: Optional[str], filename: str) -> str:
    """Resolve input_type from explicit param or file extension."""
    if input_type:
        return input_type.lower().strip()
    ext = os.path.splitext(filename)[1].lstrip(".").lower()
    return ext if ext else "txt"


def _validate_file_size(document: UploadFile) -> None:
    """Validate uploaded file doesn't exceed size limit."""
    document.file.seek(0, 2)
    size_mb = document.file.tell() / (1024 * 1024)
    document.file.seek(0)
    if size_mb > MAX_FILE_SIZE_MB:
        raise PayloadTooLargeException(
            f"File size {size_mb:.1f}MB exceeds limit of {MAX_FILE_SIZE_MB}MB"
        )


def _route_to_service(input_type: str, repo, presidio):
    """Return the appropriate service for *input_type*."""
    mapping = {
        "pdf": lambda: PDFService(repo, presidio),
        "doc": lambda: DOCService(repo, presidio),
        "docx": lambda: DOCXService(repo, presidio),
        "txt": lambda: TXTService(repo, presidio),
        "csv": lambda: CSVService(repo, presidio),
        "xlsx": lambda: XLSXService(repo, presidio),
        "json": lambda: JSONService(repo, presidio),
        "tavily": lambda: TavilyService(repo, presidio),
    }
    # Image types
    if input_type in ("png", "jpg", "jpeg", "tiff", "bmp"):
        return ImageService(repo, presidio)
    factory = mapping.get(input_type)
    if not factory:
        raise InvalidInputTypeException(f"Unsupported input type: {input_type}")
    return factory()


# ============================================================
# POST /handle-pii
# ============================================================
@router.post("/handle-pii")
def handle_pii(
    assessment_id: str = Form(...),
    prospect_id: str = Form(...),
    caller_name: str = Form(...),
    input_type: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    company_website: Optional[str] = Form(None),
    document: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> Dict:
    request_id = generate_request_id()
    start = datetime.now()
    try:
        # Resolve & validate
        resolved_type = _resolve_input_type(input_type, document.filename or "")
        if resolved_type not in SUPPORTED_INPUT_TYPES:
            raise InvalidInputTypeException(
                f"Unsupported type: {resolved_type}. Allowed: {', '.join(SUPPORTED_INPUT_TYPES)}"
            )
        _validate_input_ids(assessment_id, prospect_id, caller_name)
        _validate_file_size(document)

        # Detect country
        country = _detect_country(company_name, company_website, request_id)

        # Init repository based on storage mode
        repo = _get_repository(db)
        presidio = PresidioUtility()
        
        # Skip assessment validation in CSV mode
        if not is_csv_mode():
            repo.verify_assessment_exists(assessment_id)

        service = _route_to_service(resolved_type, repo, presidio)
        result = service.process_document(
            assessment_id=assessment_id,
            prospect_id=prospect_id,
            caller_name=caller_name,
            document=document,
            country=country,
            created_by="system",
        )

        ms = int((datetime.now() - start).total_seconds() * 1000)
        logger.info(f"[{request_id}] Done in {ms}ms")

        return _success({
            "request_id": result["request_id"],
            "processed_document": result["processed_document"],
            "entities_detected": result.get("entities_detected", 0),
            "country": country,
            "processing_time_ms": ms,
        }, f"{resolved_type.upper()} processed successfully")

    except PIIException as e:
        logger.error(f"[{request_id}] {e}")
        return _error(e, request_id)
    except Exception as e:
        logger.error(f"[{request_id}] Unexpected: {e}", exc_info=True)
        return _error(PIIException(str(e), 500), request_id)


# ============================================================
# POST /unmask-pii
# ============================================================
@router.post("/unmask-pii")
def unmask_pii(
    request_id: str = Form(...),
    input_type: str = Form(...),
    document: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> Dict:
    start = datetime.now()
    try:
        if not request_id.startswith("req_"):
            raise InvalidInputTypeException("request_id must start with 'req_'")
        it = input_type.lower().strip()
        if it not in SUPPORTED_INPUT_TYPES:
            raise InvalidInputTypeException(f"Unsupported type: {it}")

        repo = _get_repository(db)
        svc = UnmaskService(repo)
        result = svc.process_document(request_id, document, it)

        ms = int((datetime.now() - start).total_seconds() * 1000)
        return _success({
            "request_id": result["request_id"],
            "unmasked_document": result["unmasked_document"],
            "tags_replaced": result.get("tags_replaced", 0),
            "processing_time_ms": ms,
        }, f"{it.upper()} de-anonymised successfully")

    except PIIException as e:
        return _error(e, request_id)
    except Exception as e:
        return _error(PIIException(str(e), 500), request_id)


# ============================================================
# Helpers
# ============================================================
def _validate_input_ids(assessment_id, prospect_id, caller_name):
    try:
        uuid.UUID(assessment_id)
    except ValueError:
        raise InvalidInputTypeException("assessment_id must be a valid UUID")
    try:
        uuid.UUID(prospect_id)
    except ValueError:
        raise InvalidInputTypeException("prospect_id must be a valid UUID")
    if not caller_name or not caller_name.strip():
        raise InvalidInputTypeException("caller_name cannot be empty")


def _success(data: Dict, message: str) -> Dict:
    return {
        "status": "success",
        "code": 200,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def _error(exc: PIIException, request_id: str) -> Dict:
    return {
        "status": "error",
        "code": exc.code,
        "message": exc.message,
        "error": str(exc),
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
