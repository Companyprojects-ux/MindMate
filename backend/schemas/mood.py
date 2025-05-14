"""
Mood tracking schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MoodBase(BaseModel):
    """Base mood entry schema."""
    mood_rating: int = Field(..., ge=1, le=10)
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    timestamp: Optional[str] = None  # ISO format datetime, defaults to current time if not provided

class MoodCreate(MoodBase):
    """Mood entry creation schema."""
    pass

class MoodUpdate(BaseModel):
    """Mood entry update schema."""
    mood_rating: Optional[int] = Field(None, ge=1, le=10)
    tags: Optional[List[str]] = None
    notes: Optional[str] = None

class MoodResponse(MoodBase):
    """Mood entry response schema."""
    entry_id: str
    user_id: str
    created_at: int
    updated_at: int

class MoodStats(BaseModel):
    """Mood statistics schema."""
    average_rating: float
    highest_rating: int
    lowest_rating: int
    most_common_tags: List[Dict[str, Any]]
    mood_trend: List[Dict[str, Any]]
    total_entries: int
