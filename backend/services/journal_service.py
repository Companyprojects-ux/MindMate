"""
Journal service.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.db.dynamodb import journal_entries_table, create_item, get_item, update_item, delete_item, query_items
from backend.core.exceptions import NotFoundException
from backend.core.utils import generate_uuid, get_current_timestamp

async def create_journal_entry(user_id: str, journal_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new journal entry."""
    # Set timestamp to current time if not provided
    if not journal_data.get("timestamp"):
        journal_data["timestamp"] = datetime.utcnow().isoformat()
    
    journal_data["user_id"] = user_id
    journal_entry = await create_item(journal_entries_table, journal_data, "entry_id", "user_id")
    return journal_entry

async def get_journal_entry(entry_id: str, user_id: str) -> Dict[str, Any]:
    """Get a journal entry by ID."""
    journal_entry = await get_item(journal_entries_table, entry_id, "entry_id", user_id, "user_id")
    if not journal_entry:
        raise NotFoundException(f"Journal entry with ID {entry_id} not found")
    return journal_entry

async def update_journal_entry(entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a journal entry."""
    # Check if journal entry exists
    journal_entry = await get_item(journal_entries_table, entry_id, "entry_id", user_id, "user_id")
    if not journal_entry:
        raise NotFoundException(f"Journal entry with ID {entry_id} not found")
    
    updated_journal_entry = await update_item(
        journal_entries_table,
        entry_id,
        "entry_id",
        update_data,
        user_id,
        "user_id"
    )
    
    return updated_journal_entry

async def delete_journal_entry(entry_id: str, user_id: str) -> None:
    """Delete a journal entry."""
    # Check if journal entry exists
    journal_entry = await get_item(journal_entries_table, entry_id, "entry_id", user_id, "user_id")
    if not journal_entry:
        raise NotFoundException(f"Journal entry with ID {entry_id} not found")
    
    await delete_item(journal_entries_table, entry_id, "entry_id", user_id, "user_id")

async def list_journal_entries(user_id: str, limit: int = 100, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """List journal entries for a user."""
    # Get all journal entries for the user
    journal_entries = await query_items(
        journal_entries_table,
        "user_id = :user_id",
        {":user_id": user_id},
        "UserIdIndex"
    )
    
    # Filter by date range if provided
    if start_date or end_date:
        filtered_entries = []
        start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00")) if start_date else None
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00")) if end_date else None
        
        for entry in journal_entries:
            entry_dt = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if (not start_dt or entry_dt >= start_dt) and (not end_dt or entry_dt <= end_dt):
                filtered_entries.append(entry)
        
        journal_entries = filtered_entries
    
    # Sort by timestamp (newest first)
    journal_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Apply limit
    return journal_entries[:limit]

async def search_journal_entries(user_id: str, query: str, tags: Optional[List[str]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Search journal entries by content or tags."""
    # Get all journal entries for the user
    journal_entries = await list_journal_entries(user_id, limit=1000)
    
    # Filter by search query and tags
    filtered_entries = []
    query = query.lower() if query else ""
    
    for entry in journal_entries:
        # Check if entry matches search query
        matches_query = (
            not query or
            query in entry.get("title", "").lower() or
            query in entry.get("content", "").lower()
        )
        
        # Check if entry has all required tags
        matches_tags = True
        if tags:
            entry_tags = entry.get("tags", [])
            for tag in tags:
                if tag not in entry_tags:
                    matches_tags = False
                    break
        
        if matches_query and matches_tags:
            filtered_entries.append(entry)
    
    # Apply limit
    return filtered_entries[:limit]
