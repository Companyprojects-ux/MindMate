"""
Utility functions for the application.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())

def get_current_timestamp() -> int:
    """Get the current timestamp as an integer."""
    return int(datetime.utcnow().timestamp())

def format_datetime(dt: datetime) -> str:
    """Format a datetime object as an ISO string."""
    return dt.isoformat()

def parse_datetime(dt_str: str) -> datetime:
    """Parse an ISO datetime string into a datetime object."""
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

def clean_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from a dictionary."""
    return {k: v for k, v in data.items() if v is not None}
