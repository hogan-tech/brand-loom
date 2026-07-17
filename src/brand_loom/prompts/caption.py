"""Prompt builder for the caption writer skill."""

from __future__ import annotations

CAPTION_FEW_SHOT = (
    "\n\nHere are examples of strong captions:\n"
    'Topic: sustainable fashion\n'
    '{"caption": "Your closet doesn\'t need more clothes — it needs better ones. '
    "We partnered with 3 local makers to bring you pieces that last decades, not seasons. "
    'Which one are you adding first? \\n\\nLink in bio.", "platform": "instagram"}\n\n'
    'Topic: product launch\n'
    '{"caption": "6 months of late nights. 200+ beta testers. 1 big idea. '
    "Today it's yours. Meet our new analytics dashboard — built for teams "
    'who\'d rather ship than stare at spreadsheets. Try it free.", "platform": "linkedin"}'
)


def build_caption_prompt(
    topic: str,
    *,
    platform: str = "general",
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for caption generation.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a social media copywriter. Write in {locale}. "
        f"Create engaging captions optimized for {platform}. "
        "Be authentic, relatable, and include a clear call to action."
        + CAPTION_FEW_SHOT
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
        f"Write a caption for {platform} about the following topic.\n"
        f"Return a JSON object with keys: \"caption\" (the text) and "
        f"\"platform\" (\"{platform}\").\n\n"
        f"Topic: {topic}"
    )

    return system, user
