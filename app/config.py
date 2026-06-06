from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    app_name: str = "ServicePilot AI"
    app_tagline: str = "Turn messy customer requests into organized jobs, quotes, invoices, and follow-ups."
    database_url: str = Field(default=f"sqlite:///{BASE_DIR / 'data' / 'servicepilot.db'}")
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    secret_key: str = "change-me-in-production"
    demo_mode: bool = True

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8", extra="ignore")

    @property
    def ai_mode(self) -> str:
        return "Real API mode" if self.openai_api_key else "Mock mode"


@lru_cache
def get_settings() -> Settings:
    return Settings()

