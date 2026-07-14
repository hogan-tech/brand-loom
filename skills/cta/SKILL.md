---
name: cta
slug: cta
displayName: "CTA Writer"
summary: "Call-to-action variants for any goal"
description: "Use when you need call-to-action copy for buttons, banners, or closing lines. Generates multiple CTA variants. Model-agnostic. Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "CTAs, buttons, conversion copy, action prompts, closing lines"
argument-hint: "<goal> [--count 5] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# CTA Writer

Use when you need call-to-action copy for buttons, banners, or closing lines. Generates multiple CTA variants. Model-agnostic.

## Quick start

- **CLI:**  `brand-loom run cta --text "Sign up for our newsletter"`
- **Chain:** `brand-loom chain hook,cta --text "Free trial for AI marketing"`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("cta", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
