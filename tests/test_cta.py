"""Tests for the CTA writer skill."""

from brand_loom.prompts.cta import build_cta_prompt
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.cta import CTASkill


class TestCTAPromptBuilder:
    def test_basic_prompt(self):
        system, user = build_cta_prompt("sign up for a free trial")
        assert "call-to-action" in user.lower() or "cta" in user.lower()
        assert "sign up" in user

    def test_custom_count(self):
        _, user = build_cta_prompt("subscribe", count=3)
        assert "3" in user

    def test_locale(self):
        system, _ = build_cta_prompt("subscribe", locale="es")
        assert "es" in system

    def test_brand_context(self):
        system, _ = build_cta_prompt(
            "subscribe",
            brand_context={
                "tone": ["urgent", "friendly"],
                "audience": "small business owners",
                "do_phrases": ["get started"],
                "avoid_phrases": ["buy now"],
            },
        )
        assert "urgent" in system
        assert "small business owners" in system
        assert "get started" in system
        assert "buy now" in system


class TestCTASkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = CTASkill()
        result = skill.run(SkillInput(text="sign up for a free trial"))
        assert result.text
        assert isinstance(result.text, str)

    def test_brand_context(self):
        skill = CTASkill()
        result = skill.run(SkillInput(
            text="download the ebook",
            context={"brand_context": {"tone": ["professional"]}},
        ))
        assert result.text

    def test_custom_count(self):
        skill = CTASkill()
        result = skill.run(SkillInput(
            text="book a demo",
            context={"count": 3},
        ))
        assert result.text

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("cta")
        assert skill.name == "cta"
