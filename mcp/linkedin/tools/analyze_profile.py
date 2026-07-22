"""MCP tool: analyze_profile — wraps linkedin_profile_analyzer skill."""

from __future__ import annotations

from brand_loom.agent import run_skill


def analyze_profile(profile_text: str, brand_context: dict | None = None) -> str:
    """Analyse a LinkedIn profile and suggest improvements.

    Args:
        profile_text: The profile headline + about section text.
        brand_context: Optional brand voice context.

    Returns:
        JSON string with scores, suggested headlines, improved about, and tips.
    """
    result = run_skill(
        "linkedin_profile_analyzer",
        profile_text,
        brand_context=brand_context,
    )
    return result.text
