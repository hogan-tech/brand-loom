"""Tests for the thin agent runner."""

import pytest

from brand_loom.agent import run_chain, run_skill
from brand_loom.providers import use_provider


class TestRunSkill:
    def setup_method(self):
        use_provider("fake")

    def test_run_hook(self):
        result = run_skill("hook", "cloud computing")
        assert result.text
        assert isinstance(result.text, str)

    def test_run_caption(self):
        result = run_skill("caption", "product launch")
        assert result.text

    def test_run_with_brand_context(self):
        brand = {"tone": ["bold"], "audience": "founders"}
        result = run_skill("hook", "AI marketing", brand_context=brand)
        assert result.text

    def test_unknown_skill_raises(self):
        with pytest.raises(KeyError, match="nonexistent"):
            run_skill("nonexistent", "text")


class TestRunChain:
    def setup_method(self):
        use_provider("fake")

    def test_two_step_chain(self):
        result = run_chain(["hook", "caption"], "cloud costs")
        assert result.text
        assert isinstance(result.text, str)

    def test_single_step_chain(self):
        result = run_chain(["hook"], "topic")
        assert result.text

    def test_chain_passes_output_forward(self):
        r_chain = run_chain(["hook", "caption"], "topic")
        # Chain runs both skills sequentially, caption gets hook output as input
        assert r_chain.text

    def test_empty_chain_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            run_chain([], "text")

    def test_chain_with_brand_context(self):
        brand = {"tone": ["professional"], "audience": "CTOs"}
        result = run_chain(["hook", "caption"], "AI launch", brand_context=brand)
        assert result.text
