"""
Main entry point for PII Anonymization API.
"""
from dotenv import load_dotenv
load_dotenv()  # Load .env before anything else

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.PIIController import router as pii_router
from utility.database import create_tables
from utility.storage_config import is_csv_mode, init_csv_storage, get_csv_data_path
import uvicorn
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PII Anonymization API",
    description=(
        "Detect and mask PII in PDF, DOC/DOCX, TXT, CSV, JSON, XLSX, "
        "images (PNG/JPG/TIFF/BMP), and web content. "
        "Country-specific PII rules for 14 countries."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pii_router, prefix="/v1", tags=["PII Processing"])


@app.on_event("startup")
def startup_event():
    try:
        if is_csv_mode():
            # Initialize CSV storage
            init_csv_storage()
            logger.info(f"Application started in CSV mode - Data path: {get_csv_data_path()}")
        else:
            # Initialize database
            create_tables()
            logger.info("Application started in DATABASE mode")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.get("/")
def root():
    return {"status": "success", "message": "PII Anonymization API is running", "version": "2.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "PII Anonymization API", "version": "2.0.0"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
