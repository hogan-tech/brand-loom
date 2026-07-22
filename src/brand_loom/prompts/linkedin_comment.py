"""Prompt builder for the LinkedIn comment drafter skill."""

from __future__ import annotations

COMMENT_FEW_SHOT = (
    "\n\nHere is an example:\n"
    "Target post: \"We just hit $1M ARR with a 3-person team.\"\n"
    "Your context: \"I run a bootstrapped SaaS with 5 people.\"\n\n"
    '{"comment": "This is inspiring. We are at $600k ARR with 5 people '
    "and the hardest part has been saying no to features that don't move "
    "the needle.\\n\\nCurious — what was your biggest 'no' that unlocked growth?\", "
    '"style": "value-add", "word_count": 42}'
)


def build_linkedin_comment_prompt(
    target_post: str,
    *,
    your_context: str = "",
    style: str = "value-add",
    locale: str = "en",
    brand_context: dict | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for LinkedIn comment drafting.

    Returns (system_prompt, user_prompt).
    """
    system = (
        f"You are a LinkedIn engagement strategist. Write in {locale}. "
        "Draft a thoughtful, authentic comment on someone else's LinkedIn post. "
        "The comment should add value (not just 'Great post!'), show genuine "
        "engagement with the content, and optionally share a relevant personal "
        "perspective. Keep it concise (30-80 words)."
        + COMMENT_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Your audience: {audience}."

    context_line = ""
    if your_context:
        context_line = f"\nYour context/perspective: {your_context}"

    user = (
        f"Draft a {style} comment on the following LinkedIn post.{context_line}\n"
        "Return a JSON object with keys: comment (string), "
        "style (string), and word_count (int).\n\n"
        f"Target post:\n{target_post}"
    )

    return system, user
