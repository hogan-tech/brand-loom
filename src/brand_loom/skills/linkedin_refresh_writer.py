"""LinkedIn refresh writer skill — generate a fresh angle for an old post."""

from __future__ import annotations

import json

from brand_loom.prompts.linkedin_refresh import build_linkedin_refresh_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class LinkedInRefreshWriterSkill(Skill):
    """Given an old LinkedIn post, generate a fresh angle."""

    @property
    def name(self) -> str:
        return "linkedin_refresh_writer"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        angle = ctx.get("angle", "")
        locale = ctx.get("locale", "en")

        system, user = build_linkedin_refresh_prompt(
            inp.text,
            angle=angle,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        try:
            result = parse_json_response(raw)
            if isinstance(result, dict):
                return SkillOutput(
                    text=json.dumps(result, indent=2),
                    metadata={"angle": angle or "auto", "locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(LinkedInRefreshWriterSkill())
