"""OpenAI provider — requires `pip install brand-loom[openai]`."""

from __future__ import annotations

import os


class OpenAIProvider:
    """OpenAI LLM provider (BYOK)."""

    def __init__(self, api_key: str | None = None, default_model: str = "gpt-4o"):
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self._default_model = default_model
        self._client = None

    def _get_client(self):
        if self._client is None:
            if not self._api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY not set. Run: export OPENAI_API_KEY=sk-..."
                )
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError(
                    "openai package not installed. Run: pip install brand-loom[openai]"
                ) from None
            self._client = OpenAI(api_key=self._api_key)
        return self._client

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        client = self._get_client()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = client.chat.completions.create(
            model=model or self._default_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""
