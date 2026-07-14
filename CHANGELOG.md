# Changelog

## 0.1.0 (2026-07-13)

Initial release.

### Skills
- **hook** — headline / hook options for a topic
- **caption** — platform caption from a topic + `brand_context`
- **hashtags** — relevant, deduped hashtag set
- **repurpose** — long→short, article→thread, article→carousel copy, summary, email
- **seo_outline** — 4-8 section SEO article outline (locale-parametric)
- **faq** — 3-6 Q&A pairs from a body of text
- **schema_org** — FAQPage / Article / Breadcrumb JSON-LD (pure Python, no LLM)
- **cta** — call-to-action variants for a goal

### Providers
- OpenAI, Anthropic, Gemini, Ollama (BYOK, lazy-imported)
- Fake provider for tests and quickstart (zero API keys)
- Model-prefix routing (`gpt-*` → OpenAI, `claude-*` → Anthropic, `gemini-*` → Gemini)

### Agent runner
- `brand-loom run <skill> --text "..."` — run a single skill from CLI
- `brand-loom chain <skills> --text "..."` — linear skill chain
- `brand-loom list` — list available skills
- Python API: `run_skill()` / `run_chain()`

### Framework
- `Skill` / `SkillInput` / `SkillOutput` base types
- Skill registry with auto-discovery
- `brand_context` seam (tone, audience, do/avoid phrases)
- JSON response parsing (fenced, raw, embedded)
