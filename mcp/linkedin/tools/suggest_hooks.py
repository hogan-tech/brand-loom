"""MCP tool: suggest_hooks — wraps linkedin_hook_generator skill."""

from __future__ import annotations

from brand_loom.agent import run_skill


def suggest_hooks(topic: str, count: int = 5, brand_context: dict | None = None) -> str:
    """Generate LinkedIn hook variants for a topic.

    Args:
        topic: The topic to generate hooks for.
        count: Number of hook variants (default 5).
        brand_context: Optional brand voice context.

    Returns:
        JSON string with hook variants.
    """
    result = run_skill(
        "linkedin_hook_generator",
        topic,
        brand_context=brand_context,
        count=count,
    )
    return result.text
