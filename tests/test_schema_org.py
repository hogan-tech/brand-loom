"""Tests for Schema.org JSON-LD generation."""

import json

from brand_loom.skills.schema_org import (
    SchemaOrgSkill,
    generate_article_schema,
    generate_breadcrumb_schema,
    generate_faq_schema,
)


class TestFAQSchema:
    def test_basic_faq(self):
        faqs = [
            {"question": "What is X?", "answer": "X is great."},
            {"question": "How does it work?", "answer": "It just works."},
        ]
        schema = generate_faq_schema(faqs)
        assert schema["@type"] == "FAQPage"
        assert schema["@context"] == "https://schema.org"
        assert len(schema["mainEntity"]) == 2
        assert schema["mainEntity"][0]["name"] == "What is X?"

    def test_empty_input(self):
        schema = generate_faq_schema([])
        assert schema["mainEntity"] == []

    def test_skips_incomplete_entries(self):
        faqs = [{"question": "Q1"}, {"answer": "A2"}, {"question": "Q3", "answer": "A3"}]
        schema = generate_faq_schema(faqs)
        assert len(schema["mainEntity"]) == 1

    def test_site_url(self):
        schema = generate_faq_schema(
            [{"question": "Q", "answer": "A"}],
            site_url="https://example.com",
        )
        assert schema["url"] == "https://example.com"

    def test_valid_json(self):
        faqs = [{"question": "Q?", "answer": "A."}]
        schema = generate_faq_schema(faqs)
        text = json.dumps(schema)
        parsed = json.loads(text)
        assert parsed["@type"] == "FAQPage"


class TestArticleSchema:
    def test_basic_article(self):
        schema = generate_article_schema(headline="Test Article")
        assert schema["@type"] == "Article"
        assert schema["headline"] == "Test Article"

    def test_full_article(self):
        schema = generate_article_schema(
            headline="Full Article",
            description="A full test",
            author_name="Author",
            date_published="2026-01-01",
            date_modified="2026-01-02",
            image_url="https://example.com/img.jpg",
            site_url="https://example.com/article",
            publisher_name="Publisher Co",
            publisher_logo_url="https://example.com/logo.png",
        )
        assert schema["author"]["name"] == "Author"
        assert schema["publisher"]["logo"]["url"] == "https://example.com/logo.png"


class TestBreadcrumbSchema:
    def test_basic_breadcrumb(self):
        items = [
            {"name": "Home", "url": "https://example.com"},
            {"name": "Blog", "url": "https://example.com/blog"},
            {"name": "Post"},
        ]
        schema = generate_breadcrumb_schema(items)
        assert schema["@type"] == "BreadcrumbList"
        assert len(schema["itemListElement"]) == 3
        assert schema["itemListElement"][0]["position"] == 1
        assert "item" not in schema["itemListElement"][2]

    def test_empty_breadcrumb(self):
        schema = generate_breadcrumb_schema([])
        assert schema["itemListElement"] == []


class TestSchemaOrgSkill:
    def test_skill_registration(self):
        from brand_loom.skills.registry import get_skill

        skill = get_skill("schema_org")
        assert skill.name == "schema_org"

    def test_faq_via_skill(self):
        from brand_loom.skills.base import SkillInput

        skill = SchemaOrgSkill()
        result = skill.run(SkillInput(
            text="",
            context={
                "schema_type": "faq",
                "faqs": [{"question": "Q?", "answer": "A."}],
            },
        ))
        data = json.loads(result.text)
        assert data["@type"] == "FAQPage"

    def test_article_via_skill(self):
        from brand_loom.skills.base import SkillInput

        skill = SchemaOrgSkill()
        result = skill.run(SkillInput(
            text="My Article",
            context={"schema_type": "article", "headline": "My Article"},
        ))
        data = json.loads(result.text)
        assert data["headline"] == "My Article"

    def test_unknown_schema_type(self):
        from brand_loom.skills.base import SkillInput

        skill = SchemaOrgSkill()
        result = skill.run(SkillInput(text="", context={"schema_type": "unknown"}))
        assert result.text == ""
        assert "error" in result.metadata
