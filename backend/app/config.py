import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Agentic Trip Planner"
    environment: str = os.getenv("ENVIRONMENT", "dev")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database
    sqlite_path: str = os.getenv("SQLITE_PATH", "db.sqlite")

    # LLM providers (keys are optional; if missing, LLM calls will be stubbed)
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    mistral_api_key: str | None = os.getenv("MISTRAL_API_KEY")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

