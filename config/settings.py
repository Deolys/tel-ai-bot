import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")

    ai_model: str = os.getenv("AI_MODEL", "deepseek/deepseek-chat")
    ai_max_tokens: int = int(os.getenv("AI_MAX_TOKENS", "4000"))
    ai_temperature: float = float(os.getenv("AI_TEMPERATURE", "0.7"))

    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    max_context_messages: int = 10
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "ru")

    class Config:
        case_sensitive = False


settings = Settings()
