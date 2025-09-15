from pydantic_settings import BaseSettings, SettingsConfigDict


class BucketSettings(BaseSettings):
    access_key: str
    secret_key: str
    name: str
    endpoint: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BUCKET_",
        extra="ignore",
    )


bucket_settings = BucketSettings()
