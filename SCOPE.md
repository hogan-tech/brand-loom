# Scope — what belongs in brand-loom

`brand-loom` is an intentionally small, model-agnostic library of **commodity marketing skills**. This
document defines what is in scope and what is not.

## In scope (contributions welcome)

- **Single-shot "text in → text out" skills** — hooks, captions, hashtags, SEO outlines, FAQs,
  schema.org markup, CTAs, content repurposing, and similar commodity generators.
- **New LLM provider adapters** — any model behind the `LLMProvider` protocol.
- **Bug fixes, test improvements, documentation.**
- **Locale/i18n improvements** to existing skills.
- **The thin agent runner** — `run_skill` / `run_chain`, linear single-pass only.

## Out of scope (will be closed)

These capabilities live in the hosted product ([neoxra.com](https://neoxra.com)) and will **not** be
merged into this repo. PRs adding them will be closed with a pointer to this document.

| Category | Examples |
|---|---|
| **Voice-profile extraction** | Auto-detecting tone/style from existing content, voice YAML schema |
| **Multi-platform orchestration** | Planner→Platform agents→Critic, 2-pass refine, TrafficLoop |
| **Tuned scorers** | GEO/AEO/AIO extractability, snippet-readiness, RankMath, content scoring |
| **Analytics/publish integrations** | GA4 reader, GSC reader, Meta Insights, social publishers |
| **Research providers** | Tavily, Perplexity, SERP research, competitor scraping |
| **Brand Kit / no-code UI** | Visual identity storage, web dashboard |

## Rule of thumb

If a skill's value is in a *tuned prompt, a scored heuristic, a proprietary YAML schema, an
analytics/publish integration, or the orchestration graph* — it stays closed. If it's a single-shot
"text in → text out" generator that any competitor already ships — it's fair game to open.

## Dependency direction

`brand-loom` depends on **nothing proprietary**. The hosted product imports `brand-loom` and adds
closed layers on top. Never the reverse.
