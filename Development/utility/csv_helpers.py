"""
CSV Helper Utilities for file-based storage
Provides thread-safe CSV operations with proper escaping and JSON handling
"""
import csv
import json
import os
import sys
import time
from typing import List, Dict, Optional, Any
from datetime import datetime
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Platform-specific imports for file locking
if sys.platform == 'win32':
    import msvcrt
else:
    import fcntl


@contextmanager
def file_lock(file_handle, timeout=10):
    """
    Context manager for file locking with timeout
    Works on both Windows and Unix/Linux systems
    """
    start_time = time.time()
    
    if sys.platform == 'win32':
        # Windows file locking
        while True:
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)
                yield
                break
            except IOError:
                if time.time() - start_time >= timeout:
                    raise TimeoutError("Could not acquire file lock")
                time.sleep(0.1)
            finally:
                try:
                    msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass
    else:
        # Unix/Linux file locking
        while True:
            try:
                fcntl.flock(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                yield
                break
            except IOError:
                if time.time() - start_time >= timeout:
                    raise TimeoutError("Could not acquire file lock")
                time.sleep(0.1)
            finally:
                try:
                    fcntl.flock(file_handle, fcntl.LOCK_UN)
                except:
                    pass


def serialize_json_for_csv(data: Any) -> str:
    """
    Convert dict/list to JSON string for CSV storage
    
    Args:
        data: Dictionary or list to serialize
        
    Returns:
        JSON string
    """
    if data is None:
        return ""
    return json.dumps(data, ensure_ascii=False)


def deserialize_json_from_csv(json_str: str) -> Any:
    """
    Parse JSON string from CSV field
    
    Args:
        json_str: JSON string from CSV
        
    Returns:
        Parsed dict/list or None
    """
    if not json_str or json_str.strip() == "":
        return None
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None


def ensure_csv_file_exists(csv_path: str, headers: List[str]) -> None:
    """
    Create CSV file with headers if it doesn't exist
    
    Args:
        csv_path: Path to CSV file
        headers: List of column headers
    """
    if not os.path.exists(csv_path):
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
            writer.writeheader()
        logger.info(f"Created CSV file: {csv_path}")


def read_csv_records(csv_path: str) -> List[Dict[str, Any]]:
    """
    Read all records from CSV file
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of dictionaries representing records
    """
    if not os.path.exists(csv_path):
        return []
    
    records = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            with file_lock(f):
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
        return records
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return []


def write_csv_record(csv_path: str, record: Dict[str, Any], headers: List[str]) -> bool:
    """
    Append a single record to CSV file
    
    Args:
        csv_path: Path to CSV file
        record: Dictionary representing the record
        headers: List of column headers
        
    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_csv_file_exists(csv_path, headers)
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            with file_lock(f):
                writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
                writer.writerow(record)
        return True
    except Exception as e:
        logger.error(f"Failed to write CSV record: {e}")
        return False


def find_csv_record(csv_path: str, field: str, value: Any) -> Optional[Dict[str, Any]]:
    """
    Find a record in CSV by field value
    
    Args:
        csv_path: Path to CSV file
        field: Field name to search
        value: Value to match
        
    Returns:
        Dictionary representing the record or None
    """
    records = read_csv_records(csv_path)
    for record in records:
        if record.get(field) == str(value):
            return record
    return None


def find_csv_records(csv_path: str, field: str, value: Any) -> List[Dict[str, Any]]:
    """
    Find all records in CSV matching field value
    
    Args:
        csv_path: Path to CSV file
        field: Field name to search
        value: Value to match
        
    Returns:
        List of dictionaries representing matching records
    """
    records = read_csv_records(csv_path)
    return [r for r in records if r.get(field) == str(value)]


def update_csv_record(csv_path: str, field: str, value: Any, updates: Dict[str, Any], headers: List[str]) -> bool:
    """
    Update an existing record in CSV file
    
    Args:
        csv_path: Path to CSV file
        field: Field name to identify record
        value: Value to match
        updates: Dictionary of fields to update
        headers: List of column headers
        
    Returns:
        True if successful, False otherwise
    """
    try:
        records = read_csv_records(csv_path)
        updated = False
        
        for record in records:
            if record.get(field) == str(value):
                record.update(updates)
                record['modified_at'] = datetime.utcnow().isoformat() + "Z"
                updated = True
                break
        
        if not updated:
            return False
        
        # Rewrite entire file
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            with file_lock(f):
                writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                writer.writerows(records)
        
        return True
    except Exception as e:
        logger.error(f"Failed to update CSV record: {e}")
        return False


def delete_csv_record(csv_path: str, field: str, value: Any, headers: List[str]) -> bool:
    """
    Soft delete a record by setting is_active to False
    
    Args:
        csv_path: Path to CSV file
        field: Field name to identify record
        value: Value to match
        headers: List of column headers
        
    Returns:
        True if successful, False otherwise
    """
    return update_csv_record(csv_path, field, value, {'is_active': 'False'}, headers)
