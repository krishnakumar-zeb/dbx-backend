# CSV to Database Rollback Guide

This document provides step-by-step instructions to rollback from CSV storage mode to Database storage mode.

## Overview

The application now supports dual storage modes:
- **CSV Mode**: Stores PII records in CSV files (no database required)
- **Database Mode**: Stores PII records in PostgreSQL database (original implementation)

## Files Modified

### 1. New Files Created (Can be kept, won't affect DB mode)
- `Development/utility/csv_helpers.py` - CSV file operations
- `Development/utility/storage_config.py` - Storage mode configuration
- `Development/repository/CSVRepository.py` - CSV-based repository
- `DB_TO_CSV_MIGRATION_PLAN.md` - Migration planning document
- `CSV_TO_DATABASE_ROLLBACK_GUIDE.md` - This file

### 2. Files Modified (Changes documented below)

#### `Development/controllers/PIIController.py`
**Changes Made:**
1. Added imports for CSV mode
2. Added `_get_repository()` function
3. Modified `handle_pii()` to use `_get_repository()`
4. Modified `unmask_pii()` to use `_get_repository()`
5. Added conditional assessment validation

#### `Development/main.py`
**Changes Made:**
1. Added imports for CSV storage
2. Modified `startup_event()` to support both modes

#### `Development/.env`
**Changes Made:**
1. Added `STORAGE_MODE=csv`
2. Added `CSV_DATA_PATH=Development/data`

---

## Rollback Steps

### Step 1: Update Environment Configuration

**File:** `Development/.env`

**Change:**
```env
# FROM:
STORAGE_MODE=csv

# TO:
STORAGE_MODE=database
```

**Or simply comment out:**
```env
# STORAGE_MODE=csv  # Commented out - will default to database
```

### Step 2: Verify Database Credentials

Ensure your `.env` file has valid database credentials:

```env
# Lakebase PostgreSQL Configuration
LAKEBASE_USERNAME=your-username
LAKEBASE_PASSWORD=your-valid-token
LAKEBASE_HOST=your-host.database.cloud.databricks.com
LAKEBASE_PORT=5432
LAKEBASE_SCHEMA=public
```

### Step 3: Restart the Application

```bash
cd Development
python main.py
```

Or if using uvicorn directly:
```bash
uvicorn main:app --reload
```

### Step 4: Verify Database Mode

Check the startup logs - you should see:
```
Application started in DATABASE mode
Database tables created successfully
```

### Step 5: Test API Endpoints

Test that the API works with database storage:

```bash
# Test handle-pii endpoint
curl -X POST http://localhost:8000/v1/handle-pii \
  -F "assessment_id=a3097aef-06db-4568-a619-194e5b8c7d21" \
  -F "prospect_id=b4097aef-06db-4568-a619-194e5b8c7d22" \
  -F "caller_name=test" \
  -F "input_type=txt" \
  -F "document=@test.txt"
```

---

## Complete Code Rollback (If Needed)

If you want to completely remove CSV support and revert to original code:

### Rollback `Development/controllers/PIIController.py`

**Remove these imports:**
```python
from repository.CSVRepository import CSVRepository
from utility.storage_config import is_csv_mode
```

**Remove this function:**
```python
def _get_repository(db_session=None):
    """Get appropriate repository based on storage mode"""
    if is_csv_mode():
        return CSVRepository()
    else:
        return PIIRepository(db_session)
```

**In `handle_pii()` function, change:**
```python
# FROM:
repo = _get_repository(db)
presidio = PresidioUtility()

if not is_csv_mode():
    repo.verify_assessment_exists(assessment_id)

# TO:
repo = PIIRepository(db)
presidio = PresidioUtility()
repo.verify_assessment_exists(assessment_id)
```

**In `unmask_pii()` function, change:**
```python
# FROM:
repo = _get_repository(db)

# TO:
repo = PIIRepository(db)
```

### Rollback `Development/main.py`

**Remove these imports:**
```python
from utility.storage_config import is_csv_mode, init_csv_storage, get_csv_data_path
```

**In `startup_event()` function, change:**
```python
# FROM:
@app.on_event("startup")
def startup_event():
    try:
        if is_csv_mode():
            init_csv_storage()
            logger.info(f"Application started in CSV mode - Data path: {get_csv_data_path()}")
        else:
            create_tables()
            logger.info("Application started in DATABASE mode")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

# TO:
@app.on_event("startup")
def startup_event():
    try:
        create_tables()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
```

### Rollback `Development/.env`

**Remove these lines:**
```env
# Storage Configuration
STORAGE_MODE=csv
CSV_DATA_PATH=Development/data
```

---

## Data Migration (CSV to Database)

If you have data in CSV files that you want to migrate to the database:

### Option 1: Manual Migration Script

Create `migrate_csv_to_db.py`:

```python
"""
Migrate PII records from CSV to Database
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Temporarily set to database mode
os.environ['STORAGE_MODE'] = 'database'

from repository.PIIRepository import PIIRepository
from repository.CSVRepository import CSVRepository
from utility.database import SessionLocal

def migrate():
    # Read from CSV
    csv_repo = CSVRepository()
    csv_records = csv_repo.read_csv_records(csv_repo.csv_path)
    
    # Write to database
    db = SessionLocal()
    db_repo = PIIRepository(db)
    
    migrated = 0
    for record_data in csv_records:
        if record_data.get('is_active') != 'True':
            continue
            
        try:
            db_repo.save_pii_details(
                request_id=record_data['request_id'],
                assessment_id=record_data['assessment_id'],
                prospect_id=record_data['prospect_id'],
                input_type=record_data['input_type'],
                caller_name=record_data['caller_name'],
                country=record_data['country'],
                processed_document=record_data['processed_document'],
                output_text=record_data['output_text'],
                anonymizing_mapping=deserialize_json_from_csv(record_data['anonymizing_mapping']),
                encrypted_key=record_data['encrypted_key'],
                created_by=record_data['created_by']
            )
            migrated += 1
            print(f"✓ Migrated: {record_data['request_id']}")
        except Exception as e:
            print(f"✗ Failed: {record_data['request_id']} - {e}")
    
    db.close()
    print(f"\nMigration complete: {migrated} records migrated")

if __name__ == "__main__":
    migrate()
```

Run migration:
```bash
python migrate_csv_to_db.py
```

### Option 2: Keep Both (Recommended)

You can keep CSV files as backup and switch between modes as needed. The CSV files won't interfere with database operations.

---

## Verification Checklist

After rollback, verify:

- [ ] Application starts without errors
- [ ] Startup log shows "DATABASE mode"
- [ ] Database connection is successful
- [ ] `handle-pii` endpoint works
- [ ] `unmask-pii` endpoint works
- [ ] Data is being saved to database (check pii_details table)
- [ ] Data can be retrieved from database

---

## Troubleshooting

### Issue: "Failed to verify assessment" error

**Solution:** Update your database token in `.env`:
```env
LAKEBASE_PASSWORD=your-new-valid-token
```

### Issue: "No module named 'repository.CSVRepository'"

**Solution:** This is fine if you removed CSV files. Make sure you completed the full code rollback in Step "Complete Code Rollback".

### Issue: Database connection timeout

**Solution:** 
1. Check network connectivity to Databricks
2. Verify credentials are correct
3. Check if database is accessible

### Issue: Table doesn't exist

**Solution:** The application creates tables on startup. If it fails:
```python
from utility.database import create_tables
create_tables()
```

---

## Support

If you encounter issues during rollback:

1. Check application logs for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure database credentials are valid
4. Test database connectivity separately

---

## Summary

**Quick Rollback (No code changes):**
1. Set `STORAGE_MODE=database` in `.env`
2. Restart application
3. Done!

**Full Rollback (Remove CSV support):**
1. Revert changes in `PIIController.py`
2. Revert changes in `main.py`
3. Remove CSV configuration from `.env`
4. Optionally delete CSV-related files
5. Restart application

The dual-mode design allows you to switch between storage modes without code changes, making rollback simple and safe.
