"""Google Gemini provider — requires `pip install brand-loom[gemini]`."""

from __future__ import annotations

import os


class GeminiProvider:
    """Google Gemini LLM provider (BYOK)."""

    def __init__(self, api_key: str | None = None, default_model: str = "gemini-2.0-flash"):
        self._api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get(
            "GOOGLE_API_KEY", ""
        )
        self._default_model = default_model
        self._client = None

    def _get_client(self):
        if self._client is None:
            if not self._api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY (or GOOGLE_API_KEY) not set. "
                    "Run: export GEMINI_API_KEY=..."
                )
            try:
                from google import genai
            except ImportError:
                raise ImportError(
                    "google-genai package not installed. Run: pip install brand-loom[gemini]"
                ) from None
            self._client = genai.Client(api_key=self._api_key)
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
        try:
            from google.genai import types
        except ImportError:
            raise ImportError(
                "google-genai package not installed. Run: pip install brand-loom[gemini]"
            ) from None

        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        if system:
            config.system_instruction = system

        resp = client.models.generate_content(
            model=model or self._default_model,
            contents=prompt,
            config=config,
        )
        return resp.text or ""
