"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from backend.schemas.auth import UserCreate, UserLogin, UserUpdate, PasswordChange, Token, UserResponse
from backend.services import auth_service
from backend.core.dependencies import get_current_user
from backend.core.exceptions import AuthException, NotFoundException

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user."""
    try:
        user = await auth_service.register_user(user_data.model_dump())
        return user
    except AuthException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login a user."""
    try:
        user = await auth_service.authenticate_user(user_data.email, user_data.password)
        access_token = await auth_service.create_user_token(user["user_id"])
        return {"access_token": access_token, "token_type": "bearer"}
    except AuthException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """Refresh a user's token."""
    access_token = await auth_service.create_user_token(current_user["user_id"])
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get the current user's profile."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_profile(user_data: UserUpdate, current_user: dict = Depends(get_current_user)):
    """Update the current user's profile."""
    try:
        updated_user = await auth_service.update_user_profile(current_user["user_id"], user_data.dict(exclude_unset=True))
        return updated_user
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/password")
async def change_password(password_data: PasswordChange, current_user: dict = Depends(get_current_user)):
    """Change the current user's password."""
    try:
        await auth_service.change_user_password(
            current_user["user_id"],
            password_data.current_password,
            password_data.new_password
        )
        return {"message": "Password changed successfully"}
    except (AuthException, NotFoundException) as e:
        status_code = status.HTTP_401_UNAUTHORIZED if isinstance(e, AuthException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e))
