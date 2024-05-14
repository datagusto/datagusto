from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USE_GPU: Optional[str] = "cpu"
    LLM_USAGE_TYPE: str
    OPENAI_API_VERSION: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    OPENAI_KEY: Optional[str] = None
    VECTOR_DB_USAGE_TYPE: str
    VECTOR_DB_ENDPOINT: Optional[str] = None

    class Config:
        env_file = ".env"


# reading file is slow. use lru_cache to cache the result
@lru_cache()
def get_settings():
    settings = Settings()
    return settings
