"""Tests for the provider layer: fake provider, registry, selection."""

import pytest

from brand_loom.providers.base import (
    LLMProvider,
    get_provider,
    register_provider,
    resolve_provider_for_model,
    use_provider,
)
from brand_loom.providers.fake import FakeProvider


def test_fake_provider_satisfies_protocol():
    assert isinstance(FakeProvider(), LLMProvider)


def test_fake_provider_generate():
    p = FakeProvider()
    result = p.generate("hello world")
    assert "hello world" in result


def test_fake_provider_json_mode():
    p = FakeProvider()
    result = p.generate("Return JSON with the answer")
    assert "fake-response" in result


def test_register_and_get():
    p = FakeProvider()
    register_provider("test-fake", p)
    assert get_provider("test-fake") is p


def test_use_provider_sets_default():
    p = use_provider("fake")
    assert isinstance(p, FakeProvider)
    assert isinstance(get_provider(), FakeProvider)


def test_env_var_selection(monkeypatch):
    monkeypatch.setenv("BRANDLOOM_PROVIDER", "fake")
    p = get_provider()
    assert isinstance(p, FakeProvider)


def test_model_prefix_routing():
    use_provider("fake")
    register_provider("openai", FakeProvider())
    p = resolve_provider_for_model("gpt-4o")
    assert isinstance(p, FakeProvider)


def test_unknown_provider_raises():
    with pytest.raises(KeyError, match="unknown-provider"):
        get_provider("unknown-provider")


def test_unknown_model_prefix_raises():
    with pytest.raises(ValueError, match="Cannot auto-detect"):
        resolve_provider_for_model("llama-3")
