"""
Medication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query
from typing import List, Optional
from backend.schemas.medication import MedicationCreate, MedicationUpdate, MedicationResponse
from backend.services import medication_service
from backend.core.dependencies import get_current_user
from backend.core.exceptions import NotFoundException

router = APIRouter()

@router.post("", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def create_medication(
    medication_data: MedicationCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new medication."""
    medication = await medication_service.create_medication(
        current_user["user_id"],
        medication_data.dict()
    )
    return medication

@router.get("", response_model=List[MedicationResponse])
async def list_medications(
    query: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """List all medications for the current user."""
    if query:
        medications = await medication_service.search_medications(current_user["user_id"], query)
    else:
        medications = await medication_service.list_medications(current_user["user_id"])
    return medications

@router.get("/{medication_id}", response_model=MedicationResponse)
async def get_medication(
    medication_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a medication by ID."""
    try:
        medication = await medication_service.get_medication(medication_id, current_user["user_id"])
        return medication
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_medication(
    medication_id: str,
    medication_data: MedicationUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a medication."""
    try:
        updated_medication = await medication_service.update_medication(
            medication_id,
            current_user["user_id"],
            medication_data.dict(exclude_unset=True)
        )
        return updated_medication
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medication(
    medication_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a medication."""
    try:
        await medication_service.delete_medication(medication_id, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{medication_id}/image")
async def upload_image(
    medication_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload an image for a medication."""
    try:
        image_url = await medication_service.upload_medication_image(
            current_user["user_id"],
            medication_id,
            file.file,
            file.filename
        )
        return {"image_url": image_url}
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
