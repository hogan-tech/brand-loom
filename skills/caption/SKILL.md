---
name: caption
slug: caption
displayName: "Caption Writer"
summary: "Platform captions from a topic with brand voice"
description: "Use when you need a social media caption for any platform. Supports brand_context for voice/tone. Model-agnostic. Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, and any agent-skill host; or standalone via `pip install brand-loom`"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "social media captions, post copy, platform-specific text"
argument-hint: "<topic> [--platform twitter] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# Caption Writer

Use when you need a social media caption for any platform. Supports brand_context for voice/tone. Model-agnostic.

## Quick start

- **CLI:**  `brand-loom run caption --text "AI marketing trends" --platform twitter`
- **Chain:** `brand-loom chain hook,caption --text "AI marketing trends" --brand brand.json`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("caption", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
