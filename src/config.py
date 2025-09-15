from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_token: str
    log_host: str

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()  # type: ignore[Field ignored]
