---
name: linkedin_post
slug: linkedin-post
displayName: "LinkedIn Post Generator"
summary: "Engaging LinkedIn posts from milestones and topics"
description: "Use when you need to create a LinkedIn post from a milestone, achievement, or topic. Produces authentic, story-driven posts with proper formatting (line breaks, hooks, CTAs)."
version: "0.2.0"
license: Apache-2.0
compatibility: "Claude Code, Cursor, OpenClaw, or standalone via pip install brand-loom"
homepage: "https://github.com/hogan-tech/brand-loom"
when_to_use: "LinkedIn content, professional posts, milestone announcements, thought leadership posts"
argument-hint: "<milestone> [--post-type text|article|carousel] [--brand brand.json]"
metadata: {"author": "hogan-tech", "discipline": "marketing", "hosted": "https://neoxra.com"}
---

# LinkedIn Post Generator

Generate engaging LinkedIn posts from milestones, achievements, or topics. Story-driven, authentic, and formatted for LinkedIn's algorithm preferences.

## Quick start

- CLI: `brand-loom run linkedin_post --text "Just hit 10k users with zero paid ads"`
- Python API: `run_skill("linkedin_post", "raised Series A", post_type="text")`

## Post types

- `text` — standard LinkedIn post (default)
- `article` — longer form LinkedIn article intro
- `carousel` — carousel slide copy (headlines + body per slide)

> **Auto-scheduling, analytics tracking, and 6-metric quality scoring** live in hosted **[Neoxra](https://neoxra.com)**.
