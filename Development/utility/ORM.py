"""
ORM models for PII Anonymization API
"""
from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ProspectDetailsRecord(Base):
    """Prospect details table - existing table in the application"""
    __tablename__ = "prospect_details"
    
    prospect_id = Column(String, primary_key=True, nullable=False)
    prospect_name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String, nullable=True)
    modified_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    modified_by = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)


class AssessmentDetailsRecord(Base):
    """Assessment details table - existing table in the application"""
    __tablename__ = "assessment_details"
    
    assessment_id = Column(String, primary_key=True, nullable=False)
    prospect_id = Column(String, ForeignKey("prospect_details.prospect_id"), nullable=False)
    assessment_name = Column(String(255), nullable=False)
    assessment_description = Column(Text, nullable=False)
    is_draft = Column(Boolean, nullable=False)
    deck_link = Column(String(2083), nullable=True)
    document_link = Column(String(2083), nullable=True)
    volume_path = Column(String(500), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String, nullable=True)
    modified_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    modified_by = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)


class PIIDetailsRecord(Base):
    """PII details table for storing anonymization results"""
    __tablename__ = "pii_details"
    
    request_id = Column(String, primary_key=True, nullable=False)
    assessment_id = Column(String, ForeignKey("assessment_details.assessment_id"), nullable=False)
    prospect_id = Column(String, ForeignKey("prospect_details.prospect_id"), nullable=False)
    input_type = Column(String(50), nullable=False)
    caller_name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=True)  # Country detected via Tavily
    processed_document = Column(Text, nullable=False)  # Path or base64 encoded
    output_text = Column(Text, nullable=False)
    anonymizing_mapping = Column(JSON, nullable=False)  # Encrypted mapping with indexed tags
    encrypted_key = Column(Text, nullable=True)  # AES-CBC encryption key
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String, nullable=True)
    modified_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    modified_by = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
