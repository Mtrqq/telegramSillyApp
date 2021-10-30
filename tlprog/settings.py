from pydantic import BaseConfig
from pydantic import BaseSettings
from pydantic import Field


class AppSettings(BaseSettings):
    API_ID: str = Field(..., env="TELEGRAM_API_ID")
    API_HASH: str = Field(..., env="TELEGRAM_API_HASH")
    SESSION_NAME: str = Field("progress", env="TELEGRAM_SESSION_NAME")

    class Config(BaseConfig):
        env_file = ".env"


settings = AppSettings()
