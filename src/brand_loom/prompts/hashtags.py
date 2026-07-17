"""Prompt builder for the hashtag generator skill."""

from __future__ import annotations

HASHTAG_FEW_SHOT = (
    "\n\nHere are examples of strong hashtag sets:\n"
    "Topic: home coffee brewing\n"
    '["#CoffeeBrewing", "#HomeCafe", "#PourOver", "#SpecialtyCoffee", "#MorningRoutine"]\n\n'
    "Topic: B2B SaaS marketing\n"
    '["#B2BSaaS", "#SaaSGrowth", "#MarketingStrategy", "#DemandGen", "#StartupMarketing"]'
)


def build_hashtag_prompt(
    topic: str,
    *,
    count: int = 15,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for hashtag generation."""
    system = (
        f"You are a social media strategist. Write in {locale}. "
        "Generate relevant, discoverable hashtags. Mix popular broad tags "
        "with niche-specific ones for optimal reach."
        + HASHTAG_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Brand tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."

    user = (
        f"Generate exactly {count} relevant hashtags for the following topic.\n"
        f"Return them as a JSON array of strings (each starting with #).\n"
        f"No duplicates.\n\n"
        f"Topic: {topic}"
    )

    return system, user
