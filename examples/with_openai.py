"""Example using OpenAI provider (requires OPENAI_API_KEY)."""

from brand_loom.providers import use_provider

# Set your key: export OPENAI_API_KEY=sk-...
provider = use_provider("openai")

result = provider.generate(
    "Write 3 marketing hooks for a SaaS product launch",
    system="You are a marketing copywriter. Be concise and punchy.",
)
print(result)

# Want this on-brand and multi-platform without writing prompts? → neoxra.com
