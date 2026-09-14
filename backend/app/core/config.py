import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Force load environment variables from .env file, overriding any stale OS defaults
load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Janaseva Government Service Assistant"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "janaseva-super-secret-key-production-change-me-32bytes!")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database Settings - SQLite fallback if PostgreSQL is not available
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./janaseva.db")

    # Redis Settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Meta WhatsApp Cloud API
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "mock_whatsapp_token")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "mock_phone_number_id")
    WHATSAPP_VERIFY_TOKEN: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "janaseva_verify_token")
    WHATSAPP_API_URL: str = "https://graph.facebook.com/v19.0"

    # Gemini AI API Key
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")

    # Admin Initial Credentials
    FIRST_ADMIN_USERNAME: str = os.getenv("FIRST_ADMIN_USERNAME", "admin")
    FIRST_ADMIN_PASSWORD: str = os.getenv("FIRST_ADMIN_PASSWORD", "janaseva123!")

    class Config:
        case_sensitive = True

settings = Settings()
