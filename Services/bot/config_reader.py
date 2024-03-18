from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Config class.
    """

    bot_token: SecretStr

    db_host: SecretStr
    db_port: SecretStr
    postgres_db: SecretStr
    postgres_user: SecretStr
    postgres_password: SecretStr

    api_host: SecretStr
    api_port: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
