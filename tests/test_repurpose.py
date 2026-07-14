"""Tests for the content repurposer skill."""

from brand_loom.prompts.repurpose import TARGET_FORMATS, build_repurpose_prompt
from brand_loom.providers import use_provider
from brand_loom.skills.base import SkillInput
from brand_loom.skills.repurpose import RepurposeSkill

SAMPLE_ARTICLE = (
    "We reduced our cloud infrastructure costs by 40% in three months. "
    "The key was right-sizing instances, switching to spot instances for batch jobs, "
    "and implementing auto-scaling policies that matched actual usage patterns."
)


class TestRepurposePromptBuilder:
    def test_basic_prompt(self):
        system, user = build_repurpose_prompt(SAMPLE_ARTICLE)
        assert "repurpose" in user.lower() or "content" in system.lower()

    def test_short_format(self):
        system, user = build_repurpose_prompt(SAMPLE_ARTICLE, target_format="short")
        assert "concise" in system.lower() or "social" in system.lower()

    def test_thread_format(self):
        system, user = build_repurpose_prompt(SAMPLE_ARTICLE, target_format="thread")
        assert "thread" in system.lower()

    def test_carousel_format(self):
        system, user = build_repurpose_prompt(SAMPLE_ARTICLE, target_format="carousel")
        assert "carousel" in system.lower()

    def test_brand_context(self):
        system, _ = build_repurpose_prompt(
            SAMPLE_ARTICLE,
            brand_context={"tone": ["informal"], "audience": "DevOps engineers"},
        )
        assert "informal" in system
        assert "DevOps engineers" in system


class TestRepurposeSkill:
    def setup_method(self):
        use_provider("fake")

    def test_short_format(self):
        skill = RepurposeSkill()
        result = skill.run(SkillInput(
            text=SAMPLE_ARTICLE,
            context={"target_format": "short"},
        ))
        assert result.text
        assert result.metadata["target_format"] == "short"

    def test_thread_format(self):
        skill = RepurposeSkill()
        result = skill.run(SkillInput(
            text=SAMPLE_ARTICLE,
            context={"target_format": "thread"},
        ))
        assert result.text
        assert result.metadata["target_format"] == "thread"

    def test_carousel_format(self):
        skill = RepurposeSkill()
        result = skill.run(SkillInput(
            text=SAMPLE_ARTICLE,
            context={"target_format": "carousel"},
        ))
        assert result.text
        assert result.metadata["target_format"] == "carousel"

    def test_default_format(self):
        skill = RepurposeSkill()
        result = skill.run(SkillInput(text=SAMPLE_ARTICLE))
        assert result.metadata["target_format"] == "short"

    def test_available_formats_in_metadata(self):
        skill = RepurposeSkill()
        result = skill.run(SkillInput(text=SAMPLE_ARTICLE))
        assert "short" in result.metadata["available_formats"]
        assert "thread" in result.metadata["available_formats"]
        assert "carousel" in result.metadata["available_formats"]
        assert len(result.metadata["available_formats"]) >= 3

    def test_at_least_3_formats_exist(self):
        assert len(TARGET_FORMATS) >= 3

    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("repurpose")
        assert skill.name == "repurpose"
