"""Ollama provider — local models via HTTP, no SDK required."""

from __future__ import annotations

import json
import os
import urllib.request


class OllamaProvider:
    """Ollama LLM provider (local, no API key needed)."""

    def __init__(
        self,
        host: str | None = None,
        default_model: str = "llama3",
        timeout: float | None = None,
    ):
        self._host = (host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")).rstrip("/")
        self._default_model = default_model
        self._timeout = timeout if timeout is not None else float(
            os.environ.get("OLLAMA_TIMEOUT", "120")
        )

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        url = f"{self._host}/api/chat"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = json.dumps({
            "model": model or self._default_model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }).encode()

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:
            data = json.loads(resp.read())
        return data["message"]["content"]
