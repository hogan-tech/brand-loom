---
name: seo-outline
slug: seo-outline
displayName: "SEO Article Outline"
summary: "Structured SEO article outlines with section planning"
description: "Use when you need an SEO-optimized article outline with 4-8 sections. Locale-parametric. Model-agnostic. Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.1.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "SEO outlines, article planning, content structure, blog post skeletons"
argument-hint: "<topic> [--locale en] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# SEO Article Outline

Use when you need an SEO-optimized article outline with 4-8 sections. Locale-parametric. Model-agnostic.

## Quick start

- **CLI:**  `brand-loom run seo_outline --text "best CRM for startups"`
- **Chain:** `brand-loom chain seo_outline,faq --text "best CRM for startups"`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")  # or "anthropic", "gemini", "ollama", "fake"
  result = run_skill("seo_outline", "your topic here")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom            # standalone (no coding agent needed)
npx skills add hogan-tech/brand-loom  # via skills.sh
```

## Going further

Want hooks auto-matched to your brand voice, across every platform, no setup? → [neoxra.com](https://neoxra.com)
