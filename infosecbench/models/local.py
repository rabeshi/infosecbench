from __future__ import annotations

from typing import Any

from .base import BaseModel


class LocalModel(BaseModel):
    """Placeholder adapter for local Hugging Face or Ollama-style inference servers."""

    def __init__(self, name: str, endpoint: str | None = None, **kwargs: Any):
        super().__init__(name=name, endpoint=endpoint, **kwargs)

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return f"Local inference placeholder for {self.name}: {prompt[:80]}"
