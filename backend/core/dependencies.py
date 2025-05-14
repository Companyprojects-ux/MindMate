"""
Dependency injection utilities for the application.
"""
from fastapi import Depends, Header
from typing import Optional
from backend.core.security import decode_access_token
from backend.core.exceptions import AuthException
from backend.db.dynamodb import get_user_by_id

async def get_current_user(authorization: Optional[str] = Header(None)):
    """Get the current authenticated user."""
    if not authorization:
        raise AuthException("Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise AuthException("Invalid authentication scheme")
        
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthException("Invalid token payload")
        
        user = await get_user_by_id(user_id)
        if user is None:
            raise AuthException("User not found")
        
        return user
    except ValueError:
        raise AuthException("Invalid authorization header")
