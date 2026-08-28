from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    S3_ENPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    S3_REGION: str

    ALGORITHM: str
    SECRET_KEY: str
    EXP_IN_MINS: int
    ORIGINS: list[str]
    METHODS: list[str]
    HEADERS: list[str]
    CORS_CREDS: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="forbid"
    )


settings = Settings()
