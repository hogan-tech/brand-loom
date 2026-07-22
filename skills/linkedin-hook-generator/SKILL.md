---
name: linkedin_hook_generator
slug: linkedin-hook-generator
displayName: "LinkedIn Hook Generator"
summary: "5 scroll-stopping hook variants for a LinkedIn topic"
description: "Use when you need attention-grabbing opening lines for LinkedIn posts. Generates 5 varied hook styles (question, bold claim, story opener, data-led, contrarian). Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.3.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "LinkedIn hooks, opening lines, scroll-stoppers, post openers"
argument-hint: "<topic> [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# LinkedIn Hook Generator

Generate 5 scroll-stopping hook variants for any LinkedIn topic. Each hook uses a different style — question, bold claim, story opener, data-led, or contrarian.

## Quick start

- **CLI:**  `brand-loom run linkedin_hook_generator --text "How we scaled to 1M users"`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("linkedin_hook_generator", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
