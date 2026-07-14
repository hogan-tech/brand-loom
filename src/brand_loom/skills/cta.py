"""Call-to-action writer skill."""

from __future__ import annotations

import json

from brand_loom.prompts.cta import build_cta_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class CTASkill(Skill):
    """Generate call-to-action variants for a given goal."""

    @property
    def name(self) -> str:
        return "cta"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        count = ctx.get("count", 5)
        locale = ctx.get("locale", "en")

        system, user = build_cta_prompt(
            inp.text,
            count=count,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        try:
            ctas = parse_json_response(raw)
            if isinstance(ctas, list):
                return SkillOutput(
                    text=json.dumps(ctas, indent=2),
                    metadata={"count": len(ctas), "locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(CTASkill())
