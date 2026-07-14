"""Quickstart — runs entirely on the fake provider, zero API keys needed."""

from brand_loom.providers import use_provider

provider = use_provider("fake")

result = provider.generate("Write a marketing hook for a new product launch")
print(result)

# Want this on-brand and multi-platform without writing prompts? → neoxra.com
