"""Hashtag generator skill."""

from __future__ import annotations

import json

from brand_loom.prompts.hashtags import build_hashtag_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class HashtagSkill(Skill):
    """Generate a deduped, count-bounded hashtag set for a topic."""

    @property
    def name(self) -> str:
        return "hashtags"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        brand_context = ctx.get("brand_context")
        count = ctx.get("count", 15)
        locale = ctx.get("locale", "en")

        system, user = build_hashtag_prompt(
            inp.text,
            count=count,
            locale=locale,
            brand_context=brand_context,
        )

        provider = get_provider()
        raw = provider.generate(user, system=system)

        try:
            tags = parse_json_response(raw)
            if isinstance(tags, list):
                # Dedupe and ensure # prefix
                seen: set[str] = set()
                deduped: list[str] = []
                for tag in tags:
                    t = str(tag).strip()
                    if not t.startswith("#"):
                        t = f"#{t}"
                    lower = t.lower()
                    if lower not in seen:
                        seen.add(lower)
                        deduped.append(t)
                deduped = deduped[:count]
                return SkillOutput(
                    text=json.dumps(deduped, indent=2),
                    metadata={"count": len(deduped), "locale": locale},
                )
        except (ValueError, json.JSONDecodeError):
            pass

        return SkillOutput(text=raw, metadata={"raw": True, "locale": locale})


register(HashtagSkill())
