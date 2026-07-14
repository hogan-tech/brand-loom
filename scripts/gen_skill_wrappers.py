#!/usr/bin/env python3
"""Generate agent-skill wrappers (SKILL.md + manifests) from canonical Python skills.

Usage:
    python scripts/gen_skill_wrappers.py           # generate all wrappers
    python scripts/gen_skill_wrappers.py --check    # fail if wrappers are stale (CI mode)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Resolve project root
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# Ensure src is importable
sys.path.insert(0, str(SRC))

# ── Skill metadata ──────────────────────────────────────────────────────
# Single source of truth: derived from the canonical Python skill classes.
# Each entry maps a slug to the metadata needed for SKILL.md generation.

SKILL_META: dict[str, dict] = {
    "hook": {
        "display_name": "Hook / Headline Generator",
        "summary": "Marketing hooks and headlines, on any model",
        "description": (
            "Use when you need scroll-stopping hooks or headlines for a topic. "
            "Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "hooks, headlines, opening lines, scroll-stoppers for social or SEO",
        "argument_hint": "<topic> [--brand brand.json]",
        "cli_example": 'brand-loom run hook --text "How we cut cloud costs 40%"',
        "chain_example": 'brand-loom chain hook,caption --text "How we cut cloud costs 40%" --brand brand.json',
    },
    "caption": {
        "display_name": "Caption Writer",
        "summary": "Platform captions from a topic with brand voice",
        "description": (
            "Use when you need a social media caption for any platform. "
            "Supports brand_context for voice/tone. Model-agnostic. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "social media captions, post copy, platform-specific text",
        "argument_hint": "<topic> [--platform twitter] [--brand brand.json]",
        "cli_example": 'brand-loom run caption --text "AI marketing trends" --platform twitter',
        "chain_example": 'brand-loom chain hook,caption --text "AI marketing trends" --brand brand.json',
    },
    "hashtags": {
        "display_name": "Hashtag Generator",
        "summary": "Relevant, deduped hashtag sets for any topic",
        "description": (
            "Use when you need hashtags for social media posts. "
            "Generates deduped, count-bounded sets. Model-agnostic. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "hashtags, tags, social discovery keywords",
        "argument_hint": "<topic> [--count 15] [--brand brand.json]",
        "cli_example": 'brand-loom run hashtags --text "sustainable fashion"',
        "chain_example": 'brand-loom chain caption,hashtags --text "sustainable fashion"',
    },
    "repurpose": {
        "display_name": "Content Repurposer",
        "summary": "Repurpose content across formats (short, thread, carousel)",
        "description": (
            "Use when you need to transform content from one format to another — "
            "long to short, article to thread, article to carousel. Model-agnostic. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "content repurposing, format conversion, cross-platform adaptation",
        "argument_hint": "<source_text> [--target-format thread] [--brand brand.json]",
        "cli_example": 'brand-loom run repurpose --text "Long article..." --target-format thread',
        "chain_example": 'brand-loom chain repurpose,hashtags --text "Long article..."',
    },
    "seo-outline": {
        "display_name": "SEO Article Outline",
        "summary": "Structured SEO article outlines with section planning",
        "description": (
            "Use when you need an SEO-optimized article outline with 4-8 sections. "
            "Locale-parametric. Model-agnostic. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "SEO outlines, article planning, content structure, blog post skeletons",
        "argument_hint": "<topic> [--locale en] [--brand brand.json]",
        "cli_example": 'brand-loom run seo_outline --text "best CRM for startups"',
        "chain_example": 'brand-loom chain seo_outline,faq --text "best CRM for startups"',
    },
    "faq": {
        "display_name": "FAQ Generator",
        "summary": "Generate FAQ question-answer pairs from any content",
        "description": (
            "Use when you need FAQ items from a body of text. "
            "Generates 3-6 Q&A pairs. Model-agnostic. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "FAQs, Q&A sections, knowledge base entries, help content",
        "argument_hint": "<body_text> [--count 5] [--brand brand.json]",
        "cli_example": 'brand-loom run faq --text "Our product helps teams..."',
        "chain_example": 'brand-loom chain faq,schema_org --text "Our product helps teams..."',
    },
    "schema-org": {
        "display_name": "Schema.org Markup Generator",
        "summary": "FAQPage / Article / Breadcrumb JSON-LD (no LLM needed)",
        "description": (
            "Use when you need Schema.org JSON-LD structured data. "
            "Pure Python — no LLM call required. Supports FAQPage, Article, Breadcrumb. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "schema.org markup, JSON-LD, structured data, SEO rich snippets",
        "argument_hint": '<faqs_json> [--schema-type faq]',
        "cli_example": 'brand-loom run schema_org --text \'[{"q":"What is X?","a":"X is..."}]\'',
        "chain_example": 'brand-loom chain faq,schema_org --text "Our product helps teams..."',
    },
    "cta": {
        "display_name": "CTA Writer",
        "summary": "Call-to-action variants for any goal",
        "description": (
            "Use when you need call-to-action copy for buttons, banners, or closing lines. "
            "Generates multiple CTA variants. Model-agnostic. "
            "Part of brand-loom; hosted brand-memory version at neoxra.com."
        ),
        "when_to_use": "CTAs, buttons, conversion copy, action prompts, closing lines",
        "argument_hint": "<goal> [--count 5] [--brand brand.json]",
        "cli_example": 'brand-loom run cta --text "Sign up for our newsletter"',
        "chain_example": 'brand-loom chain hook,cta --text "Free trial for AI marketing"',
    },
}

VERSION = "0.1.0"
HOMEPAGE = "https://github.com/hogan-tech/brand-loom"
AUTHOR = "hogan-tech"


def _build_skill_md(slug: str, meta: dict) -> str:
    """Generate a SKILL.md for one skill."""
    # The CLI skill name uses underscores (e.g. seo_outline, schema_org)
    cli_name = slug.replace("-", "_")

    return f"""---
name: {slug}
slug: {slug}
displayName: "{meta['display_name']}"
summary: "{meta['summary']}"
description: "{meta['description']}"
version: "{VERSION}"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, and any agent-skill host; or standalone via `pip install brand-loom`"
homepage: "{HOMEPAGE}"
when_to_use: "{meta['when_to_use']}"
argument-hint: "{meta['argument_hint']}"
metadata: {{"author": "{AUTHOR}", "discipline": "marketing", "hosted": "https://neoxra.com"}}
---

# {meta['display_name']}

{meta['description'].split('. Part of')[0]}.

## Quick start

- **CLI:**  `{meta['cli_example']}`
- **Chain:** `{meta['chain_example']}`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("{cli_name}", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
"""


def _build_skills_sh_json() -> str:
    """Generate the skills.sh registry manifest."""
    data = {
        "$schema": "https://skills.sh/schemas/skills.sh.schema.json",
        "groupings": [
            {
                "title": "brand-loom — model-agnostic marketing skills",
                "description": (
                    "Runs on any LLM (OpenAI/Anthropic/Gemini/Ollama), BYOK, "
                    "no coding agent required. "
                    "Hosted brand-memory engine at neoxra.com."
                ),
                "skills": list(SKILL_META.keys()),
            }
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _build_marketplace_json() -> str:
    """Generate the Claude Code plugin marketplace manifest."""
    skills = []
    for slug, meta in SKILL_META.items():
        skills.append({
            "name": slug,
            "displayName": meta["display_name"],
            "description": meta["summary"],
            "version": VERSION,
            "license": "Apache-2.0",
            "author": AUTHOR,
            "homepage": HOMEPAGE,
            "when_to_use": meta["when_to_use"],
        })
    data = {
        "name": "brand-loom",
        "displayName": "brand-loom — model-agnostic marketing skills",
        "description": (
            "Open-source marketing skills that run on any model. "
            "Hooks, captions, hashtags, repurposing, SEO outlines, FAQs, "
            "schema.org markup, CTAs. BYOK. "
            "Hosted brand-memory engine at neoxra.com."
        ),
        "version": VERSION,
        "license": "Apache-2.0",
        "author": AUTHOR,
        "homepage": HOMEPAGE,
        "skills": skills,
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def generate(root: Path) -> dict[Path, str]:
    """Generate all wrapper files. Returns {path: content}."""
    files: dict[Path, str] = {}

    # SKILL.md for each skill
    for slug, meta in SKILL_META.items():
        path = root / "skills" / slug / "SKILL.md"
        files[path] = _build_skill_md(slug, meta)

    # Manifests at repo root
    files[root / "skills.sh.json"] = _build_skills_sh_json()
    files[root / "marketplace.json"] = _build_marketplace_json()

    return files


def write_all(files: dict[Path, str]) -> None:
    """Write generated files to disk."""
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path.relative_to(ROOT)}")


def check_all(files: dict[Path, str]) -> bool:
    """Check that all generated files match expected content. Returns True if fresh."""
    stale: list[str] = []
    for path, expected in files.items():
        if not path.exists():
            stale.append(f"  MISSING: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            stale.append(f"  STALE:   {path.relative_to(ROOT)}")

    if stale:
        print("ERROR: Generated agent-skill wrappers are out of date.")
        print("Run `python scripts/gen_skill_wrappers.py` to regenerate.\n")
        for line in stale:
            print(line)
        return False

    print("OK: All agent-skill wrappers are up to date.")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate agent-skill SKILL.md wrappers + manifests from canonical Python skills.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that wrappers are up to date (CI mode). Exits non-zero if stale.",
    )
    args = parser.parse_args()

    files = generate(ROOT)

    if args.check:
        if not check_all(files):
            sys.exit(1)
    else:
        print(f"Generating {len(files)} agent-skill wrapper files...")
        write_all(files)
        print(f"\nDone. {len(files)} files written.")


if __name__ == "__main__":
    main()
