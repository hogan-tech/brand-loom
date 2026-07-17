"""Tests for the hook / headline generator skill."""

from brand_loom.prompts.hook import HOOK_FEW_SHOT, build_hook_prompt
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.hook import HookSkill


class TestHookPromptBuilder:
    def test_basic_prompt(self):
        system, user = build_hook_prompt("cloud costs")
        assert "hook" in user.lower() or "headline" in user.lower()
        assert "cloud costs" in user
        assert "5" in user  # default count

    def test_locale(self):
        system, user = build_hook_prompt("topic", locale="zh")
        assert "zh" in system

    def test_brand_context_influences_prompt(self):
        ctx = {
            "tone": ["bold", "witty"],
            "audience": "startup founders",
            "do_phrases": ["game-changer"],
            "avoid_phrases": ["synergy"],
        }
        system, user = build_hook_prompt("topic", brand_context=ctx)
        assert "bold" in system
        assert "startup founders" in system
        assert "game-changer" in system
        assert "synergy" in system

    def test_few_shot_exemplars_in_system(self):
        system, _ = build_hook_prompt("topic")
        assert HOOK_FEW_SHOT in system
        assert "examples of strong hooks" in system

    def test_custom_count(self):
        _, user = build_hook_prompt("topic", count=3)
        assert "3" in user


class TestHookSkill:
    def setup_method(self):
        use_provider("fake")

    def test_returns_output(self):
        skill = HookSkill()
        result = skill.run(SkillInput(text="How we cut cloud costs 40%"))
        assert result.text
        assert isinstance(result.text, str)

    def test_run_topic_convenience(self):
        skill = HookSkill()
        text = skill.run_topic("AI in marketing")
        assert text
        assert isinstance(text, str)

    def test_brand_context(self):
        skill = HookSkill()
        result = skill.run(SkillInput(
            text="product launch",
            context={"brand_context": {"tone": ["professional"]}},
        ))
        assert result.text

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("hook")
        assert skill.name == "hook"
