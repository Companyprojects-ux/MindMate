"""
Configuration settings for the Mental Health Support application.
"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "Mental Health Support"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AWS Settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "mental-health-app-resources")

    # AI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
