"""Application settings.

Model identifiers live here and in RUN_MANIFEST.json — never inline in a
node. The architecture must not depend on which Claude model is selected,
so nothing below this module is allowed to name one.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- identity of this build -------------------------------------------
    app_version: str = "0.1.0"
    app_env: str = Field(default="local", description="local | ci | container")

    # --- model ------------------------------------------------------------
    anthropic_api_key: str = Field(default="", repr=False)
    model_id: str = "claude-sonnet-5"
    max_tokens: int = 4096

    # Deliberately absent: temperature, top_p, top_k.
    #
    # Current Claude models reject non-default sampling parameters — setting
    # them returns HTTP 400 rather than tuning anything (architecture/ADR-000).
    # Output reliability in this application comes from typed contracts
    # (Chapter 8), validation nodes (Chapter 11) and evaluation (Chapter 12),
    # not from a sampling knob. If you came here looking for temperature=0,
    # Chapter 8 is the chapter that replaces it.

    # --- persistence ------------------------------------------------------
    database_url: str = "postgresql://widgetware:widgetware@localhost:5432/widgetware"

    # --- autonomy boundary (Chapter 3) ------------------------------------
    # Book 1 never builds a send tool. This flag exists so the boundary is
    # inspectable and assertable in a test, not because there is a code path
    # behind it that would send anything.
    allow_external_send: bool = False

    def model_parameters(self) -> dict[str, object]:
        """Exactly what is recorded for an evaluated run.

        Sampling parameters are reported as the model's defaults rather than
        as values, because this application does not set them.
        """
        return {
            "model_id": self.model_id,
            "max_tokens": self.max_tokens,
            "sampling": "model defaults (temperature/top_p/top_k not set)",
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
