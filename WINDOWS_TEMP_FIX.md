# Windows Temp Directory Fix

## Issue

The original code used `/tmp/` for temporary files, which doesn't exist on Windows, causing:
```
[Errno 2] No such file or directory: '/tmp/req_..._original.pdf'
```

## Fix Applied

### Files Modified

**1. Development/services/BaseService.py**
- Added `import tempfile`
- Changed: `temp_path = f"/tmp/{request_id}_original{ext}"`
- To: `temp_path = os.path.join(tempfile.gettempdir(), f"{request_id}_original{ext}")`
- Changed: `out_path = f"/tmp/{request_id}_{masked_name}"`
- To: `out_path = os.path.join(tempfile.gettempdir(), f"{request_id}_{masked_name}")`

**2. Development/services/UnmaskService.py**
- Added `import tempfile`
- Changed: `temp_path = f"/tmp/{request_id}_masked.{input_type}"`
- To: `temp_path = os.path.join(tempfile.gettempdir(), f"{request_id}_masked.{input_type}")`
- Changed: `out_path = f"/tmp/{request_id}_unmasked.{input_type}"`
- To: `out_path = os.path.join(tempfile.gettempdir(), f"{request_id}_unmasked.{input_type}")`

## Result

Temp files now use the system temp directory:
- **Windows**: `C:\Users\<username>\AppData\Local\Temp\`
- **Linux/Mac**: `/tmp/`

## Testing

Restart your server and test again:

```bash
cd Development
python main.py
```

Then test with Postman - the error should be resolved!

## Temp File Locations

After processing, you can find temp files at:

**Windows:**
```
C:\Users\KishorePonnurangam\AppData\Local\Temp\req_*_masked.*
```

**To view temp directory:**
```python
import tempfile
print(tempfile.gettempdir())
```

## Cleanup

Temp files are automatically cleaned up after processing, but you can manually clean if needed:

**Windows:**
```cmd
del %TEMP%\req_*.*
```

**Linux/Mac:**
```bash
rm /tmp/req_*
```
