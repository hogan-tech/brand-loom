#!/usr/bin/env python3
"""Provider parity eval — run every skill on every available provider.

Usage:
    # Fake only (zero keys):
    python scripts/eval_parity.py

    # With real providers (BYOK):
    OPENAI_API_KEY=sk-... ANTHROPIC_API_KEY=sk-... python scripts/eval_parity.py

Prints a results table showing pass/fail per skill × provider.
"""

from __future__ import annotations

import os
import sys
import traceback

# Ensure the package is importable when run from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from brand_loom.agent import run_skill  # noqa: E402
from brand_loom.providers import use_provider  # noqa: E402

SKILLS = [
    "bilingual", "hook", "caption", "hashtags", "cta", "faq", "repurpose", "seo_outline",
]

SKILL_INPUTS = {
    "bilingual": "Ship it, then iterate. Perfection is the enemy of progress.",
    "hook": "How to reduce cloud costs by 40%",
    "caption": "Launch of our new AI analytics dashboard",
    "hashtags": "sustainable fashion for Gen Z",
    "cta": "sign up for a free 14-day trial",
    "faq": (
        "Brand-loom is an open-source library of marketing skills. "
        "It supports OpenAI, Anthropic, Gemini, and Ollama."
    ),
    "repurpose": (
        "We reduced cloud costs by 40% in three months by right-sizing "
        "instances and switching to spot instances for batch workloads."
    ),
    "seo_outline": "best project management tools for startups in 2025",
}


def _available_providers() -> list[str]:
    providers = ["fake"]
    if os.environ.get("OPENAI_API_KEY"):
        providers.append("openai")
    if os.environ.get("ANTHROPIC_API_KEY"):
        providers.append("anthropic")
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        providers.append("gemini")
    return providers


def main() -> None:
    providers = _available_providers()
    print(f"Providers: {', '.join(providers)}\n")

    # Header
    header = f"{'skill':<15}" + "".join(f"{p:<15}" for p in providers)
    print(header)
    print("-" * len(header))

    all_pass = True
    for skill in SKILLS:
        row = f"{skill:<15}"
        for provider in providers:
            try:
                use_provider(provider)
                result = run_skill(skill, SKILL_INPUTS[skill])
                if result.text and len(result.text.strip()) > 0:
                    row += f"{'PASS':<15}"
                else:
                    row += f"{'FAIL (empty)':<15}"
                    all_pass = False
            except Exception:
                row += f"{'FAIL (error)':<15}"
                traceback.print_exc()
                all_pass = False
        print(row)

    print()
    if all_pass:
        print("All skills passed on all available providers.")
    else:
        print("Some skills failed — see details above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
