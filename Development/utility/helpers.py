"""Shared helper functions."""
import uuid


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return f"req_{uuid.uuid4().hex[:24]}"
