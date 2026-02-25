"""
Pydantic models for PII Anonymization API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List


"""
Pydantic models for PII Anonymization API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List


# ==================== Country Detection Models ====================

class CountryDetectionResult(BaseModel):
    """Pydantic model for country detection result"""
    country: Optional[str] = Field(None, description="Detected country name")
    confidence: str = Field(..., description="Confidence level: high, medium, low, none")
    source: Optional[str] = Field(None, description="Source of information")
    matched_from_list: bool = Field(default=False, description="Whether country was found in supported list")
    raw_answer: Optional[str] = Field(None, description="Raw answer from API")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if v not in ['high', 'medium', 'low', 'none']:
            raise ValueError('confidence must be one of: high, medium, low, none')
        return v


# ==================== PII Processing Models ====================

class PIIRequest(BaseModel):
    """Request model for PII processing"""
    assessment_id: str = Field(..., description="Assessment UUID")
    prospect_id: str = Field(..., description="Prospect UUID")
    caller_name: str = Field(..., min_length=1, max_length=255, description="Name of calling service")
    input_type: str = Field(..., description="Document type")
    
    @validator('input_type')
    def validate_input_type(cls, v):
        allowed_types = ['pdf', 'docx', 'txt', 'csv', 'xlsx', 'json']
        if v.lower() not in allowed_types:
            raise ValueError(f'input_type must be one of: {", ".join(allowed_types)}')
        return v.lower()


class ProcessedDocumentResult(BaseModel):
    """Result model for processed document"""
    request_id: str
    processed_document: str
    entities_detected: int
    country: Optional[str] = None


class PIIResponse(BaseModel):
    """Response model for PII API"""
    status: str
    code: int
    message: str
    data: dict
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    code: int
    message: str
    error: str
    request_id: str
    timestamp: str


# ==================== Presidio Models ====================

class AnonymizedResult(BaseModel):
    """Result from Presidio anonymization"""
    anonymized_text: str
    mapping: dict
    entities_count: int


class PIIEntity(BaseModel):
    """PII entity detected by Presidio"""
    entity_type: str
    start: int
    end: int
    score: float
    text: Optional[str] = None
