---
name: hook
slug: hook
displayName: "Hook / Headline Generator"
summary: "Marketing hooks and headlines, on any model"
description: "Use when you need scroll-stopping hooks or headlines for a topic. Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, and any agent-skill host; or standalone via `pip install brand-loom`"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "hooks, headlines, opening lines, scroll-stoppers for social or SEO"
argument-hint: "<topic> [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# Hook / Headline Generator

Use when you need scroll-stopping hooks or headlines for a topic. Model-agnostic (OpenAI/Anthropic/Gemini/Ollama).

## Quick start

- **CLI:**  `brand-loom run hook --text "How we cut cloud costs 40%"`
- **Chain:** `brand-loom chain hook,caption --text "How we cut cloud costs 40%" --brand brand.json`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("hook", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
