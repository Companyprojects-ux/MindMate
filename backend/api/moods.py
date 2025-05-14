"""
Mood tracking API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from backend.schemas.mood import MoodCreate, MoodUpdate, MoodResponse, MoodStats
from backend.services import mood_service
from backend.core.dependencies import get_current_user
from backend.core.exceptions import NotFoundException

router = APIRouter()

@router.post("", response_model=MoodResponse, status_code=status.HTTP_201_CREATED)
async def create_mood_entry(
    mood_data: MoodCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new mood entry."""
    mood_entry = await mood_service.create_mood_entry(
        current_user["user_id"],
        mood_data.model_dump()
    )
    return mood_entry

@router.get("", response_model=List[MoodResponse])
async def list_mood_entries(
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """List mood entries for the current user."""
    mood_entries = await mood_service.list_mood_entries(
        current_user["user_id"],
        limit,
        start_date,
        end_date
    )
    return mood_entries

@router.get("/stats", response_model=MoodStats)
async def get_mood_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user: dict = Depends(get_current_user)
):
    """Get mood statistics for the current user."""
    stats = await mood_service.get_mood_statistics(current_user["user_id"], days)
    return stats

@router.get("/{entry_id}", response_model=MoodResponse)
async def get_mood_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a mood entry by ID."""
    try:
        mood_entry = await mood_service.get_mood_entry(entry_id, current_user["user_id"])
        return mood_entry
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{entry_id}", response_model=MoodResponse)
async def update_mood_entry(
    entry_id: str,
    mood_data: MoodUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a mood entry."""
    try:
        updated_mood_entry = await mood_service.update_mood_entry(
            entry_id,
            current_user["user_id"],
            mood_data.dict(exclude_unset=True)
        )
        return updated_mood_entry
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a mood entry."""
    try:
        await mood_service.delete_mood_entry(entry_id, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
