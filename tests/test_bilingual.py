"""Tests for the bilingual translation skill."""

from brand_loom.prompts.bilingual import (
    BILINGUAL_FEW_SHOT,
    SUPPORTED_LOCALES,
    build_bilingual_prompt,
)
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.bilingual import BilingualSkill


class TestBilingualPromptBuilder:
    def test_basic_prompt(self):
        system, user = build_bilingual_prompt("Hello world")
        assert "zh-TW" in user
        assert "translation" in user
        assert "Hello world" in user

    def test_target_locale_in_prompt(self):
        system, user = build_bilingual_prompt("Test", target_locale="en")
        assert "en" in user

    def test_few_shot_in_system(self):
        system, _ = build_bilingual_prompt("Test")
        assert BILINGUAL_FEW_SHOT in system

    def test_preserve_terms_in_user(self):
        _, user = build_bilingual_prompt(
            "Neoxra uses GEO scoring.",
            preserve_terms=["Neoxra", "GEO"],
        )
        assert "Neoxra" in user
        assert "GEO" in user
        assert "do not translate" in user

    def test_brand_context(self):
        system, _ = build_bilingual_prompt(
            "Test",
            brand_context={"tone": ["bold"], "audience": "founders"},
        )
        assert "bold" in system
        assert "founders" in system

    def test_supported_locales(self):
        assert "en" in SUPPORTED_LOCALES
        assert "zh-TW" in SUPPORTED_LOCALES


class TestBilingualSkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = BilingualSkill()
        result = skill.run(SkillInput(
            text="Ship it, then iterate.",
            context={"target_locale": "zh-TW"},
        ))
        assert result.text
        assert result.metadata["target_locale"] == "zh-TW"

    def test_same_locale_returns_unchanged(self):
        skill = BilingualSkill()
        result = skill.run(SkillInput(
            text="Same text",
            context={"target_locale": "en", "source_locale": "en"},
        ))
        assert result.text == "Same text"
        assert result.metadata["unchanged"] is True

    def test_unsupported_locale_returns_error(self):
        skill = BilingualSkill()
        result = skill.run(SkillInput(
            text="Hello",
            context={"target_locale": "fr"},
        ))
        assert result.text == "Hello"
        assert "error" in result.metadata

    def test_preserve_terms_in_metadata(self):
        skill = BilingualSkill()
        result = skill.run(SkillInput(
            text="Neoxra is great.",
            context={"target_locale": "zh-TW", "preserve_terms": ["Neoxra"]},
        ))
        assert result.metadata["preserve_terms"] == ["Neoxra"]

    def test_brand_context(self):
        skill = BilingualSkill()
        result = skill.run(SkillInput(
            text="Test copy.",
            context={
                "target_locale": "zh-TW",
                "brand_context": {"tone": ["witty"]},
            },
        ))
        assert result.text

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("bilingual")
        assert skill.name == "bilingual"

    def test_default_target_is_zh_tw(self):
        skill = BilingualSkill()
        result = skill.run(SkillInput(text="Hello world"))
        assert result.metadata["target_locale"] == "zh-TW"
