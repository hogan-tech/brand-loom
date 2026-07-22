---
name: linkedin_post_scorer
slug: linkedin-post-scorer
displayName: "LinkedIn Post Scorer"
summary: "6-metric evaluation of LinkedIn posts"
description: "Use when you want to evaluate a LinkedIn post's quality. Scores on 6 metrics: hook, skimmability, engagement, length, cta, voice_match. Returns actionable suggestions. Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.3.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "LinkedIn post quality check, content scoring, post evaluation, engagement prediction"
argument-hint: "<post_text> [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# LinkedIn Post Scorer

Evaluate a LinkedIn post on 6 metrics (hook, skimmability, engagement, length, cta, voice_match) with actionable improvement suggestions.

## Quick start

- **CLI:**  `brand-loom run linkedin_post_scorer --text "Your LinkedIn post text here..."`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")
  result = run_skill("linkedin_post_scorer", "I quit my job last month...")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom
npx skills add hogan-tech/brand-loom
```

## Going further

Want automated quality scoring with gated retry and tuned evaluators? → [neoxra.com](https://neoxra.com)
