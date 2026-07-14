"""Tests for the CLI."""

import json
import tempfile

from brand_loom.cli import main


class TestCLIRun:
    def test_run_hook(self, capsys):
        main(["run", "hook", "--text", "cloud computing"])
        captured = capsys.readouterr()
        assert captured.out.strip()

    def test_run_with_provider(self, capsys):
        main(["run", "hook", "--text", "test", "--provider", "fake"])
        captured = capsys.readouterr()
        assert captured.out.strip()

    def test_run_with_brand_file(self, capsys):
        brand = {"tone": ["bold"], "audience": "founders"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(brand, f)
            f.flush()
            main(["run", "hook", "--text", "test", "--brand", f.name])
        captured = capsys.readouterr()
        assert captured.out.strip()


class TestCLIChain:
    def test_chain_hook_caption(self, capsys):
        main(["chain", "hook,caption", "--text", "cloud costs"])
        captured = capsys.readouterr()
        assert captured.out.strip()


class TestCLIList:
    def test_list_skills(self, capsys):
        main(["list"])
        captured = capsys.readouterr()
        output = captured.out
        assert "hook" in output
        assert "caption" in output
        assert "hashtags" in output
