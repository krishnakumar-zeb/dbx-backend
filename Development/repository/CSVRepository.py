"""
CSV-based Repository for PII data operations
Implements same interface as PIIRepository but uses CSV files instead of database
"""
import os
from typing import List, Optional, Dict
from datetime import datetime
import logging

from utility.csv_helpers import (
    read_csv_records,
    write_csv_record,
    find_csv_record,
    find_csv_records,
    update_csv_record,
    serialize_json_for_csv,
    deserialize_json_from_csv,
    ensure_csv_file_exists
)
from utility.storage_config import get_pii_csv_path, PII_RECORDS_HEADERS
from utility.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class PIIRecord:
    """Simple data class to mimic ORM record"""
    
    def __init__(self, data: Dict):
        self.request_id = data.get('request_id')
        self.assessment_id = data.get('assessment_id')
        self.prospect_id = data.get('prospect_id')
        self.input_type = data.get('input_type')
        self.caller_name = data.get('caller_name')
        self.country = data.get('country')
        self.processed_document = data.get('processed_document')
        self.output_text = data.get('output_text')
        
        # Deserialize JSON fields
        mapping_str = data.get('anonymizing_mapping', '')
        self.anonymizing_mapping = deserialize_json_from_csv(mapping_str) or {}
        
        self.encrypted_key = data.get('encrypted_key')
        self.created_at = data.get('created_at')
        self.created_by = data.get('created_by')
        self.modified_at = data.get('modified_at')
        self.modified_by = data.get('modified_by')
        self.is_active = data.get('is_active', 'True') == 'True'


class CSVRepository:
    """CSV-based repository for PII data operations"""
    
    def __init__(self):
        """Initialize CSV repository"""
        self.csv_path = get_pii_csv_path()
        ensure_csv_file_exists(self.csv_path, PII_RECORDS_HEADERS)
        logger.info(f"CSVRepository initialized with file: {self.csv_path}")
    
    def verify_assessment_exists(self, assessment_id: str) -> bool:
        """
        Verify if assessment exists
        In CSV mode, we skip this validation
        
        Args:
            assessment_id: Assessment UUID
            
        Returns:
            Always returns True in CSV mode
        """
        logger.info(f"Assessment validation skipped in CSV mode for: {assessment_id}")
        return True
    
    def get_prospect_by_assessment(self, assessment_id: str) -> Optional[PIIRecord]:
        """
        Get prospect details by assessment ID
        In CSV mode, we skip this as we don't have prospect table
        
        Args:
            assessment_id: Assessment UUID
            
        Returns:
            None (not implemented in CSV mode)
        """
        logger.info(f"Prospect lookup skipped in CSV mode for: {assessment_id}")
        return None
    
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
    ) -> PIIRecord:
        """
        Save PII processing details to CSV
        
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
            PIIRecord object
        """
        try:
            timestamp = datetime.utcnow().isoformat() + "Z"
            
            record = {
                "request_id": request_id,
                "assessment_id": assessment_id,
                "prospect_id": prospect_id,
                "input_type": input_type,
                "caller_name": caller_name,
                "country": country or "",
                "processed_document": processed_document,
                "output_text": output_text,
                "anonymizing_mapping": serialize_json_for_csv(anonymizing_mapping),
                "encrypted_key": encrypted_key or "",
                "created_at": timestamp,
                "created_by": created_by,
                "modified_at": timestamp,
                "modified_by": created_by,
                "is_active": "True"
            }
            
            success = write_csv_record(self.csv_path, record, PII_RECORDS_HEADERS)
            
            if not success:
                raise DatabaseException("Failed to write PII record to CSV")
            
            logger.info(f"Saved PII record to CSV: {request_id}")
            return PIIRecord(record)
            
        except Exception as e:
            raise DatabaseException(f"Failed to save PII details: {str(e)}")
    
    def get_pii_details(self, request_id: str) -> Optional[PIIRecord]:
        """
        Get PII details by request ID
        
        Args:
            request_id: Request identifier
            
        Returns:
            PIIRecord or None
        """
        try:
            record_data = find_csv_record(self.csv_path, "request_id", request_id)
            
            if not record_data:
                return None
            
            # Only return active records
            if record_data.get('is_active') != 'True':
                return None
            
            return PIIRecord(record_data)
            
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve PII details: {str(e)}")
    
    def get_pii_by_assessment(self, assessment_id: str) -> List[PIIRecord]:
        """
        Get all PII records for an assessment
        
        Args:
            assessment_id: Assessment UUID
            
        Returns:
            List of PIIRecord objects
        """
        try:
            records_data = find_csv_records(self.csv_path, "assessment_id", assessment_id)
            
            # Filter active records and convert to PIIRecord objects
            records = []
            for data in records_data:
                if data.get('is_active') == 'True':
                    records.append(PIIRecord(data))
            
            return records
            
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve PII records: {str(e)}")
    
    def update_pii_details(
        self,
        request_id: str,
        modified_by: str,
        **kwargs
    ) -> PIIRecord:
        """
        Update PII details record
        
        Args:
            request_id: Request identifier
            modified_by: User making the modification
            **kwargs: Fields to update
            
        Returns:
            Updated PIIRecord
        """
        try:
            # Get existing record
            existing = self.get_pii_details(request_id)
            
            if not existing:
                raise DatabaseException(f"PII record not found: {request_id}")
            
            # Prepare updates
            updates = {}
            for key, value in kwargs.items():
                if key == "anonymizing_mapping":
                    updates[key] = serialize_json_for_csv(value)
                else:
                    updates[key] = str(value) if value is not None else ""
            
            updates["modified_by"] = modified_by
            updates["modified_at"] = datetime.utcnow().isoformat() + "Z"
            
            # Update record
            success = update_csv_record(
                self.csv_path,
                "request_id",
                request_id,
                updates,
                PII_RECORDS_HEADERS
            )
            
            if not success:
                raise DatabaseException(f"Failed to update PII record: {request_id}")
            
            # Return updated record
            return self.get_pii_details(request_id)
            
        except Exception as e:
            raise DatabaseException(f"Failed to update PII details: {str(e)}")
