"""MCP tool: extract_voice — wraps linkedin_comment_drafter skill.

Uses the comment drafter to draft comments that match a voice/context,
effectively extracting and applying voice characteristics.
"""

from __future__ import annotations

from brand_loom.agent import run_skill


def extract_voice(
    target_post: str,
    your_context: str = "",
    style: str = "value-add",
    brand_context: dict | None = None,
) -> str:
    """Draft a voice-matched comment on a LinkedIn post.

    Args:
        target_post: The LinkedIn post to comment on.
        your_context: Your perspective or background for the comment.
        style: Comment style (default 'value-add').
        brand_context: Optional brand voice context.

    Returns:
        JSON string with the drafted comment, style, and word count.
    """
    result = run_skill(
        "linkedin_comment_drafter",
        target_post,
        brand_context=brand_context,
        your_context=your_context,
        style=style,
    )
    return result.text
