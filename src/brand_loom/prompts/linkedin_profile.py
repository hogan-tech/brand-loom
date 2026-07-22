"""Prompt builder for the LinkedIn profile analyzer skill."""

from __future__ import annotations

PROFILE_FEW_SHOT = (
    "\n\nHere is an example analysis:\n"
    "Profile headline: \"Software Engineer at BigCo\"\n"
    "About: \"I write code.\"\n\n"
    '{"headline_score": 3, '
    '"suggested_headlines": ['
    '"Engineering Leader | Scaling distributed systems from 0→10M users | Ex-BigCo",'
    ' "I help teams ship 2x faster with better architecture | Staff Eng @ BigCo"],'
    '"about_score": 2, '
    '"suggested_about": "I have spent 8 years turning complex technical problems into '
    "products people love. At BigCo I led the platform team that cut deploy time from "
    '2 hours to 4 minutes...\\n\\nWhat I do best:\\n→ System design at scale\\n→ Team ",'
    '"suggestions": ["Add measurable results", "Include a CTA for inbound leads", '
    '"Mention specific technologies"]}'
)


def build_linkedin_profile_prompt(
    profile_text: str,
    *,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for LinkedIn profile analysis.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a LinkedIn profile optimisation expert. Write in {locale}. "
        "Analyse a LinkedIn profile (headline + about section) and suggest improvements. "
        "Focus on: clarity, specificity, keywords for discoverability, "
        "measurable achievements, and a compelling narrative."
        + PROFILE_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."

    user = (
        "Analyse the following LinkedIn profile text and suggest improvements.\n"
        "Return a JSON object with keys: headline_score (1-10), "
        "suggested_headlines (array of 2-3 strings), about_score (1-10), "
        "suggested_about (string — improved about section), "
        "and suggestions (array of 3-5 actionable tips).\n\n"
        f"Profile:\n{profile_text}"
    )

    return system, user
