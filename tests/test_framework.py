"""Tests for the skill framework: base types and registry."""

import pytest

from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import get_skill, list_skills, register


class EchoSkill(Skill):
    @property
    def name(self) -> str:
        return "echo"

    def run(self, inp: SkillInput) -> SkillOutput:
        return SkillOutput(text=inp.text, metadata={"echoed": True})


def test_skill_input_defaults():
    inp = SkillInput(text="hello")
    assert inp.text == "hello"
    assert inp.context is None


def test_skill_output_defaults():
    out = SkillOutput(text="result")
    assert out.metadata == {}


def test_echo_skill_run():
    skill = EchoSkill()
    assert skill.name == "echo"
    result = skill.run(SkillInput(text="test"))
    assert result.text == "test"
    assert result.metadata == {"echoed": True}


def test_register_and_get():
    skill = EchoSkill()
    register(skill)
    assert get_skill("echo") is skill


def test_list_skills():
    register(EchoSkill())
    names = list_skills()
    assert "echo" in names


def test_get_skill_not_found():
    with pytest.raises(KeyError, match="nonexistent"):
        get_skill("nonexistent")
