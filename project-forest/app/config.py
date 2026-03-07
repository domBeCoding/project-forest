from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # App settings
    app_name: str = "project-forest"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Binance Testnet credentials (optional for skeleton)
    binance_testnet_api_key: str = ""
    binance_testnet_secret: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
