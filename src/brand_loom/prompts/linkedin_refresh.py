"""Prompt builder for the LinkedIn refresh writer skill."""

from __future__ import annotations

REFRESH_FEW_SHOT = (
    "\n\nHere is an example:\n"
    "Old post: \"5 tips for better remote meetings: 1. Have an agenda...\"\n\n"
    '{"refreshed_post": "I have sat through 1,000+ remote meetings.\\n\\n'
    "Most are terrible. Here is why:\\n\\n"
    "The problem is not the tool. It is the culture.\\n\\n"
    "3 things that actually fixed our meetings:\\n\\n"
    "1. No meeting without a written pre-read\\n"
    "2. 25-minute default (not 30)\\n"
    '3. The quietest person speaks first\\n\\n'
    "Which would you try first?\", "
    '"angle": "contrarian reframe", "changes": ['
    '"Shifted from generic tips to personal experience",'
    ' "Added specific data point (1,000+ meetings)",'
    ' "Contrarian framing — blame culture, not tools",'
    ' "Interactive CTA at the end"]}'
)


def build_linkedin_refresh_prompt(
    old_post: str,
    *,
    angle: str = "",
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for LinkedIn post refreshing.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a LinkedIn content strategist. Write in {locale}. "
        "Given an old or underperforming LinkedIn post, generate a fresh version "
        "with a new angle. Improve the hook, structure, and engagement potential. "
        "Keep the core message but reframe it to feel new and compelling."
        + REFRESH_FEW_SHOT
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

    angle_line = ""
    if angle:
        angle_line = f"\nRequested angle: {angle}"

    user = (
        f"Refresh the following LinkedIn post with a new angle.{angle_line}\n"
        "Return a JSON object with keys: refreshed_post (string — the full new post), "
        "angle (string — describe the new angle), "
        "and changes (array of strings — what you changed and why).\n\n"
        f"Old post:\n{old_post}"
    )

    return system, user
