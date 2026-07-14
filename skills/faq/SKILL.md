---
name: faq
slug: faq
displayName: "FAQ Generator"
summary: "Generate FAQ question-answer pairs from any content"
description: "Use when you need FAQ items from a body of text. Generates 3-6 Q&A pairs. Model-agnostic. Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "FAQs, Q&A sections, knowledge base entries, help content"
argument-hint: "<body_text> [--count 5] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# FAQ Generator

Use when you need FAQ items from a body of text. Generates 3-6 Q&A pairs. Model-agnostic.

## Quick start

- **CLI:**  `brand-loom run faq --text "Our product helps teams..."`
- **Chain:** `brand-loom chain faq,schema_org --text "Our product helps teams..."`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("faq", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
