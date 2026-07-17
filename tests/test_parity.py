"""Provider parity eval — same skill, every provider, well-formed output.

CI runs on the fake provider (zero keys). Real-provider runs are opt-in
via BYOK env vars: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY.
"""

from __future__ import annotations

import os

import pytest

from brand_loom.agent import run_skill
from brand_loom.providers import use_provider

# ---------------------------------------------------------------------------
# Skills to test (all LLM-based skills)
# ---------------------------------------------------------------------------

LLM_SKILLS = ["hook", "caption", "hashtags", "cta", "faq", "repurpose", "seo_outline"]

SKILL_INPUTS: dict[str, str] = {
    "hook": "How to reduce cloud costs by 40%",
    "caption": "Launch of our new AI analytics dashboard",
    "hashtags": "sustainable fashion for Gen Z",
    "cta": "sign up for a free 14-day trial",
    "faq": (
        "Brand-loom is an open-source library of marketing skills. "
        "It supports OpenAI, Anthropic, Gemini, and Ollama."
    ),
    "repurpose": (
        "We reduced cloud costs by 40% in three months by right-sizing "
        "instances and switching to spot instances for batch workloads."
    ),
    "seo_outline": "best project management tools for startups in 2025",
}

# ---------------------------------------------------------------------------
# Structure validators per skill
# ---------------------------------------------------------------------------


def _assert_hook_structure(text: str) -> None:
    assert len(text.strip()) > 0, "hook returned empty"


def _assert_caption_structure(text: str) -> None:
    assert len(text.strip()) > 0, "caption returned empty"


def _assert_hashtags_structure(text: str) -> None:
    assert len(text.strip()) > 0, "hashtags returned empty"


def _assert_cta_structure(text: str) -> None:
    assert len(text.strip()) > 0, "cta returned empty"


def _assert_faq_structure(text: str) -> None:
    assert len(text.strip()) > 0, "faq returned empty"


def _assert_repurpose_structure(text: str) -> None:
    assert len(text.strip()) > 0, "repurpose returned empty"


def _assert_seo_outline_structure(text: str) -> None:
    assert len(text.strip()) > 0, "seo_outline returned empty"


STRUCTURE_VALIDATORS = {
    "hook": _assert_hook_structure,
    "caption": _assert_caption_structure,
    "hashtags": _assert_hashtags_structure,
    "cta": _assert_cta_structure,
    "faq": _assert_faq_structure,
    "repurpose": _assert_repurpose_structure,
    "seo_outline": _assert_seo_outline_structure,
}


# ---------------------------------------------------------------------------
# Fake provider — always runs in CI
# ---------------------------------------------------------------------------


class TestParityFake:
    """Every skill returns a well-formed result on the fake provider."""

    def setup_method(self):
        use_provider("fake")

    @pytest.mark.parametrize("skill_name", LLM_SKILLS)
    def test_skill_returns_nonempty(self, skill_name):
        result = run_skill(skill_name, SKILL_INPUTS[skill_name])
        assert result.text, f"{skill_name} returned empty on fake provider"
        STRUCTURE_VALIDATORS[skill_name](result.text)

    @pytest.mark.parametrize("skill_name", LLM_SKILLS)
    def test_skill_metadata_present(self, skill_name):
        result = run_skill(skill_name, SKILL_INPUTS[skill_name])
        assert isinstance(result.metadata, dict)


# ---------------------------------------------------------------------------
# Real providers — opt-in via BYOK env vars
# ---------------------------------------------------------------------------

_REAL_PROVIDERS = []
if os.environ.get("OPENAI_API_KEY"):
    _REAL_PROVIDERS.append("openai")
if os.environ.get("ANTHROPIC_API_KEY"):
    _REAL_PROVIDERS.append("anthropic")
if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
    _REAL_PROVIDERS.append("gemini")


@pytest.mark.skipif(not _REAL_PROVIDERS, reason="No real provider API keys set")
class TestParityReal:
    """Same skills, same inputs, on real providers — opt-in BYOK."""

    @pytest.mark.parametrize("provider_name", _REAL_PROVIDERS)
    @pytest.mark.parametrize("skill_name", LLM_SKILLS)
    def test_skill_on_provider(self, provider_name, skill_name):
        use_provider(provider_name)
        result = run_skill(skill_name, SKILL_INPUTS[skill_name])
        assert result.text, f"{skill_name} returned empty on {provider_name}"
        STRUCTURE_VALIDATORS[skill_name](result.text)
