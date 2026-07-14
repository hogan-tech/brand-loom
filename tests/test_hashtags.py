"""Tests for the hashtag generator skill."""

from brand_loom.prompts.hashtags import build_hashtag_prompt
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.hashtags import HashtagSkill


class TestHashtagPromptBuilder:
    def test_basic_prompt(self):
        system, user = build_hashtag_prompt("AI marketing")
        assert "hashtag" in user.lower()
        assert "AI marketing" in user
        assert "15" in user

    def test_custom_count(self):
        _, user = build_hashtag_prompt("topic", count=10)
        assert "10" in user

    def test_brand_context(self):
        system, _ = build_hashtag_prompt(
            "topic",
            brand_context={"tone": ["edgy"], "audience": "Gen Z"},
        )
        assert "edgy" in system
        assert "Gen Z" in system


class TestHashtagSkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = HashtagSkill()
        result = skill.run(SkillInput(text="cloud computing trends"))
        assert result.text
        assert isinstance(result.text, str)

    def test_respects_count_bound(self):
        skill = HashtagSkill()
        result = skill.run(SkillInput(
            text="marketing",
            context={"count": 5},
        ))
        assert result.text

    def test_brand_context(self):
        skill = HashtagSkill()
        result = skill.run(SkillInput(
            text="startup launch",
            context={"brand_context": {"tone": ["professional"]}},
        ))
        assert result.text

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("hashtags")
        assert skill.name == "hashtags"

    def test_skips_empty_tags(self):
        import json

        from brand_loom.providers.base import register_provider

        class StubProvider:
            def generate(self, prompt, *, system=None, max_tokens=1024,
                         temperature=0.7, model=None):
                return '["#ai", "", "  ", "#", "##", "AI", "ml"]'

        register_provider("stub-empty-tags", StubProvider())
        use_provider("stub-empty-tags")
        try:
            result = HashtagSkill().run(SkillInput(text="ai"))
            tags = json.loads(result.text)
            assert tags == ["#ai", "#ml"]
            assert result.metadata["count"] == 2
        finally:
            use_provider("fake")
