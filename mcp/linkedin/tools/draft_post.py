"""MCP tool: draft_post — wraps linkedin_post skill."""

from __future__ import annotations

from brand_loom.agent import run_skill


def draft_post(
    milestone: str,
    post_type: str = "text",
    brand_context: dict | None = None,
) -> str:
    """Draft a LinkedIn post from a milestone or topic.

    Args:
        milestone: The milestone or topic to write about.
        post_type: One of 'text', 'article', 'carousel'.
        brand_context: Optional brand voice context.

    Returns:
        JSON string with the drafted post.
    """
    result = run_skill(
        "linkedin_post",
        milestone,
        brand_context=brand_context,
        post_type=post_type,
    )
    return result.text
