"""Tests for the before/after brand_context demo and RICH_BRAND_CONTEXT."""

from __future__ import annotations

import json
import subprocess
import sys

from brand_loom.agent import run_skill
from brand_loom.brand import EMPTY_BRAND_CONTEXT, RICH_BRAND_CONTEXT, SAMPLE_BRAND_CONTEXT
from brand_loom.providers import use_provider


class TestRichBrandContext:
    def test_has_same_keys_as_empty(self):
        assert set(RICH_BRAND_CONTEXT) == set(EMPTY_BRAND_CONTEXT)

    def test_has_same_keys_as_sample(self):
        assert set(RICH_BRAND_CONTEXT) == set(SAMPLE_BRAND_CONTEXT)

    def test_tone_is_richer_than_sample(self):
        assert len(RICH_BRAND_CONTEXT["tone"]) >= len(SAMPLE_BRAND_CONTEXT["tone"])

    def test_avoid_phrases_is_richer_than_sample(self):
        rich = len(RICH_BRAND_CONTEXT["avoid_phrases"])
        sample = len(SAMPLE_BRAND_CONTEXT["avoid_phrases"])
        assert rich >= sample

    def test_audience_is_non_empty(self):
        assert len(RICH_BRAND_CONTEXT["audience"]) > 0

    def test_do_phrases_is_non_empty(self):
        assert len(RICH_BRAND_CONTEXT["do_phrases"]) > 0


class TestSampleBrandContextJson:
    def test_json_file_is_valid(self):
        with open("examples/sample_brand_context.json") as f:
            data = json.load(f)
        assert set(data) == set(EMPTY_BRAND_CONTEXT)
        assert isinstance(data["tone"], list)
        assert isinstance(data["audience"], str)

    def test_json_matches_rich_context(self):
        with open("examples/sample_brand_context.json") as f:
            data = json.load(f)
        assert data["tone"] == RICH_BRAND_CONTEXT["tone"]
        assert data["audience"] == RICH_BRAND_CONTEXT["audience"]


class TestBeforeAfterSkills:
    def setup_method(self):
        use_provider("fake")

    def test_bare_vs_branded_both_render(self):
        for skill_name in ["hook", "caption", "cta"]:
            bare = run_skill(skill_name, "cloud costs")
            branded = run_skill(skill_name, "cloud costs", brand_context=RICH_BRAND_CONTEXT)
            assert bare.text, f"{skill_name} bare returned empty"
            assert branded.text, f"{skill_name} branded returned empty"


class TestDemoScriptRuns:
    def test_demo_runs_without_error(self):
        result = subprocess.run(
            [sys.executable, "examples/before_after_demo.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"Demo failed:\n{result.stderr}"
        assert "brand-loom" in result.stdout.lower()
