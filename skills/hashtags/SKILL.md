---
name: hashtags
slug: hashtags
displayName: "Hashtag Generator"
summary: "Relevant, deduped hashtag sets for any topic"
description: "Use when you need hashtags for social media posts. Generates deduped, count-bounded sets. Model-agnostic. Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "hashtags, tags, social discovery keywords"
argument-hint: "<topic> [--count 15] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# Hashtag Generator

Use when you need hashtags for social media posts. Generates deduped, count-bounded sets. Model-agnostic.

## Quick start

- **CLI:**  `brand-loom run hashtags --text "sustainable fashion"`
- **Chain:** `brand-loom chain caption,hashtags --text "sustainable fashion"`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("hashtags", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
