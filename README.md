# PII Anonymization API

A FastAPI-based service for detecting and anonymizing Personally Identifiable Information (PII) in documents across multiple formats and countries.

## 🚀 Features

- **Multi-Format Support**: PDF, DOCX, DOC, TXT, CSV, XLSX, JSON, Images (PNG, JPG, TIFF, BMP)
- **Country-Specific PII Detection**: 14+ countries including US, Canada, UK, India, Australia, etc.
- **Dual Storage Mode**: CSV (for development) or Database (for production)
- **Encryption**: AES-CBC encryption for sensitive data
- **Unmask Capability**: Restore original PII from anonymized documents
- **RESTful API**: Easy integration with any application

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (for database mode)
- Tesseract OCR (for image processing)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Updated_PII_Implementation_Code
   ```

2. **Install dependencies**
   ```bash
   cd Development
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the server**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

## ⚙️ Configuration

### Storage Modes

**CSV Mode (Default - No Database Required)**
```env
STORAGE_MODE=csv
```

**Database Mode**
```env
STORAGE_MODE=database
LAKEBASE_USERNAME=your-username
LAKEBASE_PASSWORD=your-password
LAKEBASE_HOST=your-host
```

See [QUICK_START_CSV_MODE.md](QUICK_START_CSV_MODE.md) for detailed setup.

## 📚 API Endpoints

### Anonymize Document
```http
POST /v1/handle-pii
Content-Type: multipart/form-data

Parameters:
- assessment_id: UUID (required)
- prospect_id: UUID (required)
- caller_name: string (required)
- input_type: string (optional - auto-detected)
- company_name: string (optional - for country detection)
- company_website: string (optional)
- document: file (required)
```

### De-anonymize Document
```http
POST /v1/unmask-pii
Content-Type: multipart/form-data

Parameters:
- request_id: string (required - from anonymize response)
- input_type: string (required)
- document: file (required - the masked document)
```

## 🧪 Testing

Import the Postman collection:
```
PII_API_Testing_Collection.json
```

See [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) for comprehensive testing guide.

## 📖 Documentation

- [Quick Start Guide](QUICK_START_CSV_MODE.md)
- [CSV Migration Complete](CSV_MIGRATION_COMPLETE.md)
- [Rollback Guide](CSV_TO_DATABASE_ROLLBACK_GUIDE.md)
- [Migration Summary](MIGRATION_SUMMARY.md)
- [Windows Temp Fix](WINDOWS_TEMP_FIX.md)

## 🏗️ Architecture

```
Development/
├── controllers/     # API endpoints
├── services/        # Business logic for each file type
├── repository/      # Data access layer (CSV & Database)
├── utility/         # Helper functions, PII detection, encryption
└── data/           # CSV storage (gitignored)
```

## 🌍 Supported Countries

- **AMER**: US, Canada, Mexico
- **APJ**: Australia, India, Japan, Malaysia, Singapore
- **EMEA**: UK, France, Germany, Saudi Arabia, UAE, South Africa

## 🔒 Security

- ✅ `.env` file excluded from git
- ✅ AES-CBC encryption for PII data
- ✅ CSV data files gitignored
- ✅ Secure token handling

**⚠️ Important**: Never commit `.env` files or CSV data files to version control.

## 🤝 Contributing

This is a private repository. For access or contributions, contact the repository owner.

## 📝 License

[Specify your license here]

## 👥 Team

Developed by [Your Team Name]

## 📞 Support

For issues or questions, please contact [your-email@example.com]

---

**Note**: This project uses Presidio for PII detection. See `Presdio/` folder for Presidio-related code and documentation.
