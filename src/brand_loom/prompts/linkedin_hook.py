"""Prompt builder for the LinkedIn hook generator skill."""

from __future__ import annotations

LINKEDIN_HOOK_FEW_SHOT = (
    "\n\nHere are examples of strong LinkedIn hooks:\n"
    "Topic: career change\n"
    '["I quit my $200k job with no backup plan. Here is what happened.",'
    ' "Nobody talks about the first 90 days after a career pivot.",'
    ' "The best career advice I got was from someone who got fired.",'
    ' "I interviewed at 12 companies in 3 weeks. Only 1 asked the right question.",'
    ' "Your dream job does not exist. Build it."]\n\n'
    "Topic: startup lessons\n"
    '["We almost ran out of money 3 times. Each time taught us something different.",'
    ' "The worst business advice I ever followed (and what I do now instead).",'
    ' "Our biggest competitor is not who you think.",'
    ' "I spent $50k on marketing before I found what actually works.",'
    ' "Stop building features. Start solving problems."]'
)


def build_linkedin_hook_prompt(
    topic: str,
    *,
    count: int = 5,
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for LinkedIn hook generation.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a LinkedIn content strategist. Write in {locale}. "
        "Generate scroll-stopping opening hooks optimised for the LinkedIn feed. "
        "Each hook should be 1-2 sentences max, create curiosity or tension, "
        "and make readers stop scrolling. Vary the hook style across the set "
        "(question, bold claim, story opener, data-led, contrarian)."
        + LINKEDIN_HOOK_FEW_SHOT
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
        f"Generate exactly {count} LinkedIn hook variants for the following topic.\n"
        f"Return them as a JSON array of strings.\n\n"
        f"Topic: {topic}"
    )

    return system, user
