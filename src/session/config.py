from pydantic_settings import BaseSettings, SettingsConfigDict


class SessionSettings(BaseSettings):
    expire_days: int

    model_config = SettingsConfigDict(
        env_prefix="SESSION_",
        env_file=".env",
        extra="ignore",
    )


session_settings = SessionSettings()
