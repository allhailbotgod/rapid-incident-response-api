from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str
    SECRET_KEY: str
    EXP_IN_MINS: int
    ORIGINS: List[str]
    METHODS: List[str]
    HEADERS: List[str]
    CORS_CREDS: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="forbid"
    )


settings = Settings()
