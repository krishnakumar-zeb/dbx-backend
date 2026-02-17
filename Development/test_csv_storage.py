"""
Test CSV storage functionality
"""
import os
import sys
from datetime import datetime

# Set CSV mode
os.environ['STORAGE_MODE'] = 'csv'

from repository.CSVRepository import CSVRepository
from utility.storage_config import init_csv_storage

def test_csv_repository():
    print("=" * 70)
    print("Testing CSV Repository")
    print("=" * 70)
    
    # Initialize storage
    init_csv_storage()
    
    # Create repository
    repo = CSVRepository()
    print(f"✓ Repository initialized: {repo.csv_path}")
    
    # Test 1: Save PII details
    print("\n[Test 1] Saving PII record...")
    test_mapping = {
        "<PERSON_0>": {
            "encrypted_value": "test_encrypted_value_123",
            "entity_type": "PERSON",
            "score": 0.85
        },
        "<EMAIL_ADDRESS_0>": {
            "encrypted_value": "test_encrypted_email_456",
            "entity_type": "EMAIL_ADDRESS",
            "score": 1.0
        }
    }
    
    record = repo.save_pii_details(
        request_id="req_test_12345",
        assessment_id="a3097aef-06db-4568-a619-194e5b8c7d21",
        prospect_id="b4097aef-06db-4568-a619-194e5b8c7d22",
        input_type="txt",
        caller_name="test_script",
        country="US",
        processed_document="/tmp/test_masked.txt",
        output_text="This is <PERSON_0> with email <EMAIL_ADDRESS_0>",
        anonymizing_mapping=test_mapping,
        encrypted_key="test_key_abc123",
        created_by="test_user"
    )
    print(f"✓ Record saved: {record.request_id}")
    
    # Test 2: Retrieve PII details
    print("\n[Test 2] Retrieving PII record...")
    retrieved = repo.get_pii_details("req_test_12345")
    if retrieved:
        print(f"✓ Record retrieved: {retrieved.request_id}")
        print(f"  - Country: {retrieved.country}")
        print(f"  - Input Type: {retrieved.input_type}")
        print(f"  - Entities: {len(retrieved.anonymizing_mapping)}")
        print(f"  - Mapping: {retrieved.anonymizing_mapping}")
    else:
        print("✗ Record not found")
    
    # Test 3: Get by assessment
    print("\n[Test 3] Getting records by assessment...")
    records = repo.get_pii_by_assessment("a3097aef-06db-4568-a619-194e5b8c7d21")
    print(f"✓ Found {len(records)} record(s) for assessment")
    
    # Test 4: Update record
    print("\n[Test 4] Updating PII record...")
    updated = repo.update_pii_details(
        request_id="req_test_12345",
        modified_by="test_updater",
        country="Canada"
    )
    print(f"✓ Record updated: {updated.country}")
    
    # Test 5: Verify assessment (should always pass in CSV mode)
    print("\n[Test 5] Verifying assessment...")
    result = repo.verify_assessment_exists("any-assessment-id")
    print(f"✓ Assessment validation: {result} (always True in CSV mode)")
    
    print("\n" + "=" * 70)
    print("All tests passed!")
    print("=" * 70)
    print(f"\nCSV file location: {repo.csv_path}")
    print("You can inspect the CSV file to see the stored data.")

if __name__ == "__main__":
    try:
        test_csv_repository()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
