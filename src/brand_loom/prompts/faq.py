"""Prompt builder for the FAQ generator skill."""

from __future__ import annotations

FAQ_MIN_COUNT = 3
FAQ_MAX_COUNT = 6


def clamp_faq_count(count: int) -> int:
    """Clamp the requested pair count to the supported 3-6 range."""
    return max(FAQ_MIN_COUNT, min(FAQ_MAX_COUNT, count))


def build_faq_prompt(
    body: str,
    *,
    topic: str = "",
    count: int = 5,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for FAQ generation."""
    count = clamp_faq_count(count)

    system = (
        f"You are a content strategist. Write in {locale}. "
        "Generate clear, helpful FAQ pairs that anticipate what readers will ask."
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."

    topic_line = f" about \"{topic}\"" if topic else ""
    user = (
        f"Generate exactly {count} FAQ pairs{topic_line} based on the content below.\n"
        f"Return a JSON array of objects, each with \"question\" and \"answer\" keys.\n\n"
        f"Content:\n{body}"
    )

    return system, user
