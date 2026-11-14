from __future__ import annotations

from typing import Any

from .base import BaseModel


class APIModel(BaseModel):
    """Placeholder adapter for OpenAI-compatible or custom REST endpoints."""

    def __init__(self, name: str, endpoint: str | None = None, api_key_env: str | None = None, **kwargs: Any):
        super().__init__(name=name, endpoint=endpoint, api_key_env=api_key_env, **kwargs)

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return f"API inference placeholder for {self.name}: {prompt[:80]}"
