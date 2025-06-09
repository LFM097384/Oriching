"""
Configuration settings for the I Ching Divination API.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings.
    
    These settings can be overridden by environment variables.
    """
    
    # API Settings
    app_name: str = "易经占卜 API"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # CORS Settings
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Data Settings
    hexagram_data_file: str = "hexagrams_complete.json"
    
    # Security Settings
    secret_key: Optional[str] = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Settings (for future use)
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()
