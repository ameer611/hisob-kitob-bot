from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Telegram Bot token
    telegram_token: str
    # Database URL (async)
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()