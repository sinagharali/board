from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    database_url: str
    database_future: bool
    database_echo: bool
    database_hide_parameters: bool

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        extra="ignore",
    )


database_settings = DataBaseSettings()
