"""LLM provider protocol, registry, and selection."""

from __future__ import annotations

import os
from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Interface every provider must satisfy."""

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str: ...


_REGISTRY: dict[str, LLMProvider] = {}
_ACTIVE: list[LLMProvider | None] = [None]  # mutable container for active provider

_MODEL_PREFIX_MAP: dict[str, str] = {
    "gpt-": "openai",
    "claude-": "anthropic",
    "gemini-": "gemini",
}


def register_provider(name: str, provider: LLMProvider) -> None:
    """Register a provider instance by name."""
    _REGISTRY[name] = provider


def get_provider(name: str | None = None) -> LLMProvider:
    """Get a provider by name, env var, or return the active default."""
    if name:
        return _resolve(name)

    env = os.environ.get("BRANDLOOM_PROVIDER")
    if env:
        return _resolve(env)

    if _ACTIVE[0] is not None:
        return _ACTIVE[0]

    raise RuntimeError(
        "No provider configured. Set BRANDLOOM_PROVIDER, call use_provider(), "
        "or pass provider= explicitly."
    )


def use_provider(name: str) -> LLMProvider:
    """Set the active provider by name and return it."""
    provider = _resolve(name)
    _ACTIVE[0] = provider
    return provider


def resolve_provider_for_model(model: str) -> LLMProvider:
    """Pick the right provider based on a model-name prefix (e.g. 'gpt-4o' → openai)."""
    for prefix, provider_name in _MODEL_PREFIX_MAP.items():
        if model.startswith(prefix):
            return _resolve(provider_name)
    raise ValueError(
        f"Cannot auto-detect provider for model {model!r}. "
        f"Known prefixes: {list(_MODEL_PREFIX_MAP)}"
    )


def _resolve(name: str) -> LLMProvider:
    """Resolve a provider by name, lazily importing built-in ones if needed."""
    if name not in _REGISTRY:
        _lazy_import(name)
    try:
        return _REGISTRY[name]
    except KeyError:
        available = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise KeyError(f"Provider {name!r} not found. Available: {available}") from None


def _lazy_import(name: str) -> None:
    """Attempt to import and auto-register a built-in provider."""
    if name == "fake":
        from brand_loom.providers.fake import FakeProvider

        register_provider("fake", FakeProvider())
    elif name == "openai":
        from brand_loom.providers.openai import OpenAIProvider

        register_provider("openai", OpenAIProvider())
    elif name == "anthropic":
        from brand_loom.providers.anthropic import AnthropicProvider

        register_provider("anthropic", AnthropicProvider())
    elif name == "gemini":
        from brand_loom.providers.gemini import GeminiProvider

        register_provider("gemini", GeminiProvider())
    elif name == "ollama":
        from brand_loom.providers.ollama import OllamaProvider

        register_provider("ollama", OllamaProvider())
