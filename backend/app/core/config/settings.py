from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
)


class Settings(
    BaseSettings
):
    APP_NAME: str = (
        "AI Interview System"
    )

    MONGODB_URI: str

    GROQ_API_KEY: str

    VOYAGE_API_KEY: str

    JWT_SECRET: str

    ENVIRONMENT: str = (
        "development"
    )

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = (
    get_settings()
)