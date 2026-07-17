"""brand_context schema — the seam between open skills and hosted Neoxra.

Skills accept an optional `brand_context` dict. The OSS ships an empty/basic
default. Hosted Neoxra passes a rich, auto-extracted voice profile through the
same interface for dramatically better output.
"""

from __future__ import annotations

EMPTY_BRAND_CONTEXT: dict = {
    "tone": [],
    "audience": "",
    "do_phrases": [],
    "avoid_phrases": [],
}

SAMPLE_BRAND_CONTEXT: dict = {
    "tone": ["bold", "witty", "conversational"],
    "audience": "startup founders and indie hackers",
    "do_phrases": ["game-changer", "no-brainer", "let's be real"],
    "avoid_phrases": ["synergy", "leverage", "circle back"],
}

RICH_BRAND_CONTEXT: dict = {
    "tone": [
        "confident but not arrogant",
        "data-driven",
        "slightly irreverent",
        "direct — no filler",
    ],
    "audience": (
        "B2B SaaS founders (seed to Series B), technical co-founders, "
        "and growth-stage marketing leads who've outgrown Mailchimp"
    ),
    "do_phrases": [
        "ship it",
        "here's what the data says",
        "real talk",
        "we tested this",
        "no fluff",
        "built for builders",
    ],
    "avoid_phrases": [
        "synergy",
        "leverage",
        "circle back",
        "thought leader",
        "paradigm shift",
        "in today's fast-paced world",
        "delve",
        "unlock the power",
    ],
}
