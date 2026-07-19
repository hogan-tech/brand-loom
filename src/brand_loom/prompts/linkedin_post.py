"""Prompt builder for the LinkedIn post generator skill."""

from __future__ import annotations

POST_TYPES = {"text", "article", "carousel"}

LINKEDIN_FEW_SHOT = (
    "\n\nHere are examples of strong LinkedIn posts:\n"
    "Milestone: raised Series A\n"
    '{"post": "We just closed our Series A.\\n\\n'
    "But here is what nobody tells you about fundraising:\\n\\n"
    "→ 47 investor meetings\\n"
    "→ 31 rejections\\n"
    "→ 4 months of zero revenue focus\\n\\n"
    "The pitch that finally worked was not about TAM.\\n"
    "It was about the 3 customers who refused to churn.\\n\\n"
    "DM me if you are fundraising. Happy to share the deck.\", "
    '"post_type": "text"}\n\n'
    "Milestone: hit 10k users\n"
    '{"post": "10,000 users. Zero paid ads.\\n\\n'
    "The playbook:\\n\\n"
    "1. Built in public (every mistake, every win)\\n"
    "2. Replied to every single comment for 6 months\\n"
    "3. Turned our best support tickets into blog posts\\n\\n"
    "The growth hack nobody talks about? Actually caring.\\n\\n"
    "What has worked for you?\", \"post_type\": \"text\"}"
)


def build_linkedin_post_prompt(
    milestone: str,
    *,
    post_type: str = "text",
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for LinkedIn post generation."""
    if post_type not in POST_TYPES:
        post_type = "text"

    system = (
        f"You are a LinkedIn content strategist. Write in {locale}. "
        "Create authentic, engaging LinkedIn posts that drive meaningful engagement. "
        "Use short paragraphs, line breaks for readability, and end with a hook or CTA. "
        "Avoid corporate jargon. Be human, specific, and story-driven."
        + LINKEDIN_FEW_SHOT
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
        f"Write a LinkedIn {post_type} post about the following milestone or topic.\n"
        f"Return a JSON object with keys: \"post\" (the full post text) "
        f"and \"post_type\" (\"{post_type}\").\n\n"
        f"Milestone/topic: {milestone}"
    )

    return system, user
