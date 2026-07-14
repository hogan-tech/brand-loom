"""Content repurposer skill — one source → many target formats."""

from __future__ import annotations

from brand_loom.prompts.repurpose import TARGET_FORMATS, build_repurpose_prompt
from brand_loom.providers.base import get_provider
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class RepurposeSkill(Skill):
    """Repurpose source content into a target format (short, thread, carousel, etc.)."""

    @property
    def name(self) -> str:
        return "repurpose"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        target_format = ctx.get("target_format", "short")
        locale = ctx.get("locale", "en")

        system, user = build_repurpose_prompt(
            inp.text,
            target_format=target_format,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        return SkillOutput(
            text=raw,
            metadata={
                "target_format": target_format,
                "locale": locale,
                "available_formats": list(TARGET_FORMATS.keys()),
            },
        )


register(RepurposeSkill())
