from functools import lru_cache
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent.parent
BASE_DIR = BACKEND_DIR.parent


class Settings(
    BaseSettings
):
    APP_NAME: str = (
        "AI Interview System"
    )

    MONGODB_URI: str

    GROQ_API_KEY: str
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    VOYAGE_API_KEY: str
    VOYAGE_MODEL: str = "voyage-3.5"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    ENVIRONMENT: str = (
        "development"
    )

    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB

    FAISS_PATH: str = str(BACKEND_DIR / "knowledge_base" / "faiss.index")
    CHUNKS_PATH: str = str(BACKEND_DIR / "knowledge_base" / "chunks.json")
    METADATA_PATH: str = str(BACKEND_DIR / "knowledge_base" / "metadata.json")

    model_config = SettingsConfigDict(
        env_file=(str(BACKEND_DIR / ".env"), ".env"),
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()


settings = (
    get_settings()
)