---
name: linkedin_profile_analyzer
slug: linkedin-profile-analyzer
displayName: "LinkedIn Profile Analyzer"
summary: "Parse profile text, suggest headline + about improvements"
description: "Use when you want to improve a LinkedIn profile. Analyses headline and about section, scores each, and suggests concrete improvements for discoverability and engagement. Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.3.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "LinkedIn profile optimisation, headline improvement, about section rewrite, personal branding"
argument-hint: "<profile_text> [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# LinkedIn Profile Analyzer

Analyse a LinkedIn profile (headline + about section) and get scored suggestions for improvement — better headlines, a rewritten about section, and actionable tips.

## Quick start

- **CLI:**  `brand-loom run linkedin_profile_analyzer --text "Headline: Software Engineer..."`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")
  result = run_skill("linkedin_profile_analyzer", "Headline: Software Engineer at BigCo\nAbout: I write code.")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom
npx skills add hogan-tech/brand-loom
```

## Going further

Want automatic voice extraction and multi-platform profile optimisation? → [neoxra.com](https://neoxra.com)
