"""Thin agent runner — run one skill or a simple linear chain.

This is the "no coding agent required" wedge. It resolves skills by name,
feeds output of one skill into the next, and returns the result.
It is NOT the Neoxra orchestrator — no Planner/Critic/2-pass/TrafficLoop.
"""

from __future__ import annotations

from brand_loom.skills.base import SkillInput, SkillOutput
from brand_loom.skills.registry import get_skill


def _ensure_skills_loaded() -> None:
    """Import all skill modules so they auto-register."""
    import brand_loom.skills.caption  # noqa: F401
    import brand_loom.skills.cta  # noqa: F401
    import brand_loom.skills.faq  # noqa: F401
    import brand_loom.skills.hashtags  # noqa: F401
    import brand_loom.skills.hook  # noqa: F401
    import brand_loom.skills.repurpose  # noqa: F401
    import brand_loom.skills.schema_org  # noqa: F401
    import brand_loom.skills.seo_outline  # noqa: F401


def run_skill(
    name: str,
    text: str,
    brand_context: dict | None = None,
    **extra_context,
) -> SkillOutput:
    """Run a single skill by name."""
    _ensure_skills_loaded()
    skill = get_skill(name)
    context = dict(extra_context)
    if brand_context:
        context["brand_context"] = brand_context
    return skill.run(SkillInput(text=text, context=context or None))


def run_chain(
    names: list[str],
    text: str,
    brand_context: dict | None = None,
    **extra_context,
) -> SkillOutput:
    """Run a linear chain of skills, passing each output as the next input.

    Single-pass, linear — no Planner/Critic/retries.
    """
    _ensure_skills_loaded()
    if not names:
        raise ValueError("Chain must contain at least one skill name.")

    current_text = text
    result = SkillOutput(text=text)

    for name in names:
        skill = get_skill(name)
        context = dict(extra_context)
        if brand_context:
            context["brand_context"] = brand_context
        result = skill.run(SkillInput(text=current_text, context=context or None))
        current_text = result.text

    return result
