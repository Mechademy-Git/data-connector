from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    api_key: str = "your_secure_api_key"


def get_settings() -> Settings:
    return Settings()
