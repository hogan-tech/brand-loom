"""Tests for real providers — mock SDK clients; no network in CI."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from brand_loom.providers.base import LLMProvider


class TestOpenAIProvider:
    def test_lazy_import_error(self):
        from brand_loom.providers.openai import OpenAIProvider

        p = OpenAIProvider(api_key="test-key")
        with patch.dict("sys.modules", {"openai": None}):
            # Force re-import failure by clearing cached client
            p._client = None
            with pytest.raises(ImportError, match="openai package"):
                p._get_client()

    def test_missing_key_error(self):
        from brand_loom.providers.openai import OpenAIProvider

        p = OpenAIProvider(api_key="")
        with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
            p._get_client()

    def test_generate_with_mock(self):
        from brand_loom.providers.openai import OpenAIProvider

        p = OpenAIProvider(api_key="test-key")
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="mocked response"))]
        )
        p._client = mock_client
        result = p.generate("test prompt", system="be helpful")
        assert result == "mocked response"
        assert isinstance(p, LLMProvider)


class TestAnthropicProvider:
    def test_missing_key_error(self):
        from brand_loom.providers.anthropic import AnthropicProvider

        p = AnthropicProvider(api_key="")
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            p._get_client()

    def test_generate_with_mock(self):
        from brand_loom.providers.anthropic import AnthropicProvider

        p = AnthropicProvider(api_key="test-key")
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="mocked claude response")]
        )
        p._client = mock_client
        result = p.generate("test prompt", system="be helpful")
        assert result == "mocked claude response"
        assert isinstance(p, LLMProvider)


class TestGeminiProvider:
    def test_missing_key_error(self):
        from brand_loom.providers.gemini import GeminiProvider

        p = GeminiProvider(api_key="")
        with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
            p._get_client()

    def test_generate_with_mock(self):
        from brand_loom.providers.gemini import GeminiProvider

        # We need to mock the google.genai module
        mock_genai = MagicMock()
        mock_types = MagicMock()
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = MagicMock(text="mocked gemini")

        p = GeminiProvider(api_key="test-key")
        p._client = mock_client

        with patch.dict("sys.modules", {"google": MagicMock(), "google.genai": mock_genai}):
            mock_genai.types = mock_types
            result = p.generate("test prompt")
            assert result == "mocked gemini"
            assert isinstance(p, LLMProvider)


class TestOllamaProvider:
    def test_default_host(self):
        from brand_loom.providers.ollama import OllamaProvider

        p = OllamaProvider()
        assert "localhost:11434" in p._host
        assert isinstance(p, LLMProvider)

    def test_generate_with_mock(self):
        import json

        from brand_loom.providers.ollama import OllamaProvider

        p = OllamaProvider(host="http://localhost:11434")
        response_data = json.dumps({"message": {"content": "mocked ollama"}}).encode()

        mock_resp = MagicMock()
        mock_resp.read.return_value = response_data
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = p.generate("test prompt")
            assert result == "mocked ollama"

    def test_default_timeout(self):
        from brand_loom.providers.ollama import OllamaProvider

        p = OllamaProvider()
        assert p._timeout == 120.0

    def test_timeout_from_env(self, monkeypatch):
        from brand_loom.providers.ollama import OllamaProvider

        monkeypatch.setenv("OLLAMA_TIMEOUT", "5")
        p = OllamaProvider()
        assert p._timeout == 5.0

    def test_explicit_timeout_beats_env(self, monkeypatch):
        from brand_loom.providers.ollama import OllamaProvider

        monkeypatch.setenv("OLLAMA_TIMEOUT", "5")
        p = OllamaProvider(timeout=30)
        assert p._timeout == 30

    def test_generate_passes_timeout(self):
        import json

        from brand_loom.providers.ollama import OllamaProvider

        p = OllamaProvider(timeout=7)
        response_data = json.dumps({"message": {"content": "ok"}}).encode()

        mock_resp = MagicMock()
        mock_resp.read.return_value = response_data
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
            p.generate("test prompt")
        assert mock_urlopen.call_args.kwargs["timeout"] == 7


class TestModelPrefixRouting:
    def test_gpt_routes_to_openai(self):
        from brand_loom.providers.base import register_provider, resolve_provider_for_model
        from brand_loom.providers.openai import OpenAIProvider

        p = OpenAIProvider(api_key="test")
        register_provider("openai", p)
        assert resolve_provider_for_model("gpt-4o") is p

    def test_claude_routes_to_anthropic(self):
        from brand_loom.providers.anthropic import AnthropicProvider
        from brand_loom.providers.base import register_provider, resolve_provider_for_model

        p = AnthropicProvider(api_key="test")
        register_provider("anthropic", p)
        assert resolve_provider_for_model("claude-sonnet-4-20250514") is p

    def test_gemini_routes_to_gemini(self):
        from brand_loom.providers.base import register_provider, resolve_provider_for_model
        from brand_loom.providers.gemini import GeminiProvider

        p = GeminiProvider(api_key="test")
        register_provider("gemini", p)
        assert resolve_provider_for_model("gemini-2.0-flash") is p
