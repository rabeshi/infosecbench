from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    """Common interface for all benchmark models."""

    def __init__(self, name: str, **kwargs: Any):
        self.name = name
        self.config = kwargs

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Return a model response for a prompt."""

    def __call__(self, prompt: str, **kwargs: Any) -> str:
        return self.generate(prompt, **kwargs)
