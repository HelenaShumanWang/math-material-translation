"""Runtime settings (environment variables / .env)."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MATHTRANS_", env_file=".env", extra="ignore")

    anthropic_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("ANTHROPIC_API_KEY", "MATHTRANS_ANTHROPIC_API_KEY"),
    )
    claude_model: str = "claude-opus-5-5"
    claude_review_model: Optional[str] = None  # defaults to claude_model
    claude_effort: Literal["low", "medium", "high", "xhigh", "max"] = "high"
    enable_fallbacks: bool = True
    translator: Literal["auto", "claude", "mock"] = "auto"
    ocr_engine: Literal["auto", "rapid", "claude", "none"] = "auto"
    data_dir: Path = Path("data")
    fonts_dir: Optional[Path] = None
    max_qa_rounds: int = 3
    require_qa_pass: bool = True
    min_font_scale: float = 0.55
    preview_dpi: int = 110
    batch_chars: int = 6000  # approx. characters of source text per translation request
    max_workers: int = 2  # concurrent translation jobs in the web service
    max_upload_mb: int = 100  # per-file upload limit of the web service
    log_level: str = "INFO"

    @property
    def has_api_key(self) -> bool:
        return bool(self.anthropic_api_key) or bool(os.environ.get("ANTHROPIC_AUTH_TOKEN"))

    def resolved_translator(self, requested: str = "auto") -> str:
        req = requested if requested and requested != "auto" else self.translator
        if req == "auto":
            return "claude" if self.has_api_key else "mock"
        return req

    def resolved_ocr(self, requested: str = "auto") -> str:
        req = requested if requested and requested != "auto" else self.ocr_engine
        return req

    def review_model(self) -> str:
        return self.claude_review_model or self.claude_model


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings() -> None:
    get_settings.cache_clear()
