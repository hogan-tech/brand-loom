"""LinkedIn comment drafter skill — draft a comment on a target post."""

from __future__ import annotations

import json

from brand_loom.prompts.linkedin_comment import build_linkedin_comment_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class LinkedInCommentDrafterSkill(Skill):
    """Draft a thoughtful comment on a target LinkedIn post."""

    @property
    def name(self) -> str:
        return "linkedin_comment_drafter"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        your_context = ctx.get("your_context", "")
        style = ctx.get("style", "value-add")
        locale = ctx.get("locale", "en")

        system, user = build_linkedin_comment_prompt(
            inp.text,
            your_context=your_context,
            style=style,
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
                    metadata={"style": style, "locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(LinkedInCommentDrafterSkill())
