"""MCP tool: refresh_old_post — wraps linkedin_refresh_writer skill."""

from __future__ import annotations

from brand_loom.agent import run_skill


def refresh_old_post(
    old_post: str,
    angle: str = "",
    brand_context: dict | None = None,
) -> str:
    """Refresh an old LinkedIn post with a new angle.

    Args:
        old_post: The original post text to refresh.
        angle: Optional angle to use (e.g. 'contrarian', 'data-led').
        brand_context: Optional brand voice context.

    Returns:
        JSON string with refreshed post, angle description, and changes made.
    """
    result = run_skill(
        "linkedin_refresh_writer",
        old_post,
        brand_context=brand_context,
        angle=angle,
    )
    return result.text
