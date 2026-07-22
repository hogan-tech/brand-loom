---
name: linkedin_refresh_writer
slug: linkedin-refresh-writer
displayName: "LinkedIn Refresh Writer"
summary: "Generate a fresh angle for an old LinkedIn post"
description: "Use when you want to breathe new life into an old or underperforming LinkedIn post. Generates a refreshed version with a new angle, improved hook, and better structure. Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.3.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "LinkedIn content refresh, post rewrite, content recycling, evergreen updates"
argument-hint: "<old_post> [--angle 'contrarian'] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# LinkedIn Refresh Writer

Given an old or underperforming LinkedIn post, generate a refreshed version with a new angle, improved hook, and better engagement structure.

## Quick start

- **CLI:**  `brand-loom run linkedin_refresh_writer --text "5 tips for better remote meetings..."`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")
  result = run_skill("linkedin_refresh_writer", "Your old post text...", angle="contrarian")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom
npx skills add hogan-tech/brand-loom
```

## Going further

Want automated content recycling with performance tracking? → [neoxra.com](https://neoxra.com)
