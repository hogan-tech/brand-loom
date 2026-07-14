"""Skill registry — register, discover, and resolve skills by name."""

from __future__ import annotations

from brand_loom.skills.base import Skill

_REGISTRY: dict[str, Skill] = {}


def register(skill: Skill) -> Skill:
    """Register a skill instance by its name."""
    _REGISTRY[skill.name] = skill
    return skill


def get_skill(name: str) -> Skill:
    """Look up a registered skill by name. Raises KeyError if not found."""
    try:
        return _REGISTRY[name]
    except KeyError:
        available = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise KeyError(f"Skill {name!r} not found. Available: {available}") from None


def list_skills() -> list[str]:
    """Return sorted list of registered skill names."""
    return sorted(_REGISTRY)
