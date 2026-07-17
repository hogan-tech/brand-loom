"""Prompt builder for the hook / headline generator skill."""

from __future__ import annotations

HOOK_FEW_SHOT = (
    "\n\nHere are examples of strong hooks:\n"
    "Topic: remote work productivity\n"
    '["We tracked 1,000 remote teams for a year — here\'s what the top 1% do differently",'
    ' "Your home office is costing you 2 hours a day (and you don\'t even notice)",'
    ' "I managed 50 remote engineers. The #1 mistake? Meetings."]\n\n'
    "Topic: email marketing\n"
    '["We deleted 80% of our email list. Revenue went up.",'
    ' "The subject line formula that doubled our open rate overnight",'
    ' "Stop sending newsletters. Start sending this instead."]'
)


def build_hook_prompt(
    topic: str,
    *,
    count: int = 5,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for hook generation.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a marketing copywriter. Write in {locale}. "
        "Generate attention-grabbing hooks and headlines. "
        "Be concise, punchy, and scroll-stopping."
        + HOOK_FEW_SHOT
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
            system += f" Preferred phrases/style: {', '.join(do_phrases)}."
        if avoid_phrases:
            system += f" Avoid: {', '.join(avoid_phrases)}."

    user = (
        f"Generate exactly {count} hook/headline options for the following topic.\n"
        f"Return them as a JSON array of strings.\n\n"
        f"Topic: {topic}"
    )

    return system, user
