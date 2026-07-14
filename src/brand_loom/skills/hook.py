"""Hook / headline generator skill."""

from __future__ import annotations

import json

from brand_loom.prompts.hook import build_hook_prompt
from brand_loom.providers.base import get_provider
from brand_loom.providers.parsing import parse_json_response
from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


class HookSkill(Skill):
    """Generate attention-grabbing hooks/headlines for a topic."""

    @property
    def name(self) -> str:
        return "hook"

    def run(self, inp: SkillInput) -> SkillOutput:
        brand_context = inp.context.get("brand_context") if inp.context else None
        count = (inp.context or {}).get("count", 5)
        locale = (inp.context or {}).get("locale", "en")

        system, user = build_hook_prompt(
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

    def run_topic(self, topic: str, **kwargs) -> str:
        """Convenience: generate hooks for a topic string."""
        result = self.run(SkillInput(text=topic, context=kwargs or None))
        return result.text


register(HookSkill())
