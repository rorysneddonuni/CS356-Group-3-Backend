from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    uploads_directory: str = "uploads"


@lru_cache
def get_settings():
    return Settings()
