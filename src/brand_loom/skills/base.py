"""Skill base interface and data types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SkillInput:
    """Input to a skill."""

    text: str
    context: dict | None = None


@dataclass
class SkillOutput:
    """Output from a skill."""

    text: str
    metadata: dict = field(default_factory=dict)


class Skill(ABC):
    """Abstract base for all brand-loom skills."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique skill name used for registry lookup."""

    @abstractmethod
    def run(self, inp: SkillInput) -> SkillOutput:
        """Execute the skill."""
