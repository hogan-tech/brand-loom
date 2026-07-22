"""LinkedIn post scorer skill — 6-metric evaluation."""

from __future__ import annotations

import json

from brand_loom.prompts.linkedin_post_scorer import METRICS, build_linkedin_post_scorer_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class LinkedInPostScorerSkill(Skill):
    """Score a LinkedIn post on 6 metrics.

    Metrics: hook, skimmability, engagement, length, cta, voice_match.
    """

    @property
    def name(self) -> str:
        return "linkedin_post_scorer"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        locale = ctx.get("locale", "en")

        system, user = build_linkedin_post_scorer_prompt(
            inp.text,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        try:
            scores = parse_json_response(raw)
            if isinstance(scores, dict):
                return SkillOutput(
                    text=json.dumps(scores, indent=2),
                    metadata={"metrics": METRICS, "locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(LinkedInPostScorerSkill())
