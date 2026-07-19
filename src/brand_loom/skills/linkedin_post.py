"""LinkedIn post generator skill — milestone/topic to engaging post."""

from __future__ import annotations

from brand_loom.prompts.linkedin_post import POST_TYPES, build_linkedin_post_prompt
from brand_loom.providers.base import get_provider
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class LinkedInPostSkill(Skill):
    """Generate an engaging LinkedIn post from a milestone or topic."""

    @property
    def name(self) -> str:
        return "linkedin_post"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        post_type = ctx.get("post_type", "text")
        locale = ctx.get("locale", "en")

        system, user = build_linkedin_post_prompt(
            inp.text,
            post_type=post_type,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        return SkillOutput(
            text=raw,
            metadata={
                "post_type": post_type,
                "locale": locale,
                "available_types": sorted(POST_TYPES),
            },
        )


register(LinkedInPostSkill())
