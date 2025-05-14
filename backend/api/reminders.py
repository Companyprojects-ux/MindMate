"""
Reminder API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from backend.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse, ReminderStatusUpdate
from backend.services import reminder_service
from backend.core.dependencies import get_current_user
from backend.core.exceptions import NotFoundException

router = APIRouter()

@router.post("", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    reminder_data: ReminderCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new reminder."""
    try:
        reminder = await reminder_service.create_reminder(
            current_user["user_id"],
            reminder_data.dict()
        )
        return reminder
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("", response_model=List[ReminderResponse])
async def list_reminders(
    current_user: dict = Depends(get_current_user)
):
    """List all reminders for the current user."""
    reminders = await reminder_service.list_reminders(current_user["user_id"])
    return reminders

@router.get("/today", response_model=List[ReminderResponse])
async def get_today_reminders(
    current_user: dict = Depends(get_current_user)
):
    """Get today's reminders for the current user."""
    reminders = await reminder_service.get_today_reminders(current_user["user_id"])
    return reminders

@router.get("/upcoming", response_model=List[ReminderResponse])
async def get_upcoming_reminders(
    days: int = Query(7, ge=1, le=30),
    current_user: dict = Depends(get_current_user)
):
    """Get upcoming reminders for the current user."""
    reminders = await reminder_service.get_upcoming_reminders(current_user["user_id"], days)
    return reminders

@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a reminder by ID."""
    try:
        reminder = await reminder_service.get_reminder(reminder_id, current_user["user_id"])
        return reminder
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: str,
    reminder_data: ReminderUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a reminder."""
    try:
        updated_reminder = await reminder_service.update_reminder(
            reminder_id,
            current_user["user_id"],
            reminder_data.dict(exclude_unset=True)
        )
        return updated_reminder
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{reminder_id}/status", response_model=ReminderResponse)
async def update_reminder_status(
    reminder_id: str,
    status_data: ReminderStatusUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a reminder's status."""
    try:
        updated_reminder = await reminder_service.update_reminder_status(
            reminder_id,
            current_user["user_id"],
            status_data.status,
            status_data.notes
        )
        return updated_reminder
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    reminder_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a reminder."""
    try:
        await reminder_service.delete_reminder(reminder_id, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
