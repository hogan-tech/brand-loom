"""Fake / echo provider for tests and quickstart — zero API keys needed."""

from __future__ import annotations

import json


class FakeProvider:
    """Deterministic provider that returns templated responses."""

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        # If the prompt asks for JSON, return a plausible JSON structure
        lower = prompt.lower()
        if "json" in lower:
            return json.dumps(self._json_response(prompt))
        # Default: echo back a summary
        snippet = prompt[:120].replace("\n", " ")
        return f"[fake-provider] Response for: {snippet}"

    def _json_response(self, prompt: str) -> dict:
        """Return a simple JSON structure matching common skill outputs."""
        return {
            "result": "fake-response",
            "prompt_length": len(prompt),
        }
