from pydantic_settings import BaseSettings, SettingsConfigDict


class AclSettings(BaseSettings):
    api_url: str
    store_id: str
    model_id: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FGA_",
        extra="ignore",
    )


acl_settings = AclSettings()
