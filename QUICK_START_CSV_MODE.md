# Quick Start - CSV Storage Mode

## Start the API Server

```bash
cd Development
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     CSV storage initialized at: C:\...\Development\data
INFO:     Application started in CSV mode - Data path: C:\...\Development\data
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Test with Postman

1. **Import Collection**
   - Open Postman
   - Import `PII_API_Testing_Collection.json`

2. **Update Variables**
   - `assessment_id`: Any UUID (e.g., `a3097aef-06db-4568-a619-194e5b8c7d21`)
   - `prospect_id`: Any UUID (e.g., `b4097aef-06db-4568-a619-194e5b8c7d22`)
   - `base_url`: `http://localhost:8000/v1`

3. **Select a Test**
   - Navigate to: AMER Region Tests → Canada Tests → Canada - TXT
   - Click on Body tab
   - Click "Select File" for the `document` field
   - Choose: `c:\Users\KishorePonnurangam\generated_documents\AMER\Canada\AMER_Canada.txt`

4. **Send Request**
   - Click "Send"
   - You should get a 200 response with:
     ```json
     {
       "status": "success",
       "code": 200,
       "message": "TXT processed successfully",
       "data": {
         "request_id": "req_...",
         "processed_document": "/tmp/req_..._AMER_Canada_masked.txt",
         "entities_detected": 15,
         "country": "Canada",
         "processing_time_ms": 1234
       }
     }
     ```

## View Stored Data

```bash
# View CSV file
type Development\data\pii_records.csv

# Or open in Excel
start Development\data\pii_records.csv
```

## Test Unmask Endpoint

1. **Copy request_id** from previous response
2. **Select Unmask Request** in Postman (if you have one)
3. **Or create new request:**
   - Method: POST
   - URL: `http://localhost:8000/v1/unmask-pii`
   - Body (form-data):
     - `request_id`: (paste the request_id)
     - `input_type`: `txt`
     - `document`: (select the masked file from /tmp)

## Verify Data

Check the CSV file has your record:
```bash
python -c "from repository.CSVRepository import CSVRepository; repo = CSVRepository(); records = repo.get_pii_by_assessment('a3097aef-06db-4568-a619-194e5b8c7d21'); print(f'Found {len(records)} records')"
```

## Troubleshooting

### Server won't start
- Check if port 8000 is available
- Try: `python main.py` instead of uvicorn

### "Could not acquire file lock"
- Close any programs that might have the CSV file open (Excel, etc.)
- Delete `Development/data/pii_records.csv` and restart

### "Module not found"
- Install requirements: `pip install -r requirements.txt`

### Want to switch to Database mode?
- Edit `.env`: Change `STORAGE_MODE=csv` to `STORAGE_MODE=database`
- Update database credentials
- Restart server

## Success!

If you see records in the CSV file and can retrieve them via the unmask endpoint, everything is working! 🎉
