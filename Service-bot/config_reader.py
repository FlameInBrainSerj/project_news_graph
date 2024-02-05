from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Config class.
    """

    bot_token: SecretStr

    user: SecretStr
    password: SecretStr
    host: SecretStr
    port: SecretStr
    database: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
