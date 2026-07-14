"""SEO article outline skill — locale-parametric, structured output."""

from __future__ import annotations

from brand_loom.prompts.seo_outline import build_seo_outline_prompt
from brand_loom.providers.base import get_provider
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class SEOOutlineSkill(Skill):
    """Generate a structured SEO article outline."""

    @property
    def name(self) -> str:
        return "seo_outline"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        locale = ctx.get("locale", "en")
        section_count = ctx.get("section_count", 6)

        system, user = build_seo_outline_prompt(
            inp.text,
            locale=locale,
            section_count=section_count,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        return SkillOutput(
            text=raw,
            metadata={"locale": locale, "section_count": section_count},
        )


register(SEOOutlineSkill())
