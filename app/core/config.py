from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AlgoRoot Function Execution API"
    
    # Vector Database Settings
    CHROMA_DB_PATH: str = str(Path("data/chroma_db"))
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Function Registry Settings
    MAX_RETRIEVAL_RESULTS: int = 3
    
    class Config:
        case_sensitive = True

settings = Settings() 