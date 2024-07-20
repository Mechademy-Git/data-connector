from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    api_key: str = "your_secure_api_key"
    database_url: str = "sqlite:///sample_db.sqlite3"
    api_base_url: str = "http://turbomechanica.ai"
    api_post_endpoint: str = "/api/data"
    post_data_endpoint: str = "http://turbomechanica.ai/api/data"
    post_data_api_key: str = "turbomechanica_api_key"
    fetch_data_interval: int = 30  # minutes
    batch_size: int = 30  # minutes

    class Config:
        env_file = ".env"


settings = Settings()
