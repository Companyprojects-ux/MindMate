"""
Medication service.
"""
from typing import List, Dict, Any, Optional
from backend.db.dynamodb import medications_table, create_item, get_item, update_item, delete_item, query_items
from backend.core.exceptions import NotFoundException
from backend.db.s3 import upload_file, delete_file, generate_presigned_url
from backend.core.utils import generate_uuid
import uuid

async def create_medication(user_id: str, medication_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new medication."""
    medication_data["user_id"] = user_id
    medication = await create_item(medications_table, medication_data, "medication_id", "user_id")
    return medication

async def get_medication(medication_id: str, user_id: str) -> Dict[str, Any]:
    """Get a medication by ID."""
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if not medication:
        raise NotFoundException(f"Medication with ID {medication_id} not found")
    return medication

async def update_medication(medication_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a medication."""
    # Check if medication exists
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if not medication:
        raise NotFoundException(f"Medication with ID {medication_id} not found")
    
    updated_medication = await update_item(
        medications_table,
        medication_id,
        "medication_id",
        update_data,
        user_id,
        "user_id"
    )
    
    return updated_medication

async def delete_medication(medication_id: str, user_id: str) -> None:
    """Delete a medication."""
    # Check if medication exists
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if not medication:
        raise NotFoundException(f"Medication with ID {medication_id} not found")
    
    # Delete medication image if exists
    if medication.get("image_url"):
        try:
            # Extract object name from URL
            object_name = medication["image_url"].split("/")[-1]
            await delete_file(object_name)
        except Exception:
            # Continue even if image deletion fails
            pass
    
    await delete_item(medications_table, medication_id, "medication_id", user_id, "user_id")

async def list_medications(user_id: str) -> List[Dict[str, Any]]:
    """List all medications for a user."""
    medications = await query_items(
        medications_table,
        "user_id = :user_id",
        {":user_id": user_id},
        "UserIdIndex"
    )
    return medications

async def search_medications(user_id: str, query: str) -> List[Dict[str, Any]]:
    """Search medications for a user."""
    # Get all medications for the user
    medications = await list_medications(user_id)
    
    # Filter medications based on the query
    if query:
        query = query.lower()
        filtered_medications = [
            med for med in medications
            if query in med.get("name", "").lower() or
               query in med.get("notes", "").lower() or
               query in med.get("dosage", "").lower()
        ]
        return filtered_medications
    
    return medications

async def upload_medication_image(user_id: str, medication_id: str, file_obj, filename: str) -> str:
    """Upload an image for a medication."""
    # Check if medication exists
    medication = await get_item(medications_table, medication_id, "medication_id", user_id, "user_id")
    if not medication:
        raise NotFoundException(f"Medication with ID {medication_id} not found")
    
    # Generate a unique filename
    ext = filename.split(".")[-1]
    object_name = f"medications/{user_id}/{medication_id}_{uuid.uuid4()}.{ext}"
    
    # Upload file to S3
    image_url = await upload_file(file_obj, object_name, f"image/{ext}")
    
    # Update medication with image URL
    await update_medication(medication_id, user_id, {"image_url": image_url})
    
    return image_url
