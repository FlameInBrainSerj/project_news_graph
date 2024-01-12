from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


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
    external_uri: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
