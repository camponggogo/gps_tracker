from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    database_url: str = "mysql+pymysql://root:123456!@localhost:3306/transportation_db"
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "transportation_db"
    database_user: str = "root"
    database_password: str = "123456!"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 17890
    api_debug: bool = True
    
    # Security settings
    secret_key: str = "_5wwvZWMjUUpK7eg5sklHh8mpQE0UNtQSVabpIE0ArY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # GPS settings
    gps_update_interval: int = 30  # seconds
    gps_accuracy_threshold: float = 10.0  # meters
    gps_idle_timeout: int = 300  # seconds (5 minutes)
    
    # Area settings
    max_area_points: int = 1000
    default_area_buffer: float = 50.0  # meters
    
    # Dashboard settings
    dashboard_refresh_interval: int = 10  # seconds
    max_vehicles_display: int = 100
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "logs/gps_tracking.log"
    
    # Map settings
    default_latitude: float = 13.7563
    default_longitude: float = 100.5018
    default_zoom: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()
