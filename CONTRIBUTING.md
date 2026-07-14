<!-- SKELETON — proposed CONTRIBUTING.md for brand-loom. -->

# Contributing to brand-loom

Thanks for your interest. `brand-loom` is an intentionally small, model-agnostic library of **commodity marketing
skills**. Contributions that fit that scope are very welcome.

## Before you start: scope

`brand-loom` is open core. Some capabilities intentionally live in the hosted product (Neoxra) and will **not** be
merged here. See [SCOPE.md](SCOPE.md). In short:

- **In scope:** single-shot "text in → text out" skills; new LLM provider adapters; bug fixes; docs; tests.
- **Out of scope (will be closed):** voice-profile extraction, multi-platform orchestration (Planner/agents/Critic,
  TrafficLoop), tuned GEO/AEO/AIO scorers, analytics readers (GA4/GSC/Meta), publishers, research providers.

If unsure, open an issue first.

## Contributor License Agreement (required)

Because a hosted commercial product is built on top of this library, **all contributors must sign the
[CLA](CLA.md)** before their first PR is merged. A bot will prompt you on your PR; signing is one click. The CLA
grants Meridian Global / the maintainer a broad, irrevocable license (including use in the closed hosted product)
plus a patent grant. You keep copyright to your contribution.

## Development setup

```bash
git clone https://github.com/hogan-tech/brand-loom
cd brand-loom
pip install -e ".[dev,all]"
ruff check .
pytest
```

All tests must run **offline** (use the `fake` provider). Do not add tests that require live API keys to pass.

## Ground rules

- Never import `neoxra` / `neoxra_core`, and never reintroduce closed logic.
- Every skill accepts an optional `brand_context: dict | None` and works on the `fake` provider with zero keys.
- Keep prompt builders locale-parametric (no hard-coded language pairs).
- Ruff-clean, typed where practical, tested.

## Pull requests

1. Branch from `main`, one skill/fix per PR.
2. Add tests and update the README skills table if you add a skill.
3. Ensure CI (ruff + pytest on 3.10–3.12) is green.
4. Sign the CLA when prompted.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
