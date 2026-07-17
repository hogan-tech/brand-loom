"""Tests for the SEO outline skill."""

from brand_loom.prompts.seo_outline import SEO_OUTLINE_FEW_SHOT, build_seo_outline_prompt
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.seo_outline import SEOOutlineSkill


class TestSEOOutlinePromptBuilder:
    def test_basic_prompt(self):
        system, user = build_seo_outline_prompt("cloud cost optimization")
        assert "outline" in user.lower() or "seo" in system.lower()
        assert "cloud cost optimization" in user

    def test_section_count_default(self):
        _, user = build_seo_outline_prompt("topic")
        assert "6" in user

    def test_section_count_clamped_min(self):
        _, user = build_seo_outline_prompt("topic", section_count=2)
        assert "4" in user  # clamped to min 4

    def test_section_count_clamped_max(self):
        _, user = build_seo_outline_prompt("topic", section_count=20)
        assert "8" in user  # clamped to max 8

    def test_locale_param(self):
        system, _ = build_seo_outline_prompt("topic", locale="de")
        assert "de" in system

    def test_brand_context(self):
        system, _ = build_seo_outline_prompt(
            "topic",
            brand_context={"tone": ["authoritative"], "audience": "CTOs"},
        )
        assert "authoritative" in system
        assert "CTOs" in system

    def test_few_shot_exemplars_in_system(self):
        system, _ = build_seo_outline_prompt("topic")
        assert SEO_OUTLINE_FEW_SHOT in system
        assert "example of a strong SEO outline" in system

    def test_json_structure_requested(self):
        _, user = build_seo_outline_prompt("topic")
        assert "title" in user
        assert "slug" in user
        assert "meta_description" in user
        assert "sections" in user


class TestSEOOutlineSkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = SEOOutlineSkill()
        result = skill.run(SkillInput(text="AI in healthcare"))
        assert result.text
        assert result.metadata["locale"] == "en"

    def test_locale_switches(self):
        skill = SEOOutlineSkill()
        r_en = skill.run(SkillInput(text="topic", context={"locale": "en"}))
        r_zh = skill.run(SkillInput(text="topic", context={"locale": "zh"}))
        assert r_en.metadata["locale"] == "en"
        assert r_zh.metadata["locale"] == "zh"

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("seo_outline")
        assert skill.name == "seo_outline"
