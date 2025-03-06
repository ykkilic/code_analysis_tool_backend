# app/core/config.py
from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Security Analysis API"
    
    # SQLite configuration
    SQLITE_DB: str = "security_analysis.db"
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///./{SQLITE_DB}"
    
    # NVD API Configuration
    NVD_API_KEY: Optional[str] = None
    NVD_API_DELAY: int = 6  # Delay between API calls in seconds
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()