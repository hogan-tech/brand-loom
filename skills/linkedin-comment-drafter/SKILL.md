---
name: linkedin_comment_drafter
slug: linkedin-comment-drafter
displayName: "LinkedIn Comment Drafter"
summary: "Draft thoughtful comments on target LinkedIn posts"
description: "Use when you want to draft an authentic, value-adding comment on someone else's LinkedIn post. Accepts the target post and your context to create a relevant, engaging comment. Model-agnostic (OpenAI/Anthropic/Gemini/Ollama). Part of brand-loom; hosted brand-memory version at neoxra.com."
version: "0.3.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "LinkedIn comments, engagement, networking, thought leadership replies"
argument-hint: "<target_post> [--your-context '...'] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# LinkedIn Comment Drafter

Draft a thoughtful, value-adding comment on someone else's LinkedIn post. Provide the target post and optionally your context/perspective.

## Quick start

- **CLI:**  `brand-loom run linkedin_comment_drafter --text "We just hit $1M ARR with a 3-person team."`
- **Python:**
  ```python
  from brand_loom.agent import run_skill
  from brand_loom.providers import use_provider

  use_provider("openai")
  result = run_skill("linkedin_comment_drafter", "Target post text...", your_context="I run a bootstrapped SaaS")
  print(result.text)
  ```

## Install

```bash
pip install brand-loom
npx skills add hogan-tech/brand-loom
```

## Going further

Want auto-engagement workflows and brand-matched commenting? → [neoxra.com](https://neoxra.com)
