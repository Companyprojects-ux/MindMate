"""
Reminder service.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.db.dynamodb import reminders_table, medications_table, create_item, get_item, update_item, delete_item, query_items
from backend.core.exceptions import NotFoundException
from backend.core.utils import generate_uuid, get_current_timestamp
from backend.schemas.reminder import ReminderStatus

async def create_reminder(user_id: str, reminder_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new reminder."""
    # Check if medication exists
    medication_id = reminder_data.get("medication_id")
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if not medication:
        raise NotFoundException(f"Medication with ID {medication_id} not found")
    
    reminder_data["user_id"] = user_id
    reminder = await create_item(reminders_table, reminder_data, "reminder_id", "user_id")
    
    # Add medication details to the response
    reminder["medication"] = medication
    
    return reminder

async def get_reminder(reminder_id: str, user_id: str) -> Dict[str, Any]:
    """Get a reminder by ID."""
    reminder = await get_item(reminders_table, reminder_id, "reminder_id", user_id, "user_id")
    if not reminder:
        raise NotFoundException(f"Reminder with ID {reminder_id} not found")
    
    # Get medication details
    medication_id = reminder.get("medication_id")
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if medication:
        reminder["medication"] = medication
    
    return reminder

async def update_reminder(reminder_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a reminder."""
    # Check if reminder exists
    reminder = await get_item(reminders_table, reminder_id, "reminder_id", user_id, "user_id")
    if not reminder:
        raise NotFoundException(f"Reminder with ID {reminder_id} not found")
    
    updated_reminder = await update_item(
        reminders_table,
        reminder_id,
        "reminder_id",
        update_data,
        user_id,
        "user_id"
    )
    
    # Get medication details
    medication_id = updated_reminder.get("medication_id")
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if medication:
        updated_reminder["medication"] = medication
    
    return updated_reminder

async def delete_reminder(reminder_id: str, user_id: str) -> None:
    """Delete a reminder."""
    # Check if reminder exists
    reminder = await get_item(reminders_table, reminder_id, "reminder_id", user_id, "user_id")
    if not reminder:
        raise NotFoundException(f"Reminder with ID {reminder_id} not found")
    
    await delete_item(reminders_table, reminder_id, "reminder_id", user_id, "user_id")

async def list_reminders(user_id: str) -> List[Dict[str, Any]]:
    """List all reminders for a user."""
    reminders = await query_items(
        reminders_table,
        "user_id = :user_id",
        {":user_id": user_id},
        "UserIdIndex"
    )
    
    # Get medication details for each reminder
    for reminder in reminders:
        medication_id = reminder.get("medication_id")
        medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
        if medication:
            reminder["medication"] = medication
    
    return reminders

async def get_today_reminders(user_id: str) -> List[Dict[str, Any]]:
    """Get today's reminders for a user."""
    # Get all reminders for the user
    reminders = await list_reminders(user_id)
    
    # Filter reminders for today
    today = datetime.utcnow().date()
    today_reminders = [
        reminder for reminder in reminders
        if datetime.fromisoformat(reminder["scheduled_time"].replace("Z", "+00:00")).date() == today
    ]
    
    # Sort by scheduled time
    today_reminders.sort(key=lambda r: r["scheduled_time"])
    
    return today_reminders

async def get_upcoming_reminders(user_id: str, days: int = 7) -> List[Dict[str, Any]]:
    """Get upcoming reminders for a user."""
    # Get all reminders for the user
    reminders = await list_reminders(user_id)
    
    # Filter upcoming reminders
    now = datetime.utcnow()
    end_date = now + timedelta(days=days)
    
    upcoming_reminders = [
        reminder for reminder in reminders
        if now <= datetime.fromisoformat(reminder["scheduled_time"].replace("Z", "+00:00")) <= end_date
    ]
    
    # Sort by scheduled time
    upcoming_reminders.sort(key=lambda r: r["scheduled_time"])
    
    return upcoming_reminders

async def update_reminder_status(reminder_id: str, user_id: str, status: ReminderStatus, notes: Optional[str] = None) -> Dict[str, Any]:
    """Update a reminder's status."""
    # Check if reminder exists
    reminder = await get_item(reminders_table, reminder_id, "reminder_id", user_id, "user_id")
    if not reminder:
        raise NotFoundException(f"Reminder with ID {reminder_id} not found")
    
    update_data = {"status": status}
    if notes is not None:
        update_data["notes"] = notes
    
    updated_reminder = await update_item(
        reminders_table,
        reminder_id,
        "reminder_id",
        update_data,
        user_id,
        "user_id"
    )
    
    # Get medication details
    medication_id = updated_reminder.get("medication_id")
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if medication:
        updated_reminder["medication"] = medication
    
    return updated_reminder
