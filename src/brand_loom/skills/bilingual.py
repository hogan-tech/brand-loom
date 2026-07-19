"""Bilingual translation skill — EN <-> zh-TW voice-preserving rewrite."""

from __future__ import annotations

from brand_loom.prompts.bilingual import SUPPORTED_LOCALES, build_bilingual_prompt
from brand_loom.providers.base import get_provider
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class BilingualSkill(Skill):
    """Translate marketing copy between EN and zh-TW preserving brand voice."""

    @property
    def name(self) -> str:
        return "bilingual"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        target_locale = ctx.get("target_locale", "zh-TW")
        preserve_terms = ctx.get("preserve_terms", [])

        # If target matches source locale hint, return unchanged
        source_locale = ctx.get("source_locale")
        if source_locale and source_locale == target_locale:
            return SkillOutput(
                text=inp.text,
                metadata={
                    "target_locale": target_locale,
                    "unchanged": True,
                    "note": "Source and target locale are the same.",
                },
            )

        if target_locale not in SUPPORTED_LOCALES:
            return SkillOutput(
                text=inp.text,
                metadata={
                    "target_locale": target_locale,
                    "error": f"Unsupported locale: {target_locale}. "
                    f"Supported: {', '.join(sorted(SUPPORTED_LOCALES))}",
                },
            )

        system, user = build_bilingual_prompt(
            inp.text,
            target_locale=target_locale,
            brand_context=brand_context,
            preserve_terms=preserve_terms,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        return SkillOutput(
            text=raw,
            metadata={
                "target_locale": target_locale,
                "preserve_terms": preserve_terms,
                "supported_locales": sorted(SUPPORTED_LOCALES),
            },
        )


register(BilingualSkill())
