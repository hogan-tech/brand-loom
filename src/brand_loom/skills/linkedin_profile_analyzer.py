"""LinkedIn profile analyzer skill — headline + about improvements."""

from __future__ import annotations

import json

from brand_loom.prompts.linkedin_profile import build_linkedin_profile_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class LinkedInProfileAnalyzerSkill(Skill):
    """Analyse LinkedIn profile text and suggest headline + about improvements."""

    @property
    def name(self) -> str:
        return "linkedin_profile_analyzer"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        locale = ctx.get("locale", "en")

        system, user = build_linkedin_profile_prompt(
            inp.text,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        try:
            analysis = parse_json_response(raw)
            if isinstance(analysis, dict):
                return SkillOutput(
                    text=json.dumps(analysis, indent=2),
                    metadata={"locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(LinkedInProfileAnalyzerSkill())
