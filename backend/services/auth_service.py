"""
Authentication service.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from backend.core.security import verify_password, get_password_hash, create_access_token
from backend.core.exceptions import AuthException, NotFoundException
from backend.db.dynamodb import create_user, get_user_by_email, get_user_by_id, update_user
from backend.config import settings

async def register_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Register a new user."""
    # Check if user with email already exists
    existing_user = await get_user_by_email(user_data["email"])
    if existing_user:
        raise AuthException("User with this email already exists")
    
    # Hash the password
    user_data["password_hash"] = get_password_hash(user_data.pop("password"))
    
    # Create the user
    user = await create_user(user_data)
    
    # Remove password_hash from response
    user.pop("password_hash", None)
    
    return user

async def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticate a user."""
    user = await get_user_by_email(email)
    if not user:
        raise AuthException("Invalid email or password")
    
    if not verify_password(password, user["password_hash"]):
        raise AuthException("Invalid email or password")
    
    # Remove password_hash from response
    user.pop("password_hash", None)
    
    return user

async def create_user_token(user_id: str) -> str:
    """Create a JWT token for a user."""
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user_id},
        expires_delta=expires_delta
    )

async def get_user_profile(user_id: str) -> Dict[str, Any]:
    """Get a user's profile."""
    user = await get_user_by_id(user_id)
    if not user:
        raise NotFoundException("User not found")
    
    # Remove password_hash from response
    user.pop("password_hash", None)
    
    return user

async def update_user_profile(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a user's profile."""
    user = await get_user_by_id(user_id)
    if not user:
        raise NotFoundException("User not found")
    
    updated_user = await update_user(user_id, update_data)
    
    # Remove password_hash from response
    updated_user.pop("password_hash", None)
    
    return updated_user

async def change_user_password(user_id: str, current_password: str, new_password: str) -> None:
    """Change a user's password."""
    user = await get_user_by_id(user_id)
    if not user:
        raise NotFoundException("User not found")
    
    if not verify_password(current_password, user["password_hash"]):
        raise AuthException("Current password is incorrect")
    
    password_hash = get_password_hash(new_password)
    await update_user(user_id, {"password_hash": password_hash})
