"""Prompt builder for the LinkedIn post scorer skill."""

from __future__ import annotations

METRICS = ["hook", "skimmability", "engagement", "length", "cta", "voice_match"]

SCORER_FEW_SHOT = (
    "\n\nHere is an example scored post:\n"
    "Post: \"I quit my job last month.\\n\\n"
    "Not because I hated it.\\n"
    "Because I loved something else more.\\n\\n"
    "3 lessons from month one of self-employment:\\n\\n"
    "1. Nobody cares about your title anymore\\n"
    "2. Revenue fixes impostor syndrome\\n"
    "3. Loneliness is real — build your crew early\\n\\n"
    "What would you do with full freedom?\"\n\n"
    '{"hook": 8, "skimmability": 9, "engagement": 8, '
    '"length": 7, "cta": 7, "voice_match": 6, '
    '"overall": 7.5, "suggestions": ['
    '"Add a more specific data point in the hook", '
    '"CTA could be more targeted — ask a specific audience"]}'
)


def build_linkedin_post_scorer_prompt(
    post_text: str,
    *,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for LinkedIn post scoring.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a LinkedIn content analyst. Write in {locale}. "
        "Score a LinkedIn post on 6 metrics, each 1-10:\n"
        "- hook: Does the opening line stop the scroll?\n"
        "- skimmability: Short paragraphs, line breaks, easy to scan?\n"
        "- engagement: Does it invite comments, shares, or saves?\n"
        "- length: Appropriate length (not too short, not too long)?\n"
        "- cta: Clear call-to-action or closing question?\n"
        "- voice_match: Authentic, human tone (not corporate jargon)?\n\n"
        "Also provide an overall score (average) and 2-3 actionable suggestions."
        + SCORER_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Expected tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."

    user = (
        "Score the following LinkedIn post on all 6 metrics.\n"
        "Return a JSON object with keys: hook, skimmability, engagement, "
        "length, cta, voice_match (each 1-10), overall (float), "
        "and suggestions (array of strings).\n\n"
        f"Post:\n{post_text}"
    )

    return system, user
