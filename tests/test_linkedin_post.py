"""Tests for the LinkedIn post generator skill."""

from brand_loom.prompts.linkedin_post import (
    LINKEDIN_FEW_SHOT,
    POST_TYPES,
    build_linkedin_post_prompt,
)
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.linkedin_post import LinkedInPostSkill


class TestLinkedInPostPromptBuilder:
    def test_basic_prompt(self):
        system, user = build_linkedin_post_prompt("raised Series A")
        assert "linkedin" in user.lower()
        assert "raised Series A" in user

    def test_few_shot_in_system(self):
        system, _ = build_linkedin_post_prompt("milestone")
        assert LINKEDIN_FEW_SHOT in system

    def test_post_type_in_prompt(self):
        _, user = build_linkedin_post_prompt("topic", post_type="article")
        assert "article" in user

    def test_invalid_post_type_defaults_to_text(self):
        _, user = build_linkedin_post_prompt("topic", post_type="invalid")
        assert "text" in user

    def test_locale(self):
        system, _ = build_linkedin_post_prompt("topic", locale="zh")
        assert "zh" in system

    def test_brand_context(self):
        system, _ = build_linkedin_post_prompt(
            "topic",
            brand_context={
                "tone": ["confident"],
                "audience": "SaaS founders",
                "do_phrases": ["ship it"],
                "avoid_phrases": ["synergy"],
            },
        )
        assert "confident" in system
        assert "SaaS founders" in system
        assert "ship it" in system
        assert "synergy" in system

    def test_supported_post_types(self):
        assert "text" in POST_TYPES
        assert "article" in POST_TYPES
        assert "carousel" in POST_TYPES


class TestLinkedInPostSkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = LinkedInPostSkill()
        result = skill.run(SkillInput(text="Just hit 10k users"))
        assert result.text
        assert result.metadata["post_type"] == "text"

    def test_article_type(self):
        skill = LinkedInPostSkill()
        result = skill.run(SkillInput(
            text="Our open source journey",
            context={"post_type": "article"},
        ))
        assert result.metadata["post_type"] == "article"

    def test_available_types_in_metadata(self):
        skill = LinkedInPostSkill()
        result = skill.run(SkillInput(text="milestone"))
        assert "text" in result.metadata["available_types"]
        assert "article" in result.metadata["available_types"]
        assert "carousel" in result.metadata["available_types"]

    def test_brand_context(self):
        skill = LinkedInPostSkill()
        result = skill.run(SkillInput(
            text="product launch",
            context={"brand_context": {"tone": ["bold", "direct"]}},
        ))
        assert result.text

    def test_locale(self):
        skill = LinkedInPostSkill()
        result = skill.run(SkillInput(
            text="milestone",
            context={"locale": "zh-TW"},
        ))
        assert result.metadata["locale"] == "zh-TW"

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("linkedin_post")
        assert skill.name == "linkedin_post"
