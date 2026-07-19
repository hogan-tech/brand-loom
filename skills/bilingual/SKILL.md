---
name: bilingual
slug: bilingual
displayName: "Bilingual Translator (EN ↔ zh-TW)"
summary: "Voice-preserving translation between English and Traditional Chinese"
description: "Use when you need to translate marketing copy between EN and zh-TW while preserving brand voice, tone, and impact. Not word-level translation — a voice-preserving rewrite in the target locale."
version: "0.2.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "bilingual content, EN to zh-TW translation, zh-TW to EN translation, localization, i18n marketing copy"
argument-hint: "<text> --target-locale zh-TW [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# Bilingual Translator (EN ↔ zh-TW)

Voice-preserving translation between English and Traditional Chinese. Preserves brand tone, audience targeting, and phrase preferences across languages.

## Quick start

- CLI: `brand-loom run bilingual --text "Ship it, then iterate." --target-locale zh-TW`
- Python API: `run_skill("bilingual", "Ship it.", target_locale="zh-TW")`

## Features

- Voice-preserving rewrite (not word-level translation)
- Supports `preserve_terms` to keep brand names, acronyms verbatim
- Full `brand_context` support (tone, audience, do/avoid phrases)
- Returns unchanged if source = target locale

> **Multi-language support beyond EN/zh-TW** (auto-detection, 10+ locales, continuous voice alignment) lives in hosted **[Neoxra](https://neoxra.com)**.
