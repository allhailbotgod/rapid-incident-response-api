from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    S3_ENPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    S3_REGION: str

    ALLOWED_MEDIA_TYPES: set[str]

    REDIS_URL: str

    ACCESS_TOKEN_EXPIRY_IN_MINS: int
    REFRESH_TOKEN_EXPIRY_IN_DAYS: int

    ALGORITHM: str
    SECRET_KEY: str
    ORIGINS: list[str]
    METHODS: list[str]
    HEADERS: list[str]
    CORS_CREDS: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="forbid"
    )


settings = Settings()
