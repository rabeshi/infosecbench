from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .base import BaseModel

DEFAULT_OLLAMA_ENDPOINT = "http://localhost:11434"


class OllamaConnectionError(RuntimeError):
    """Raised when the local Ollama server cannot be reached or returns an error."""


class LocalModel(BaseModel):
    """Adapter for a local Ollama server's /api/generate endpoint."""

    def __init__(
        self,
        name: str,
        model: str | None = None,
        endpoint: str = DEFAULT_OLLAMA_ENDPOINT,
        timeout: float = 120.0,
        options: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        super().__init__(name=name, endpoint=endpoint, **kwargs)
        self.endpoint = endpoint.rstrip("/")
        self.model = model or name
        self.timeout = timeout
        self.options = options or {}

    def generate(self, prompt: str, **kwargs: Any) -> str:
        call_options = {**self.options, **kwargs.pop("options", {})}
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if call_options:
            payload["options"] = call_options

        request = urllib.request.Request(
            f"{self.endpoint}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            raise OllamaConnectionError(
                f"Could not reach Ollama at {self.endpoint} for model '{self.model}': {exc}"
            ) from exc

        if "error" in body:
            raise OllamaConnectionError(f"Ollama returned an error for model '{self.model}': {body['error']}")

        return str(body.get("response", ""))
