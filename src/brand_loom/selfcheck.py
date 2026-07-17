"""Lightweight, rule-based self-check / lint for skill outputs.

This is a commodity, single-pass lint — it FLAGS issues but does NOT score,
veto, or retry. Quality scoring + gated retry is in the hosted product
at neoxra.com.
"""

from __future__ import annotations

import re

# --- Anti-slop: phrases that signal generic, low-effort LLM output ----------

SLOP_PHRASES: list[str] = [
    "in today's fast-paced world",
    "in today's digital age",
    "in today's rapidly evolving",
    "it's important to note that",
    "it is important to note that",
    "dive into",
    "dive deep",
    "delve into",
    "delve deep",
    "let's delve",
    "unlock the power",
    "unlock the potential",
    "unlock the secret",
    "game-changer for",
    "revolutionize your",
    "take your .* to the next level",
    "without further ado",
    "in this article, we will",
    "in this blog post",
    "are you ready to",
    "look no further",
    "but wait, there's more",
]

# --- Banned generic phrases (filler / empty calories) -----------------------

BANNED_GENERIC: list[str] = [
    "leverage synergies",
    "paradigm shift",
    "move the needle",
    "circle back",
    "low-hanging fruit",
    "boil the ocean",
    "thought leader",
]

# --- Leaked frontmatter / system artifact patterns --------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n", re.MULTILINE)
SYSTEM_LEAK_PATTERNS: list[str] = [
    "as an ai",
    "as a language model",
    "i'm an ai",
    "i am an ai",
    "i cannot",
    "i can't help with",
]


def lint(text: str) -> list[dict[str, str]]:
    """Run all lint checks on *text* and return a list of issues.

    Each issue is ``{"rule": "<rule-id>", "detail": "<human-readable>"}``.
    An empty list means the text is clean.
    """
    issues: list[dict[str, str]] = []
    lower = text.lower()

    # 1. Anti-slop
    for phrase in SLOP_PHRASES:
        if re.search(phrase, lower):
            issues.append({
                "rule": "anti-slop",
                "detail": f"Slop phrase detected: '{phrase}'",
            })

    # 2. Banned generic phrases
    for phrase in BANNED_GENERIC:
        if phrase in lower:
            issues.append({
                "rule": "banned-generic",
                "detail": f"Banned generic phrase: '{phrase}'",
            })

    # 3. Leaked frontmatter
    if FRONTMATTER_RE.search(text):
        issues.append({
            "rule": "leaked-frontmatter",
            "detail": "Output contains YAML frontmatter delimiters (---)",
        })

    # 4. System prompt / AI identity leaks
    for pattern in SYSTEM_LEAK_PATTERNS:
        if pattern in lower:
            issues.append({
                "rule": "system-leak",
                "detail": f"AI identity leak detected: '{pattern}'",
            })

    # 5. Length check — flag suspiciously short output (< 20 chars)
    stripped = text.strip()
    if len(stripped) < 20 and len(stripped) > 0:
        issues.append({
            "rule": "too-short",
            "detail": f"Output is only {len(stripped)} characters — may be incomplete",
        })

    return issues
