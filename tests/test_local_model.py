import json
import urllib.error
from io import BytesIO
from unittest.mock import patch

import pytest

from infosecbench.models.local import LocalModel, OllamaConnectionError


class _FakeResponse(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False


def test_local_model_parses_ollama_response() -> None:
    model = LocalModel(name="llama3", endpoint="http://localhost:11434")
    fake_body = json.dumps({"response": "use salted adaptive hashing"}).encode("utf-8")

    with patch("urllib.request.urlopen", return_value=_FakeResponse(fake_body)) as mock_urlopen:
        result = model.generate("Explain secure password storage.")

    assert result == "use salted adaptive hashing"
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "http://localhost:11434/api/generate"
    sent_payload = json.loads(request.data.decode("utf-8"))
    assert sent_payload["model"] == "llama3"
    assert sent_payload["prompt"] == "Explain secure password storage."
    assert sent_payload["stream"] is False


def test_local_model_raises_on_connection_failure() -> None:
    model = LocalModel(name="llama3")

    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("no connection")):
        with pytest.raises(OllamaConnectionError):
            model.generate("prompt")


def test_local_model_raises_on_ollama_error_payload() -> None:
    model = LocalModel(name="llama3")
    fake_body = json.dumps({"error": "model not found"}).encode("utf-8")

    with patch("urllib.request.urlopen", return_value=_FakeResponse(fake_body)):
        with pytest.raises(OllamaConnectionError):
            model.generate("prompt")
