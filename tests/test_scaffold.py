"""Smoke test: package imports and version is set."""


def test_version():
    from brand_loom import __version__

    assert __version__ == "0.1.0"
