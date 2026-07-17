"""Prompt builder for the SEO outline skill."""

from __future__ import annotations

SEO_OUTLINE_FEW_SHOT = (
    "\n\nHere is an example of a strong SEO outline:\n"
    "Topic: best project management tools for startups\n"
    '{"title": "Best Project Management Tools for Startups in 2025",'
    ' "slug": "best-project-management-tools-startups",'
    ' "meta_description": "Compare the top project management tools for startups. '
    'We cover pricing, features, and team size fit so you can pick the right one.",'
    ' "sections": ['
    '{"heading": "Why Startups Need a Dedicated PM Tool", '
    '"key_points": ["Spreadsheets break at 5+ people", "Visibility reduces duplicate work"]},'
    ' {"heading": "Top 5 Tools Compared", '
    '"key_points": ["Feature matrix", "Pricing tiers", "Free-plan limits"]}]}'
)


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
        + SEO_OUTLINE_FEW_SHOT
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
