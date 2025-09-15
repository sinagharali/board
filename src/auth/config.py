from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    alg: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    access_token_secret_key: str
    refresh_token_secret_key: str

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=".env",
        extra="ignore",
    )


auth_settings = AuthSettings()  # type: ignore[Field ignored]
