# brand-loom

**Open-source marketing skills that run on any model — with a hosted brand-memory engine. No coding agent required.**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/brand-loom.svg)](https://pypi.org/project/brand-loom/)
[![CI](https://github.com/hogan-tech/brand-loom/actions/workflows/ci.yml/badge.svg)](https://github.com/hogan-tech/brand-loom/actions/workflows/ci.yml)

`brand-loom` is a small library of **commodity marketing skills** — hooks, captions, hashtags, content
repurposing, SEO outlines, FAQs, schema.org markup, CTAs — that run on **any LLM** (OpenAI, Anthropic, Gemini,
or a local model via Ollama). Bring your own key. No coding agent, no vendor lock-in.

> Want it *on-brand* and *multi-platform* automatically — without writing prompts? That's the hosted engine at
> **[neoxra.com](https://neoxra.com)** (auto voice extraction, multi-platform orchestration, Brand Kit). `brand-loom`
> is the open core; Neoxra hosts the rest.

## Why brand-loom

- **Model-agnostic.** One interface, four providers, BYOK. Swap models with one env var.
- **No coding agent required.** Plain Python — not coupled to Claude Code / Cursor / OpenClaw.
- **Brand-aware seam.** Every skill accepts an optional `brand_context`. Ship a basic default here; get automatic,
  extracted brand voice on hosted Neoxra.

## Quickstart (60 seconds, no API key)

```bash
pip install brand-loom
```

```python
from brand_loom.providers import use_provider
from brand_loom.skills.hook import HookSkill

use_provider("fake")              # runs with zero keys; swap for "openai"/"anthropic"/"gemini"/"ollama"
skill = HookSkill()
print(skill.run_topic("How we cut cloud costs 40%"))
```

Real provider (BYOK):

```bash
pip install "brand-loom[openai]"
export OPENAI_API_KEY=sk-...
export BRANDLOOM_PROVIDER=openai
```

Run it as an agent (no coding agent required):

```bash
brand-loom run hook --text "How we cut cloud costs 40%"
brand-loom chain hook,caption --text "How we cut cloud costs 40%" --brand brand.json
```

A thin, linear runner — one skill or a simple chain, on any model. Sophisticated multi-platform orchestration
(voice-matched, Planner→Critic, auto fan-out) lives in hosted **[Neoxra](https://neoxra.com)**.

Agent chain (Python API):

```python
from brand_loom.agent import run_chain, run_skill
from brand_loom.providers import use_provider

use_provider("fake")  # or "openai", "anthropic", "gemini", "ollama"

# Single skill
result = run_skill("hook", "How we cut cloud costs 40%")
print(result.text)

# Chain: hook → caption
result = run_chain(["hook", "caption"], "How we cut cloud costs 40%")
print(result.text)

# With brand context
result = run_skill("hook", "AI marketing", brand_context={
    "tone": ["bold", "witty"],
    "audience": "startup founders",
})
print(result.text)
```

## Skills (v0.1)

| Skill | What it does |
|---|---|
| `hook` | Headline / hook options for a topic |
| `caption` | Platform caption from a topic + `brand_context` |
| `hashtags` | Relevant, deduped hashtag set |
| `repurpose` | long→short, article→thread, article→carousel copy |
| `seo_outline` | 4–8 section SEO article outline (locale-parametric) |
| `faq` | 3–6 Q&A pairs from a body of text |
| `schema_org` | FAQPage / Article / Breadcrumb JSON-LD (no LLM) |
| `cta` | Call-to-action variants for a goal |

## Providers

| Provider | Extra | Env |
|---|---|---|
| OpenAI | `brand-loom[openai]` | `OPENAI_API_KEY` |
| Anthropic | `brand-loom[anthropic]` | `ANTHROPIC_API_KEY` |
| Gemini | `brand-loom[gemini]` | `GEMINI_API_KEY` |
| Ollama (local) | built-in (HTTP) | `OLLAMA_HOST` |
| Fake (tests/demo) | built-in | — |

## The brand_context seam

Skills accept an optional `brand_context` dict (`tone`, `audience`, `do_phrases`, `avoid_phrases`). `brand-loom`
ships an empty/basic default. Automatic voice extraction from your existing content, multi-platform fan-out, and a
no-code UI live in hosted **[Neoxra](https://neoxra.com)** — see [HOSTED.md](HOSTED.md).

## Contributing

PRs welcome — read [CONTRIBUTING.md](CONTRIBUTING.md), [SCOPE.md](SCOPE.md), and sign the
[CLA](CLA.md). In scope: single-shot commodity skills. Out of scope: voice engine, orchestration, tuned scorers,
analytics/publish integrations (these live in the hosted product).

## License

[Apache-2.0](LICENSE). Hosted by [Neoxra](https://neoxra.com) · a Meridian Global product.
