"""
Journal schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class JournalBase(BaseModel):
    """Base journal entry schema."""
    title: str
    content: str
    tags: Optional[List[str]] = None
    timestamp: Optional[str] = None  # ISO format datetime, defaults to current time if not provided

class JournalCreate(JournalBase):
    """Journal entry creation schema."""
    pass

class JournalUpdate(BaseModel):
    """Journal entry update schema."""
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class JournalResponse(JournalBase):
    """Journal entry response schema."""
    entry_id: str
    user_id: str
    created_at: int
    updated_at: int
