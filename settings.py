from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the application.
    """
    # Telegram Bot token
    telegram_bot_token: str
    # Database URL (async)
    database_url: str
    # Admin user ID
    admin_users_ids: List[int]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()