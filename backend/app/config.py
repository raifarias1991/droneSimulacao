from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "drone-simulacao-ai"
    environment: str = "development"
    api_prefix: str = "/api"
    llm_provider: Literal["openai", "ollama", "mock"] = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    drone_max_speed: float = 12.0
    drone_max_altitude: float = 120.0
    drone_min_altitude: float = 5.0
    battery_warning_level: int = 25


@lru_cache
def get_settings() -> Settings:
    return Settings()
