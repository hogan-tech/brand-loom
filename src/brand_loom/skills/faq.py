"""FAQ generator skill — locale-parametric, single-locale default."""

from __future__ import annotations

from brand_loom.prompts.faq import build_faq_prompt, clamp_faq_count
from brand_loom.providers.base import get_provider
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class FAQSkill(Skill):
    """Generate FAQ question-answer pairs from body text."""

    @property
    def name(self) -> str:
        return "faq"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        topic = ctx.get("topic", "")
        count = clamp_faq_count(ctx.get("count", 5))
        locale = ctx.get("locale", "en")

        system, user = build_faq_prompt(
            inp.text,
            topic=topic,
            count=count,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        return SkillOutput(
            text=raw,
            metadata={"locale": locale, "count": count},
        )


register(FAQSkill())
