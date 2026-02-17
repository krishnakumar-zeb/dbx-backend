"""
Repository for PII database operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from utility.ORM import PIIDetailsRecord, AssessmentDetailsRecord, ProspectDetailsRecord
from utility.exceptions import DatabaseException, AssessmentNotFoundException
import json


class PIIRepository:
    """Repository for PII data operations"""
    
    def __init__(self, db_session: Session):
        """
        Initialize repository with database session
        
        Args:
            db_session: Database session
        """
        self.db_session = db_session
    
    def verify_assessment_exists(self, assessment_id: str) -> bool:
        """
        Verify if assessment exists in database
        
        Args:
            assessment_id: Assessment UUID
            
        Returns:
            True if exists, raises exception otherwise
        """
        try:
            query = select(AssessmentDetailsRecord).where(
                AssessmentDetailsRecord.assessment_id == assessment_id,
                AssessmentDetailsRecord.is_active == True
            )
            result = self.db_session.execute(query)
            assessment = result.scalar_one_or_none()
            
            if not assessment:
                raise AssessmentNotFoundException(
                    f"No assessment found with ID: {assessment_id}"
                )
            
            return True
            
        except AssessmentNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to verify assessment: {str(e)}")
    
    def get_prospect_by_assessment(self, assessment_id: str) -> Optional[ProspectDetailsRecord]:
        """
        Get prospect details by assessment ID
        
        Args:
            assessment_id: Assessment UUID
            
        Returns:
            ProspectDetailsRecord or None
        """
        try:
            query = select(ProspectDetailsRecord).join(
                AssessmentDetailsRecord,
                AssessmentDetailsRecord.prospect_id == ProspectDetailsRecord.prospect_id
            ).where(
                AssessmentDetailsRecord.assessment_id == assessment_id,
                AssessmentDetailsRecord.is_active == True,
                ProspectDetailsRecord.is_active == True
            )
            result = self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to retrieve prospect: {str(e)}")
    
    def save_pii_details(
        self,
        request_id: str,
        assessment_id: str,
        prospect_id: str,
        input_type: str,
        caller_name: str,
        country: Optional[str],
        processed_document: str,
        output_text: str,
        anonymizing_mapping: dict,
        encrypted_key: Optional[str] = None,
        created_by: str = "system"
    ) -> PIIDetailsRecord:
        """
        Save PII processing details to database
        
        Args:
            request_id: Unique request identifier
            assessment_id: Assessment UUID
            prospect_id: Prospect UUID
            input_type: Type of input document
            caller_name: Name of calling service
            country: Detected country
            processed_document: Path or encoded document
            output_text: Extracted text
            anonymizing_mapping: Mapping of anonymized entities
            encrypted_key: AES-CBC encryption key
            created_by: User who created the record
            
        Returns:
            Saved PIIDetailsRecord
        """
        try:
            # Create new record
            pii_record = PIIDetailsRecord(
                request_id=request_id,
                assessment_id=assessment_id,
                prospect_id=prospect_id,
                input_type=input_type,
                caller_name=caller_name,
                country=country,
                processed_document=processed_document,
                output_text=output_text,
                anonymizing_mapping=anonymizing_mapping,
                encrypted_key=encrypted_key,
                created_by=created_by,
                modified_by=created_by,
                is_active=True
            )
            
            # Add to session
            self.db_session.add(pii_record)
            
            # Commit transaction
            self.db_session.commit()
            
            # Refresh to get generated values
            self.db_session.refresh(pii_record)
            
            return pii_record
            
        except SQLAlchemyError as e:
            # Rollback on error
            self.db_session.rollback()
            raise DatabaseException(f"Failed to save PII details: {str(e)}")
    
    def get_pii_details(self, request_id: str) -> Optional[PIIDetailsRecord]:
        """
        Get PII details by request ID
        
        Args:
            request_id: Request identifier
            
        Returns:
            PIIDetailsRecord or None
        """
        try:
            query = select(PIIDetailsRecord).where(
                PIIDetailsRecord.request_id == request_id,
                PIIDetailsRecord.is_active == True
            )
            result = self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to retrieve PII details: {str(e)}")
    
    def get_pii_by_assessment(self, assessment_id: str) -> List[PIIDetailsRecord]:
        """
        Get all PII records for an assessment
        
        Args:
            assessment_id: Assessment UUID
            
        Returns:
            List of PIIDetailsRecord
        """
        try:
            query = select(PIIDetailsRecord).where(
                PIIDetailsRecord.assessment_id == assessment_id,
                PIIDetailsRecord.is_active == True
            )
            result = self.db_session.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to retrieve PII records: {str(e)}")
    
    def update_pii_details(
        self,
        request_id: str,
        modified_by: str,
        **kwargs
    ) -> PIIDetailsRecord:
        """
        Update PII details record
        
        Args:
            request_id: Request identifier
            modified_by: User making the modification
            **kwargs: Fields to update
            
        Returns:
            Updated PIIDetailsRecord
        """
        try:
            # Get existing record
            query = select(PIIDetailsRecord).where(
                PIIDetailsRecord.request_id == request_id
            )
            result = self.db_session.execute(query)
            pii_record = result.scalar_one_or_none()
            
            if not pii_record:
                raise DatabaseException(f"PII record not found: {request_id}")
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(pii_record, key):
                    setattr(pii_record, key, value)
            
            pii_record.modified_by = modified_by
            
            # Commit changes
            self.db_session.commit()
            self.db_session.refresh(pii_record)
            
            return pii_record
            
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise DatabaseException(f"Failed to update PII details: {str(e)}")
