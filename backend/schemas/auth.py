"""
Authentication schemas.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8)
    
class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """User update schema."""
    name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    notification_settings: Optional[Dict[str, Any]] = None

class PasswordChange(BaseModel):
    """Password change schema."""
    current_password: str
    new_password: str = Field(..., min_length=8)

class Token(BaseModel):
    """Token schema."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token data schema."""
    sub: str
    exp: int

class UserResponse(UserBase):
    """User response schema."""
    user_id: str
    created_at: int
    updated_at: int
    preferences: Dict[str, Any] = {}
    notification_settings: Dict[str, Any] = {}
