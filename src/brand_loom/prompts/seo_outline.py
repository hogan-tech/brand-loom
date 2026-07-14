"""Prompt builder for the SEO outline skill."""

from __future__ import annotations


def build_seo_outline_prompt(
    topic: str,
    *,
    locale: str = "en",
    section_count: int = 6,
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for SEO article outline generation."""
    section_count = max(4, min(8, section_count))

    system = (
        f"You are an SEO content strategist. Write in {locale}. "
        "Create structured, search-optimized article outlines that target "
        "featured snippets and long-tail keywords."
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."

    user = (
        f"Create an SEO article outline for the following topic.\n"
        f"Include exactly {section_count} H2 sections (no more, no less).\n\n"
        f"Return a JSON object with these keys:\n"
        f'- "title": the article title\n'
        f'- "slug": URL-friendly slug\n'
        f'- "meta_description": under 160 characters\n'
        f'- "sections": array of objects, each with "heading" (H2) and '
        f'"key_points" (array of strings)\n\n'
        f"Topic: {topic}"
    )

    return system, user
