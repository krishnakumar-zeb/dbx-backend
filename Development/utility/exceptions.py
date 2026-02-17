"""
Custom exceptions for PII Anonymization API
"""

class PIIException(Exception):
    """Base exception for PII API"""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class InvalidInputTypeException(PIIException):
    """Exception for invalid input type"""
    def __init__(self, message: str = "Invalid input type provided"):
        super().__init__(message, code=400)


class DocumentProcessingException(PIIException):
    """Exception for document processing errors"""
    def __init__(self, message: str = "Failed to process document"):
        super().__init__(message, code=500)


class PresidioException(PIIException):
    """Exception for Presidio service errors"""
    def __init__(self, message: str = "PII detection failed"):
        super().__init__(message, code=500)


class DatabaseException(PIIException):
    """Exception for database operation errors"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, code=500)


class FileValidationException(PIIException):
    """Exception for file validation errors"""
    def __init__(self, message: str = "File validation failed"):
        super().__init__(message, code=400)


class AssessmentNotFoundException(PIIException):
    """Exception when assessment is not found"""
    def __init__(self, message: str = "Assessment not found"):
        super().__init__(message, code=404)


class ServiceUnavailableException(PIIException):
    """Exception when service is unavailable"""
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(message, code=503)


class GatewayTimeoutException(PIIException):
    """Exception for request timeout"""
    def __init__(self, message: str = "Request processing timeout"):
        super().__init__(message, code=504)


class PayloadTooLargeException(PIIException):
    """Exception when file size exceeds limit"""
    def __init__(self, message: str = "File size exceeds maximum allowed limit"):
        super().__init__(message, code=413)
