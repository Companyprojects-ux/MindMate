"""
Journal API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from backend.schemas.journal import JournalCreate, JournalUpdate, JournalResponse
from backend.services import journal_service
from backend.core.dependencies import get_current_user
from backend.core.exceptions import NotFoundException

router = APIRouter()

@router.post("", response_model=JournalResponse, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    journal_data: JournalCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new journal entry."""
    journal_entry = await journal_service.create_journal_entry(
        current_user["user_id"],
        journal_data.dict()
    )
    return journal_entry

@router.get("", response_model=List[JournalResponse])
async def list_journal_entries(
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """List journal entries for the current user."""
    journal_entries = await journal_service.list_journal_entries(
        current_user["user_id"],
        limit,
        start_date,
        end_date
    )
    return journal_entries

@router.get("/search", response_model=List[JournalResponse])
async def search_journal_entries(
    query: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user)
):
    """Search journal entries by content or tags."""
    journal_entries = await journal_service.search_journal_entries(
        current_user["user_id"],
        query,
        tags,
        limit
    )
    return journal_entries

@router.get("/{entry_id}", response_model=JournalResponse)
async def get_journal_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a journal entry by ID."""
    try:
        journal_entry = await journal_service.get_journal_entry(entry_id, current_user["user_id"])
        return journal_entry
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{entry_id}", response_model=JournalResponse)
async def update_journal_entry(
    entry_id: str,
    journal_data: JournalUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a journal entry."""
    try:
        updated_journal_entry = await journal_service.update_journal_entry(
            entry_id,
            current_user["user_id"],
            journal_data.dict(exclude_unset=True)
        )
        return updated_journal_entry
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a journal entry."""
    try:
        await journal_service.delete_journal_entry(entry_id, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
