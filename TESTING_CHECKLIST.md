# Testing Checklist - CSV Storage Mode

## Pre-Testing Setup

- [ ] Verify `STORAGE_MODE=csv` in `Development/.env`
- [ ] Ensure `Development/data/` folder exists
- [ ] Close any Excel/editors that might lock CSV files
- [ ] Install dependencies: `pip install -r requirements.txt`

---

## Server Startup

- [ ] Navigate to Development folder: `cd Development`
- [ ] Start server: `python main.py`
- [ ] Verify startup message shows "CSV mode"
- [ ] Check server is running on http://localhost:8000
- [ ] Test health endpoint: http://localhost:8000/health

**Expected Output:**
```
INFO: Application started in CSV mode - Data path: C:\...\Development\data
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## API Testing with Postman

### Setup
- [ ] Import `PII_API_Testing_Collection.json` into Postman
- [ ] Set variables:
  - `base_url`: `http://localhost:8000/v1`
  - `assessment_id`: `a3097aef-06db-4568-a619-194e5b8c7d21`
  - `prospect_id`: `b4097aef-06db-4568-a619-194e5b8c7d22`
  - `caller_name`: `postman-test`

### Test 1: Handle PII - TXT File
- [ ] Select: AMER → Canada → Canada - TXT
- [ ] Click Body tab
- [ ] Click "Select File" for `document` field
- [ ] Choose: `generated_documents\AMER\Canada\AMER_Canada.txt`
- [ ] Click "Send"
- [ ] Verify response status: 200
- [ ] Verify response has `request_id`
- [ ] Copy `request_id` for unmask test

**Expected Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "TXT processed successfully",
  "data": {
    "request_id": "req_...",
    "processed_document": "/tmp/..._masked.txt",
    "entities_detected": 10,
    "country": "Canada",
    "processing_time_ms": 500
  }
}
```

### Test 2: Handle PII - PDF File
- [ ] Select: AMER → Canada → Canada - PDF
- [ ] Select file: `generated_documents\AMER\Canada\AMER_Canada.pdf`
- [ ] Click "Send"
- [ ] Verify response status: 200
- [ ] Verify entities detected > 0

### Test 3: Handle PII - DOCX File
- [ ] Select: AMER → Canada → Canada - DOCX
- [ ] Select file: `generated_documents\AMER\Canada\AMER_Canada.docx`
- [ ] Click "Send"
- [ ] Verify response status: 200

### Test 4: Handle PII - DOC File
- [ ] Select: AMER → Canada → Canada - DOC
- [ ] Select file: `generated_documents\AMER\Canada\AMER_Canada.doc`
- [ ] Click "Send"
- [ ] Verify response status: 200

### Test 5: Handle PII - CSV File
- [ ] Select: AMER → Canada → Canada - CSV
- [ ] Select file: `generated_documents\AMER\Canada\AMER_Canada.csv`
- [ ] Click "Send"
- [ ] Verify response status: 200

### Test 6: Handle PII - XLSX File
- [ ] Select: AMER → Canada → Canada - XLSX
- [ ] Select file: `generated_documents\AMER\Canada\AMER_Canada.xlsx`
- [ ] Click "Send"
- [ ] Verify response status: 200

### Test 7: Different Countries
- [ ] Test US: AMER → US → US - TXT
- [ ] Test Mexico: AMER → Mexico → Mexico - TXT
- [ ] Test India: APJ → India → India - TXT
- [ ] Test UK: EMEA → UK → UK - TXT
- [ ] Verify each returns correct country in response

---

## CSV File Verification

### Check CSV File Created
- [ ] Navigate to: `Development\data\`
- [ ] Verify `pii_records.csv` exists
- [ ] Open in text editor or Excel

### Verify CSV Contents
- [ ] Check headers are present (15 columns)
- [ ] Verify records exist (one per API call)
- [ ] Check `request_id` matches API responses
- [ ] Verify `anonymizing_mapping` contains JSON
- [ ] Check `encrypted_key` is populated
- [ ] Verify `is_active` is "True"

**CSV Columns:**
```
request_id, assessment_id, prospect_id, input_type, caller_name, country,
processed_document, output_text, anonymizing_mapping, encrypted_key,
created_at, created_by, modified_at, modified_by, is_active
```

---

## Unmask Testing

### Test 8: Unmask Document
- [ ] Get `request_id` from Test 1
- [ ] Get masked file path from Test 1 response
- [ ] Create new POST request to: `http://localhost:8000/v1/unmask-pii`
- [ ] Body (form-data):
  - `request_id`: (paste request_id)
  - `input_type`: `txt`
  - `document`: (select masked file from /tmp)
- [ ] Click "Send"
- [ ] Verify response status: 200
- [ ] Verify `unmasked_document` path returned
- [ ] Check unmasked file exists

**Expected Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "TXT de-anonymised successfully",
  "data": {
    "request_id": "req_...",
    "unmasked_document": "/tmp/..._unmasked.txt",
    "tags_replaced": 10,
    "processing_time_ms": 200
  }
}
```

---

## Data Retrieval Testing

### Test 9: Query CSV Repository
```bash
cd Development
python -c "from repository.CSVRepository import CSVRepository; repo = CSVRepository(); record = repo.get_pii_details('req_...'); print('Found:', record.request_id if record else 'Not found')"
```
- [ ] Replace `req_...` with actual request_id
- [ ] Verify record is found

### Test 10: Query by Assessment
```bash
python -c "from repository.CSVRepository import CSVRepository; repo = CSVRepository(); records = repo.get_pii_by_assessment('a3097aef-06db-4568-a619-194e5b8c7d21'); print(f'Found {len(records)} records')"
```
- [ ] Verify count matches number of API calls made

---

## Error Handling Testing

### Test 11: Invalid Request ID
- [ ] Call unmask-pii with non-existent request_id
- [ ] Verify error response returned
- [ ] Check error message is descriptive

### Test 12: Missing Required Fields
- [ ] Call handle-pii without `prospect_id`
- [ ] Verify 422 validation error
- [ ] Check error details field names

### Test 13: Invalid File Type
- [ ] Call handle-pii with `input_type=invalid`
- [ ] Verify error response
- [ ] Check error message mentions supported types

---

## Performance Testing

### Test 14: Multiple Concurrent Requests
- [ ] Use Postman Runner or Collection Runner
- [ ] Run 5-10 requests simultaneously
- [ ] Verify all complete successfully
- [ ] Check CSV file has all records
- [ ] Verify no file lock errors

---

## Cleanup and Verification

### Final Checks
- [ ] Check server logs for errors
- [ ] Verify all masked files created in /tmp
- [ ] Count CSV records matches API calls
- [ ] No duplicate request_ids in CSV
- [ ] All records have `is_active=True`

### Cleanup (Optional)
- [ ] Delete test records from CSV
- [ ] Delete masked files from /tmp
- [ ] Or keep for reference

---

## Database Mode Testing (Optional)

### Test 15: Switch to Database Mode
- [ ] Stop server
- [ ] Edit `.env`: `STORAGE_MODE=database`
- [ ] Update database credentials
- [ ] Start server
- [ ] Verify startup shows "DATABASE mode"
- [ ] Test one API call
- [ ] Verify data saved to database

### Test 16: Switch Back to CSV
- [ ] Stop server
- [ ] Edit `.env`: `STORAGE_MODE=csv`
- [ ] Start server
- [ ] Verify startup shows "CSV mode"
- [ ] Test one API call
- [ ] Verify data saved to CSV

---

## Issue Tracking

### Issues Found
| Test # | Issue Description | Severity | Status |
|--------|------------------|----------|--------|
|        |                  |          |        |

### Notes
```
Add any observations, performance notes, or suggestions here.
```

---

## Sign-Off

- [ ] All critical tests passed
- [ ] CSV file structure verified
- [ ] API responses correct
- [ ] Error handling works
- [ ] Documentation reviewed
- [ ] Ready for use

**Tested By:** _______________  
**Date:** _______________  
**Status:** ⬜ Pass / ⬜ Fail / ⬜ Needs Review

---

## Quick Reference

**Start Server:**
```bash
cd Development
python main.py
```

**View CSV:**
```bash
type Development\data\pii_records.csv
```

**Test API:**
```bash
curl -X POST http://localhost:8000/v1/handle-pii \
  -F "assessment_id=a3097aef-06db-4568-a619-194e5b8c7d21" \
  -F "prospect_id=b4097aef-06db-4568-a619-194e5b8c7d22" \
  -F "caller_name=test" \
  -F "input_type=txt" \
  -F "document=@test.txt"
```

**Health Check:**
```
http://localhost:8000/health
```

---

**Happy Testing! 🚀**
