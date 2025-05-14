"""
Medication schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MedicationBase(BaseModel):
    """Base medication schema."""
    name: str
    dosage: str
    frequency: str  # daily, twice daily, etc.
    time_of_day: Optional[str] = None  # morning, afternoon, evening, etc.
    specific_times: Optional[List[str]] = None  # List of specific times
    start_date: str  # ISO format date
    end_date: Optional[str] = None  # ISO format date
    notes: Optional[str] = None
    medication_type: Optional[str] = None  # pill, liquid, injection, etc.
    image_url: Optional[str] = None

class MedicationCreate(MedicationBase):
    """Medication creation schema."""
    pass

class MedicationUpdate(BaseModel):
    """Medication update schema."""
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    time_of_day: Optional[str] = None
    specific_times: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None
    medication_type: Optional[str] = None
    image_url: Optional[str] = None

class MedicationResponse(MedicationBase):
    """Medication response schema."""
    medication_id: str
    user_id: str
    created_at: int
    updated_at: int
