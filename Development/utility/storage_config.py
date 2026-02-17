"""
Storage Configuration
Manages storage mode (database vs CSV) and related settings
"""
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Storage mode from environment variable
STORAGE_MODE = os.getenv("STORAGE_MODE", "csv").lower()

# CSV data path - use absolute path
_default_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_DATA_PATH = os.getenv("CSV_DATA_PATH", _default_csv_path)

# CSV file names
PII_RECORDS_CSV = "pii_records.csv"


def get_storage_mode() -> str:
    """
    Get current storage mode
    
    Returns:
        "database" or "csv"
    """
    return STORAGE_MODE


def get_csv_data_path() -> str:
    """
    Get path to CSV data directory
    
    Returns:
        Path to CSV data directory
    """
    return CSV_DATA_PATH


def get_pii_csv_path() -> str:
    """
    Get full path to PII records CSV file
    
    Returns:
        Full path to pii_records.csv
    """
    return os.path.join(CSV_DATA_PATH, PII_RECORDS_CSV)


def is_csv_mode() -> bool:
    """
    Check if running in CSV storage mode
    
    Returns:
        True if CSV mode, False if database mode
    """
    return STORAGE_MODE == "csv"


def is_database_mode() -> bool:
    """
    Check if running in database storage mode
    
    Returns:
        True if database mode, False if CSV mode
    """
    return STORAGE_MODE == "database"


def init_csv_storage() -> None:
    """
    Initialize CSV storage directory and files
    Creates data directory if it doesn't exist
    """
    try:
        data_path = Path(CSV_DATA_PATH)
        data_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"CSV storage initialized at: {data_path.absolute()}")
    except Exception as e:
        logger.error(f"Failed to initialize CSV storage: {e}")
        raise


# CSV Headers for pii_records.csv
PII_RECORDS_HEADERS = [
    "request_id",
    "assessment_id",
    "prospect_id",
    "input_type",
    "caller_name",
    "country",
    "processed_document",
    "output_text",
    "anonymizing_mapping",
    "encrypted_key",
    "created_at",
    "created_by",
    "modified_at",
    "modified_by",
    "is_active"
]
