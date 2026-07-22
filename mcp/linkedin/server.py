"""LinkedIn MCP server — stdio transport.

Exposes brand-loom LinkedIn skills as MCP tools over stdin/stdout.

Usage:
    python -m mcp.linkedin.server

Requires:
    pip install "brand-loom[openai]" mcp
    export BRANDLOOM_PROVIDER=openai  # or anthropic, gemini, ollama, fake
"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from mcp.linkedin.tools.analyze_profile import analyze_profile
from mcp.linkedin.tools.draft_post import draft_post
from mcp.linkedin.tools.extract_voice import extract_voice
from mcp.linkedin.tools.refresh_old_post import refresh_old_post
from mcp.linkedin.tools.score_post import score_post
from mcp.linkedin.tools.suggest_hooks import suggest_hooks

server = FastMCP(
    "brand-loom-linkedin",
    version="0.3.0",
)


@server.tool()
def linkedin_draft_post(
    milestone: str,
    post_type: str = "text",
    brand_context: str = "",
) -> str:
    """Draft a LinkedIn post from a milestone or topic.

    Args:
        milestone: The milestone or topic to write about.
        post_type: One of 'text', 'article', 'carousel' (default 'text').
        brand_context: Optional JSON string with brand voice context.
    """
    ctx = json.loads(brand_context) if brand_context else None
    return draft_post(milestone, post_type=post_type, brand_context=ctx)


@server.tool()
def linkedin_score_post(
    post_text: str,
    brand_context: str = "",
) -> str:
    """Score a LinkedIn post on 6 metrics: hook, skimmability, engagement, length, cta, voice_match.

    Args:
        post_text: The LinkedIn post to evaluate.
        brand_context: Optional JSON string with brand voice context.
    """
    ctx = json.loads(brand_context) if brand_context else None
    return score_post(post_text, brand_context=ctx)


@server.tool()
def linkedin_analyze_profile(
    profile_text: str,
    brand_context: str = "",
) -> str:
    """Analyse a LinkedIn profile (headline + about) and suggest improvements.

    Args:
        profile_text: The profile headline and about section text.
        brand_context: Optional JSON string with brand voice context.
    """
    ctx = json.loads(brand_context) if brand_context else None
    return analyze_profile(profile_text, brand_context=ctx)


@server.tool()
def linkedin_suggest_hooks(
    topic: str,
    count: int = 5,
    brand_context: str = "",
) -> str:
    """Generate scroll-stopping hook variants for a LinkedIn topic.

    Args:
        topic: The topic to generate hooks for.
        count: Number of hook variants (default 5).
        brand_context: Optional JSON string with brand voice context.
    """
    ctx = json.loads(brand_context) if brand_context else None
    return suggest_hooks(topic, count=count, brand_context=ctx)


@server.tool()
def linkedin_extract_voice(
    target_post: str,
    your_context: str = "",
    style: str = "value-add",
    brand_context: str = "",
) -> str:
    """Draft a voice-matched comment on a LinkedIn post.

    Args:
        target_post: The LinkedIn post to comment on.
        your_context: Your perspective or background for the comment.
        style: Comment style (default 'value-add').
        brand_context: Optional JSON string with brand voice context.
    """
    ctx = json.loads(brand_context) if brand_context else None
    return extract_voice(target_post, your_context=your_context, style=style, brand_context=ctx)


@server.tool()
def linkedin_refresh_old_post(
    old_post: str,
    angle: str = "",
    brand_context: str = "",
) -> str:
    """Refresh an old LinkedIn post with a new angle.

    Args:
        old_post: The original post text to refresh.
        angle: Optional angle (e.g. 'contrarian', 'data-led', 'story').
        brand_context: Optional JSON string with brand voice context.
    """
    ctx = json.loads(brand_context) if brand_context else None
    return refresh_old_post(old_post, angle=angle, brand_context=ctx)


if __name__ == "__main__":
    server.run(transport="stdio")
