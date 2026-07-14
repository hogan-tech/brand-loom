"""Tests for brand_context schema contract and cross-skill seam coverage."""

from __future__ import annotations

import pytest

from brand_loom.agent import run_skill
from brand_loom.brand import EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT
from brand_loom.providers import use_provider
from brand_loom.skills.registry import list_skills

# ---------------------------------------------------------------------------
# 1) brand_context schema contract
# ---------------------------------------------------------------------------

EXPECTED_KEYS = {"tone", "audience", "do_phrases", "avoid_phrases"}


class TestBrandContextSchema:
    """EMPTY and SAMPLE brand contexts have identical shape and correct types."""

    def test_empty_and_sample_have_same_keys(self):
        assert set(EMPTY_BRAND_CONTEXT) == set(SAMPLE_BRAND_CONTEXT) == EXPECTED_KEYS

    # --- EMPTY assertions ---------------------------------------------------

    def test_empty_tone_is_empty_list(self):
        assert EMPTY_BRAND_CONTEXT["tone"] == []

    def test_empty_audience_is_empty_string(self):
        assert EMPTY_BRAND_CONTEXT["audience"] == ""

    def test_empty_do_phrases_is_empty_list(self):
        assert EMPTY_BRAND_CONTEXT["do_phrases"] == []

    def test_empty_avoid_phrases_is_empty_list(self):
        assert EMPTY_BRAND_CONTEXT["avoid_phrases"] == []

    # --- SAMPLE assertions --------------------------------------------------

    def test_sample_tone_non_empty(self):
        assert len(SAMPLE_BRAND_CONTEXT["tone"]) > 0

    def test_sample_audience_non_empty(self):
        assert SAMPLE_BRAND_CONTEXT["audience"] != ""

    def test_sample_do_phrases_non_empty(self):
        assert len(SAMPLE_BRAND_CONTEXT["do_phrases"]) > 0

    def test_sample_avoid_phrases_non_empty(self):
        assert len(SAMPLE_BRAND_CONTEXT["avoid_phrases"]) > 0

    # --- type checks --------------------------------------------------------

    @pytest.mark.parametrize("ctx", [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT])
    def test_tone_is_list_of_str(self, ctx):
        assert isinstance(ctx["tone"], list)
        assert all(isinstance(t, str) for t in ctx["tone"])

    @pytest.mark.parametrize("ctx", [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT])
    def test_audience_is_str(self, ctx):
        assert isinstance(ctx["audience"], str)

    @pytest.mark.parametrize("ctx", [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT])
    def test_do_phrases_is_list_of_str(self, ctx):
        assert isinstance(ctx["do_phrases"], list)
        assert all(isinstance(p, str) for p in ctx["do_phrases"])

    @pytest.mark.parametrize("ctx", [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT])
    def test_avoid_phrases_is_list_of_str(self, ctx):
        assert isinstance(ctx["avoid_phrases"], list)
        assert all(isinstance(p, str) for p in ctx["avoid_phrases"])


# ---------------------------------------------------------------------------
# 2) Seam contract — every skill × both brand contexts on the fake provider
# ---------------------------------------------------------------------------


def _all_skills() -> list[str]:
    """Load and return all registered skill names."""
    # Trigger auto-registration by importing agent module side-effect helper
    from brand_loom.agent import _ensure_skills_loaded

    _ensure_skills_loaded()
    return list_skills()


# schema_org is pure-Python (no LLM), but needs context keys instead of
# plain text. We handle it with a dedicated parametrize below.
_LLM_SKILLS = [s for s in _all_skills() if s != "schema_org"]


class TestSkillSeamContract:
    """Every registered skill must accept both EMPTY and SAMPLE brand_context
    on the fake provider without error and return a non-empty result."""

    def setup_method(self):
        use_provider("fake")

    # --- LLM-based skills ----------------------------------------------------

    @pytest.mark.parametrize("skill_name", _LLM_SKILLS)
    @pytest.mark.parametrize(
        "brand_ctx",
        [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT],
        ids=["empty_ctx", "sample_ctx"],
    )
    def test_llm_skill_with_brand_context(self, skill_name, brand_ctx):
        result = run_skill(skill_name, "cloud computing for startups", brand_context=brand_ctx)
        assert result.text, f"{skill_name} returned empty text with {brand_ctx}"
        assert isinstance(result.text, str)

    # --- schema_org (pure-Python, needs structured context) -------------------

    @pytest.mark.parametrize(
        "brand_ctx",
        [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT],
        ids=["empty_ctx", "sample_ctx"],
    )
    def test_schema_org_faq_with_brand_context(self, brand_ctx):
        result = run_skill(
            "schema_org",
            "faq page",
            brand_context=brand_ctx,
            schema_type="faq",
            faqs=[{"question": "What is brand-loom?", "answer": "An open-source toolkit."}],
        )
        assert result.text
        assert '"FAQPage"' in result.text

    @pytest.mark.parametrize(
        "brand_ctx",
        [EMPTY_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT],
        ids=["empty_ctx", "sample_ctx"],
    )
    def test_schema_org_article_with_brand_context(self, brand_ctx):
        result = run_skill(
            "schema_org",
            "My Headline",
            brand_context=brand_ctx,
            schema_type="article",
            headline="My Headline",
        )
        assert result.text
        assert '"Article"' in result.text
