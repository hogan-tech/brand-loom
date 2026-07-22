"""LinkedIn hook generator skill — 5 hook variants for a topic."""

from __future__ import annotations

import json

from brand_loom.prompts.linkedin_hook import build_linkedin_hook_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class LinkedInHookGeneratorSkill(Skill):
    """Generate 5 LinkedIn-optimised hook variants for a topic."""

    @property
    def name(self) -> str:
        return "linkedin_hook_generator"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        count = ctx.get("count", 5)
        locale = ctx.get("locale", "en")

        system, user = build_linkedin_hook_prompt(
            inp.text,
            count=count,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        try:
            hooks = parse_json_response(raw)
            if isinstance(hooks, list):
                return SkillOutput(
                    text=json.dumps(hooks, indent=2),
                    metadata={"count": len(hooks), "locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        # Fallback: return raw text
        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(LinkedInHookGeneratorSkill())
