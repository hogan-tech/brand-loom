"""Prompt builder for the content repurposer skill."""

from __future__ import annotations

TARGET_FORMATS = {
    "short": "a concise social media post (1-3 sentences)",
    "thread": "a Twitter/X thread (5-8 numbered tweets, each under 280 chars)",
    "carousel": "carousel slide copy (5-8 slides, each with a headline and 1-2 sentences)",
    "summary": "a brief executive summary (3-5 bullet points)",
    "email": "a short email newsletter snippet with subject line",
}

REPURPOSE_FEW_SHOT = (
    "\n\nHere are examples of strong repurposed content:\n"
    "Format: short (social post)\n"
    '{"format": "short", "content": "We analyzed 500 landing pages. '
    "The ones that converted best had one thing in common: a single, "
    'clear CTA above the fold. Fewer choices = more clicks."}\n\n'
    "Format: summary (executive bullets)\n"
    '{"format": "summary", "content": '
    '"• Remote teams with async-first practices ship 30% faster\\n'
    "• Daily standups don't improve velocity — weekly syncs do\\n"
    '• Written updates outperform video check-ins for knowledge retention"}'
)


def build_repurpose_prompt(
    source_text: str,
    *,
    target_format: str = "short",
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for content repurposing."""
    format_desc = TARGET_FORMATS.get(target_format, target_format)

    system = (
        f"You are a content strategist. Write in {locale}. "
        f"Repurpose the given content into {format_desc}. "
        "Preserve the key message and value while adapting the format."
        + REPURPOSE_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."

    user = (
        f"Repurpose the following content into: {format_desc}.\n"
        f"Return a JSON object with keys: \"format\" (\"{target_format}\") "
        f"and \"content\" (the repurposed text).\n\n"
        f"Source content:\n{source_text}"
    )

    return system, user
