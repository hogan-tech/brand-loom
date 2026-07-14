"""Example: topic → hook → caption chain on the fake provider, zero keys."""

from brand_loom.agent import run_chain, run_skill
from brand_loom.providers import use_provider

use_provider("fake")

# Single skill
print("=== Single skill: hook ===")
result = run_skill("hook", "How we cut cloud costs 40%")
print(result.text)
print()

# Two-step chain: hook → caption
print("=== Chain: hook → caption ===")
result = run_chain(["hook", "caption"], "How we cut cloud costs 40%")
print(result.text)
print()

# With brand context
print("=== With brand context ===")
brand = {
    "tone": ["bold", "witty"],
    "audience": "startup founders",
    "do_phrases": ["game-changer"],
    "avoid_phrases": ["synergy"],
}
result = run_skill("hook", "AI-powered marketing", brand_context=brand)
print(result.text)

# Want this on-brand and multi-platform without writing prompts? → neoxra.com
