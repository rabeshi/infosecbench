from __future__ import annotations

from typing import Any

from .base import BaseModel


class MockModel(BaseModel):
    """A deterministic model used for tests and local benchmarking."""

    def __init__(self, name: str = "mock-model", response_text: str = "mock response", **kwargs: Any):
        super().__init__(name=name, **kwargs)
        self.response_text = response_text

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.response_text
