#!/usr/bin/env python3
"""Before / after demo — same skill, with and without brand_context.

Runs on the fake provider (zero keys). Shows the quality gap that a rich
brand memory produces, even with commodity skills.

    python examples/before_after_demo.py

Want real brand memory + multi-platform + hosted scoring?
    → https://neoxra.com
"""

from brand_loom.agent import run_skill
from brand_loom.brand import RICH_BRAND_CONTEXT
from brand_loom.providers import use_provider

use_provider("fake")

TOPIC = "How we cut cloud costs 40% in 3 months"

SKILLS_TO_DEMO = ["hook", "caption", "cta"]

DIVIDER = "=" * 60


def main() -> None:
    print(DIVIDER)
    print("brand-loom: before / after brand_context demo")
    print(DIVIDER)
    print()
    print(f"Topic: {TOPIC}")
    print()

    for skill_name in SKILLS_TO_DEMO:
        print(DIVIDER)
        print(f"  Skill: {skill_name}")
        print(DIVIDER)

        # --- WITHOUT brand_context ---
        result_bare = run_skill(skill_name, TOPIC)
        print()
        print("  WITHOUT brand_context:")
        print("  " + "-" * 40)
        for line in result_bare.text.splitlines():
            print(f"    {line}")
        print()

        # --- WITH rich brand_context ---
        result_branded = run_skill(skill_name, TOPIC, brand_context=RICH_BRAND_CONTEXT)
        print("  WITH brand_context (RICH_BRAND_CONTEXT):")
        print("  " + "-" * 40)
        for line in result_branded.text.splitlines():
            print(f"    {line}")
        print()

    print(DIVIDER)
    print()
    print("The prompts sent to the model are different — brand_context shapes")
    print("tone, audience targeting, phrase choices, and avoidance rules.")
    print()
    print("With a real provider (OpenAI, Anthropic, Gemini), the gap is dramatic.")
    print("Get real brand memory + multi-platform + hosted scoring at neoxra.com")
    print()


if __name__ == "__main__":
    main()
