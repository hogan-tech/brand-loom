"""Prompt builder for the hook / headline generator skill."""

from __future__ import annotations


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
