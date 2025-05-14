"""
Mood tracking service.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.db.dynamodb import mood_entries_table, create_item, get_item, update_item, delete_item, query_items
from backend.core.exceptions import NotFoundException
from backend.core.utils import generate_uuid, get_current_timestamp
from collections import Counter

async def create_mood_entry(user_id: str, mood_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new mood entry."""
    # Set timestamp to current time if not provided
    if not mood_data.get("timestamp"):
        mood_data["timestamp"] = datetime.utcnow().isoformat()
    
    mood_data["user_id"] = user_id
    mood_entry = await create_item(mood_entries_table, mood_data, "entry_id", "user_id")
    return mood_entry

async def get_mood_entry(entry_id: str, user_id: str) -> Dict[str, Any]:
    """Get a mood entry by ID."""
    mood_entry = await get_item(mood_entries_table, entry_id, "entry_id", user_id, "user_id")
    if not mood_entry:
        raise NotFoundException(f"Mood entry with ID {entry_id} not found")
    return mood_entry

async def update_mood_entry(entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a mood entry."""
    # Check if mood entry exists
    mood_entry = await get_item(mood_entries_table, entry_id, "entry_id", user_id, "user_id")
    if not mood_entry:
        raise NotFoundException(f"Mood entry with ID {entry_id} not found")
    
    updated_mood_entry = await update_item(
        mood_entries_table,
        entry_id,
        "entry_id",
        update_data,
        user_id,
        "user_id"
    )
    
    return updated_mood_entry

async def delete_mood_entry(entry_id: str, user_id: str) -> None:
    """Delete a mood entry."""
    # Check if mood entry exists
    mood_entry = await get_item(mood_entries_table, entry_id, "entry_id", user_id, "user_id")
    if not mood_entry:
        raise NotFoundException(f"Mood entry with ID {entry_id} not found")
    
    await delete_item(mood_entries_table, entry_id, "entry_id", user_id, "user_id")

async def list_mood_entries(user_id: str, limit: int = 100, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """List mood entries for a user."""
    # Get all mood entries for the user
    mood_entries = await query_items(
        mood_entries_table,
        "user_id = :user_id",
        {":user_id": user_id},
        "UserIdIndex"
    )
    
    # Filter by date range if provided
    if start_date or end_date:
        filtered_entries = []
        start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00")) if start_date else None
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00")) if end_date else None
        
        for entry in mood_entries:
            entry_dt = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if (not start_dt or entry_dt >= start_dt) and (not end_dt or entry_dt <= end_dt):
                filtered_entries.append(entry)
        
        mood_entries = filtered_entries
    
    # Sort by timestamp (newest first)
    mood_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Apply limit
    return mood_entries[:limit]

async def get_mood_statistics(user_id: str, days: int = 30) -> Dict[str, Any]:
    """Get mood statistics for a user."""
    # Get mood entries for the specified period
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    mood_entries = await list_mood_entries(
        user_id,
        limit=1000,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )
    
    if not mood_entries:
        return {
            "average_rating": 0,
            "highest_rating": 0,
            "lowest_rating": 0,
            "most_common_tags": [],
            "mood_trend": [],
            "total_entries": 0
        }
    
    # Calculate statistics
    ratings = [entry["mood_rating"] for entry in mood_entries]
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    highest_rating = max(ratings) if ratings else 0
    lowest_rating = min(ratings) if ratings else 0
    
    # Collect all tags
    all_tags = []
    for entry in mood_entries:
        if entry.get("tags"):
            all_tags.extend(entry["tags"])
    
    # Get most common tags
    tag_counter = Counter(all_tags)
    most_common_tags = [{"tag": tag, "count": count} for tag, count in tag_counter.most_common(5)]
    
    # Calculate mood trend (average rating per day)
    mood_trend = []
    date_ratings = {}
    
    for entry in mood_entries:
        entry_date = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")).date().isoformat()
        if entry_date not in date_ratings:
            date_ratings[entry_date] = {"sum": 0, "count": 0}
        
        date_ratings[entry_date]["sum"] += entry["mood_rating"]
        date_ratings[entry_date]["count"] += 1
    
    for date, data in sorted(date_ratings.items()):
        avg_rating = data["sum"] / data["count"]
        mood_trend.append({"date": date, "average_rating": avg_rating})
    
    return {
        "average_rating": average_rating,
        "highest_rating": highest_rating,
        "lowest_rating": lowest_rating,
        "most_common_tags": most_common_tags,
        "mood_trend": mood_trend,
        "total_entries": len(mood_entries)
    }
