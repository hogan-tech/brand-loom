"""Tests for the lightweight self-check / lint module."""

from brand_loom.selfcheck import lint


class TestAntiSlop:
    def test_flags_fast_paced_world(self):
        issues = lint("In today's fast-paced world, marketing matters.")
        assert any(i["rule"] == "anti-slop" for i in issues)

    def test_flags_delve(self):
        issues = lint("Let's delve into the details of this topic.")
        assert any(i["rule"] == "anti-slop" for i in issues)

    def test_flags_unlock(self):
        issues = lint("Unlock the power of social media marketing today.")
        assert any(i["rule"] == "anti-slop" for i in issues)

    def test_flags_digital_age(self):
        issues = lint("In today's digital age, every brand needs a strategy.")
        assert any(i["rule"] == "anti-slop" for i in issues)


class TestBannedGeneric:
    def test_flags_synergies(self):
        issues = lint("We should leverage synergies across all departments.")
        assert any(i["rule"] == "banned-generic" for i in issues)

    def test_flags_thought_leader(self):
        issues = lint("Position yourself as a thought leader in your niche.")
        assert any(i["rule"] == "banned-generic" for i in issues)


class TestLeakedFrontmatter:
    def test_flags_yaml_frontmatter(self):
        text = "---\ntitle: something\n---\nActual content here."
        issues = lint(text)
        assert any(i["rule"] == "leaked-frontmatter" for i in issues)


class TestSystemLeak:
    def test_flags_as_an_ai(self):
        issues = lint("As an AI language model, I cannot provide financial advice.")
        assert any(i["rule"] == "system-leak" for i in issues)

    def test_flags_i_cannot(self):
        issues = lint("I cannot help with that request, but here's what I can do.")
        assert any(i["rule"] == "system-leak" for i in issues)


class TestTooShort:
    def test_flags_short_output(self):
        issues = lint("Too short.")
        assert any(i["rule"] == "too-short" for i in issues)

    def test_does_not_flag_empty(self):
        issues = lint("")
        assert not any(i["rule"] == "too-short" for i in issues)


class TestCleanText:
    def test_clean_text_passes(self):
        text = (
            "We reduced our cloud infrastructure costs by 40% in three months. "
            "The key was right-sizing instances, switching to spot instances for "
            "batch jobs, and implementing auto-scaling policies that matched "
            "actual usage patterns."
        )
        issues = lint(text)
        assert issues == []

    def test_clean_hooks_pass(self):
        text = '["5 ways to cut cloud costs without sacrificing performance"]'
        issues = lint(text)
        assert issues == []


class TestSelfCheckIntegration:
    def test_self_check_false_unchanged(self):
        from brand_loom.agent import run_skill
        from brand_loom.providers import use_provider

        use_provider("fake")
        result = run_skill("hook", "cloud costs")
        assert "lint" not in result.metadata

    def test_self_check_true_adds_lint(self):
        from brand_loom.agent import run_skill
        from brand_loom.providers import use_provider

        use_provider("fake")
        result = run_skill("hook", "cloud costs", self_check=True)
        assert "lint" in result.metadata
        assert isinstance(result.metadata["lint"], list)
