from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="USETAI_", extra="ignore")

    provider: str = Field(default="heuristic")
    max_steps: int = Field(default=4, ge=1, le=12)
    enable_docs_tool: bool = True
    enable_web_tool: bool = True

    docs_paths: str = "README.md,docs"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    hf_model: str = "google/flan-t5-small"
    hf_api_token: str | None = None

    history_file: str = "history.json"

    def parsed_docs_paths(self) -> list[str]:
        return [p.strip() for p in self.docs_paths.split(",") if p.strip()]
