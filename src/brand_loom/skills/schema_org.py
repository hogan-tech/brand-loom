"""Schema.org JSON-LD generator — pure Python, no LLM needed.

Generates valid JSON-LD for FAQPage, Article, and BreadcrumbList schemas.
"""

from __future__ import annotations

import json

from brand_loom.skills.base import Skill, SkillInput, SkillOutput
from brand_loom.skills.registry import register


def generate_faq_schema(
    faqs: list[dict[str, str]],
    *,
    site_url: str = "",
) -> dict:
    """Generate FAQPage JSON-LD from a list of {question, answer} dicts."""
    entities = []
    for faq in faqs:
        q = faq.get("question", "")
        a = faq.get("answer", "")
        if not q or not a:
            continue
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a,
            },
        })
    schema: dict = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    if site_url:
        schema["url"] = site_url
    return schema


def generate_article_schema(
    *,
    headline: str,
    description: str = "",
    author_name: str = "",
    date_published: str = "",
    date_modified: str = "",
    image_url: str = "",
    site_url: str = "",
    publisher_name: str = "",
    publisher_logo_url: str = "",
) -> dict:
    """Generate Article JSON-LD."""
    schema: dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
    }
    if description:
        schema["description"] = description
    if author_name:
        schema["author"] = {"@type": "Person", "name": author_name}
    if date_published:
        schema["datePublished"] = date_published
    if date_modified:
        schema["dateModified"] = date_modified
    if image_url:
        schema["image"] = image_url
    if site_url:
        schema["url"] = site_url
    if publisher_name:
        publisher: dict = {"@type": "Organization", "name": publisher_name}
        if publisher_logo_url:
            publisher["logo"] = {"@type": "ImageObject", "url": publisher_logo_url}
        schema["publisher"] = publisher
    return schema


def generate_breadcrumb_schema(
    items: list[dict[str, str]],
) -> dict:
    """Generate BreadcrumbList JSON-LD from a list of {name, url} dicts."""
    elements = []
    for i, item in enumerate(items, 1):
        element: dict = {
            "@type": "ListItem",
            "position": i,
            "name": item.get("name", ""),
        }
        url = item.get("url", "")
        if url:
            element["item"] = url
        elements.append(element)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }


class SchemaOrgSkill(Skill):
    """Skill wrapper for schema.org JSON-LD generation."""

    @property
    def name(self) -> str:
        return "schema_org"

    def run(self, inp: SkillInput) -> SkillOutput:
        ctx = inp.context or {}
        schema_type = ctx.get("schema_type", "faq")

        if schema_type == "faq":
            faqs = ctx.get("faqs", [])
            schema = generate_faq_schema(faqs, site_url=ctx.get("site_url", ""))
        elif schema_type == "article":
            schema = generate_article_schema(
                headline=ctx.get("headline", inp.text),
                description=ctx.get("description", ""),
                author_name=ctx.get("author_name", ""),
                date_published=ctx.get("date_published", ""),
                date_modified=ctx.get("date_modified", ""),
                image_url=ctx.get("image_url", ""),
                site_url=ctx.get("site_url", ""),
                publisher_name=ctx.get("publisher_name", ""),
                publisher_logo_url=ctx.get("publisher_logo_url", ""),
            )
        elif schema_type == "breadcrumb":
            items = ctx.get("items", [])
            schema = generate_breadcrumb_schema(items)
        else:
            return SkillOutput(text="", metadata={"error": f"Unknown schema_type: {schema_type}"})

        return SkillOutput(
            text=json.dumps(schema, indent=2),
            metadata={"schema_type": schema_type},
        )


register(SchemaOrgSkill())
