"""Prompt builder for the CTA writer skill."""

from __future__ import annotations

CTA_FEW_SHOT = (
    "\n\nHere are examples of strong CTAs:\n"
    "Goal: free trial sign-up\n"
    '["Start your free trial — no credit card needed",'
    ' "See it in action: 14-day free trial",'
    ' "Try it free for 14 days, cancel anytime"]\n\n'
    "Goal: newsletter subscription\n"
    '["Get weekly insights — join 10,000+ marketers",'
    ' "Subscribe and never miss a strategy update",'
    ' "Join the list. One email a week, zero fluff."]'
)


def build_cta_prompt(
    goal: str,
    *,
    count: int = 5,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for CTA generation."""
    system = (
        f"You are a conversion copywriter. Write in {locale}. "
        "Generate compelling calls-to-action that drive action. "
        "Be clear, urgent, and benefit-focused."
        + CTA_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        do_phrases = brand_context.get("do_phrases", [])
        avoid_phrases = brand_context.get("avoid_phrases", [])
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."
        if do_phrases:
            system += f" Preferred phrases: {', '.join(do_phrases)}."
        if avoid_phrases:
            system += f" Avoid: {', '.join(avoid_phrases)}."

    user = (
        f"Generate exactly {count} call-to-action variants for the following goal.\n"
        f"Return a JSON array of strings.\n\n"
        f"Goal: {goal}"
    )

    return system, user
