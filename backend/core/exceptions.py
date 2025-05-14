"""
Custom exception classes for the application.
"""
from fastapi import status

class AppException(Exception):
    """Base exception class for application-specific exceptions."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)

class AuthException(AppException):
    """Exception raised for authentication errors."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail, status_code=status.HTTP_401_UNAUTHORIZED)

class NotFoundException(AppException):
    """Exception raised when a resource is not found."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail, status_code=status.HTTP_404_NOT_FOUND)

class ForbiddenException(AppException):
    """Exception raised when access to a resource is forbidden."""
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(detail, status_code=status.HTTP_403_FORBIDDEN)
