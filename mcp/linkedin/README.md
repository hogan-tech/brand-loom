# brand-loom LinkedIn MCP Server

An [MCP](https://modelcontextprotocol.io/) server that exposes brand-loom LinkedIn skills as tools over stdio transport.

## Tools

| Tool | Description |
|---|---|
| `linkedin_draft_post` | Draft a LinkedIn post from a milestone or topic |
| `linkedin_score_post` | Score a post on 6 metrics (hook, skimmability, engagement, length, cta, voice_match) |
| `linkedin_analyze_profile` | Analyse a profile (headline + about) and suggest improvements |
| `linkedin_suggest_hooks` | Generate scroll-stopping hook variants for a topic |
| `linkedin_extract_voice` | Draft a voice-matched comment on a LinkedIn post |
| `linkedin_refresh_old_post` | Refresh an old post with a new angle |

## Install

```bash
pip install "brand-loom[openai]" mcp
```

## Configure a provider

```bash
export BRANDLOOM_PROVIDER=openai   # or anthropic, gemini, ollama, fake
export OPENAI_API_KEY=sk-...       # your API key
```

## Run

```bash
python -m mcp.linkedin.server
```

## Claude Desktop config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "brand-loom-linkedin": {
      "command": "python",
      "args": ["-m", "mcp.linkedin.server"],
      "env": {
        "BRANDLOOM_PROVIDER": "openai",
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

## License

[Apache-2.0](../../LICENSE). Part of [brand-loom](https://github.com/hogan-tech/brand-loom) by [Neoxra](https://neoxra.com).
