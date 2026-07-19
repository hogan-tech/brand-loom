# Changelog

## 0.2.0 (2026-07-19)

### Added
- **bilingual** skill — EN ↔ zh-TW voice-preserving translation with preserve_terms support
- **linkedin_post** skill — LinkedIn post generation from milestones/topics (text, article, carousel)
- Generic few-shot exemplars in every prompt builder (lifts baseline output quality)
- Opt-in self-check lint (`self_check=True`) — anti-slop, banned phrases, frontmatter leak detection
- Provider parity eval (`make eval-parity`) — proves model-agnostic execution across all providers
- Before/after brand_context demo (`examples/before_after_demo.py`)
- `RICH_BRAND_CONTEXT` with detailed tone, audience, and phrase guidance
- `examples/sample_brand_context.json` for CLI usage
- `Makefile` with lint, test, and eval-parity targets

### Changed
- Provider parity matrix expanded to 9 skills (from 7)
- README skill table updated to v0.2 (10 skills total)

## 0.1.1 (2026-07-15)

### Bug fixes
- **Provider precedence:** `use_provider()` and `--provider` flag now correctly beat the `BRANDLOOM_PROVIDER` env var. Previously the env var silently overrode explicit provider selection, potentially spending API credits on the wrong vendor. (#20, #22)
- **Hashtag dedupe:** skip empty/whitespace-only tags instead of emitting bare `#` entries. (#18)
- **FAQ metadata:** report the clamped count (3–6) in skill metadata instead of the raw user input. (#19)

### Tests
- Added brand_context schema contract + cross-skill seam coverage (39 new tests). (#21)

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
