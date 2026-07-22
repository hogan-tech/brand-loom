"""MCP tool: score_post — wraps linkedin_post_scorer skill."""

from __future__ import annotations

from brand_loom.agent import run_skill


def score_post(post_text: str, brand_context: dict | None = None) -> str:
    """Score a LinkedIn post on 6 metrics.

    Args:
        post_text: The LinkedIn post to evaluate.
        brand_context: Optional brand voice context.

    Returns:
        JSON string with scores (hook, skimmability, engagement, length, cta, voice_match)
        and suggestions.
    """
    result = run_skill(
        "linkedin_post_scorer",
        post_text,
        brand_context=brand_context,
    )
    return result.text
