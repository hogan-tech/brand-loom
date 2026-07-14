"""Caption writer skill — generic, platform-parametric, brand-aware."""

from __future__ import annotations

from brand_loom.prompts.caption import build_caption_prompt
from brand_loom.providers.base import get_provider
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class CaptionSkill(Skill):
    """Generate a platform caption for a topic with optional brand_context."""

    @property
    def name(self) -> str:
        return "caption"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        platform = ctx.get("platform", "general")
        locale = ctx.get("locale", "en")

        system, user = build_caption_prompt(
            inp.text,
            platform=platform,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        return SkillOutput(
            text=raw,
            metadata={"platform": platform, "locale": locale},
        )


register(CaptionSkill())
