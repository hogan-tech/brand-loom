"""Tests for the FAQ generator skill."""

from brand_loom.prompts.faq import build_faq_prompt
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.faq import FAQSkill

SAMPLE_BODY = (
    "Brand-loom is an open-source library of marketing skills that runs on any LLM. "
    "It supports OpenAI, Anthropic, Gemini, and Ollama. Skills include hooks, captions, "
    "hashtags, and SEO outlines. A hosted version with voice extraction is available at neoxra.com."
)


class TestFAQPromptBuilder:
    def test_basic_prompt(self):
        system, user = build_faq_prompt(SAMPLE_BODY)
        assert "faq" in user.lower()
        assert "5" in user  # default count

    def test_count_clamped_min(self):
        _, user = build_faq_prompt(SAMPLE_BODY, count=1)
        assert "3" in user  # clamped to 3

    def test_count_clamped_max(self):
        _, user = build_faq_prompt(SAMPLE_BODY, count=20)
        assert "6" in user  # clamped to 6

    def test_topic_included(self):
        _, user = build_faq_prompt(SAMPLE_BODY, topic="brand-loom")
        assert "brand-loom" in user

    def test_locale(self):
        system, _ = build_faq_prompt(SAMPLE_BODY, locale="ja")
        assert "ja" in system

    def test_brand_context(self):
        system, _ = build_faq_prompt(
            SAMPLE_BODY,
            brand_context={"tone": ["friendly"], "audience": "marketers"},
        )
        assert "friendly" in system
        assert "marketers" in system

    def test_json_structure_requested(self):
        _, user = build_faq_prompt(SAMPLE_BODY)
        assert "question" in user
        assert "answer" in user


class TestFAQSkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = FAQSkill()
        result = skill.run(SkillInput(text=SAMPLE_BODY))
        assert result.text
        assert result.metadata["locale"] == "en"

    def test_locale_param(self):
        skill = FAQSkill()
        result = skill.run(SkillInput(text=SAMPLE_BODY, context={"locale": "fr"}))
        assert result.metadata["locale"] == "fr"

    def test_topic_param(self):
        skill = FAQSkill()
        result = skill.run(SkillInput(
            text=SAMPLE_BODY,
            context={"topic": "brand-loom"},
        ))
        assert result.text

    def test_metadata_reports_clamped_count(self):
        skill = FAQSkill()
        result = skill.run(SkillInput(text=SAMPLE_BODY, context={"count": 10}))
        assert result.metadata["count"] == 6

        result = skill.run(SkillInput(text=SAMPLE_BODY, context={"count": 1}))
        assert result.metadata["count"] == 3

    def test_metadata_count_within_range_unchanged(self):
        skill = FAQSkill()
        result = skill.run(SkillInput(text=SAMPLE_BODY, context={"count": 4}))
        assert result.metadata["count"] == 4

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("faq")
        assert skill.name == "faq"
