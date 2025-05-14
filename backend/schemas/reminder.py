"""
Reminder schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class ReminderStatus(str, Enum):
    """Reminder status enum."""
    PENDING = "pending"
    COMPLETED = "completed"
    MISSED = "missed"
    SKIPPED = "skipped"

class ReminderBase(BaseModel):
    """Base reminder schema."""
    medication_id: str
    scheduled_time: str  # ISO format datetime
    status: ReminderStatus = ReminderStatus.PENDING
    notes: Optional[str] = None

class ReminderCreate(ReminderBase):
    """Reminder creation schema."""
    pass

class ReminderUpdate(BaseModel):
    """Reminder update schema."""
    scheduled_time: Optional[str] = None
    status: Optional[ReminderStatus] = None
    notes: Optional[str] = None

class ReminderResponse(ReminderBase):
    """Reminder response schema."""
    reminder_id: str
    user_id: str
    created_at: int
    updated_at: int
    medication: Optional[Dict[str, Any]] = None  # Medication details

class ReminderStatusUpdate(BaseModel):
    """Reminder status update schema."""
    status: ReminderStatus
    notes: Optional[str] = None
