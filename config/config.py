from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Config_var(BaseSettings):
    app_name: str
    app_env: str
    debug: bool
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str
    mongodb_uri: str
    mongodb_db: str
    azure_openai_endpoint: str
    openai_api_key: str
    azure_openai_api_version: str
    azure_openai_deployment: str
    access_token_expire_minutes: int

    # ✅ Pydantic v2 style configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # allow extra env variables without error
    )


# create instance
config = Config_var()
