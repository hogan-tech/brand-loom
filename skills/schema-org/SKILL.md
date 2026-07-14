---
name: schema-org
slug: schema-org
displayName: "Schema.org Markup Generator"
summary: "FAQPage / Article / Breadcrumb JSON-LD (no LLM needed)"
description: "Use when you need Schema.org JSON-LD structured data. Pure Python — no LLM call required. Supports FAQPage, Article, Breadcrumb. Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "schema.org markup, JSON-LD, structured data, SEO rich snippets"
argument-hint: "<faqs_json> [--schema-type faq]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# Schema.org Markup Generator

Use when you need Schema.org JSON-LD structured data. Pure Python — no LLM call required. Supports FAQPage, Article, Breadcrumb.

## Quick start

- **CLI:**  `brand-loom run schema_org --text '[{"q":"What is X?","a":"X is..."}]'`
- **Chain:** `brand-loom chain faq,schema_org --text "Our product helps teams..."`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("schema_org", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
