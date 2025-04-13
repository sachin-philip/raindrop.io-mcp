### Raindrop.io MCP Server
[![smithery badge](https://smithery.ai/badge/@sachin-philip/raindrop-io-mcp)](https://smithery.ai/server/@sachin-philip/raindrop-io-mcp)

## What is Raindrop?

[Raindrop](https://raindrop.io/) is an all in one bookmark manager, It is the best place to keep all your favorite books, songs, articles or whatever else you come across while browsing.

## Prerequisites

1. Python 3.11
2. Install UV `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Install Dependancy `uv activate && uv install`

## How to use the MCP Server

1. Grab an API token from [raindrop.io](https://developer.raindrop.io/v1/authentication/token)
2. Navigate to your mcp config and add the following

```json
{
  "mcpServers": {
    "Raindrop": {
      "command": "uv",
      "args": [
        "--directory",
        "<location to project clone location>",
        "run",
        "raindrop.py"
      ],
      "env": {
        "RAINDROP_TOKEN": "<raindrop token>"
      }
    }
  }
}
```

3. Restart your LLM App (Claude/Cursor etc) and voila!

### Installing via Smithery

To install raindrop-io-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@sachin-philip/raindrop-io-mcp):

```bash
npx -y @smithery/cli install @sachin-philip/raindrop-io-mcp --client claude
```

## Command Supported

1. Add a bookmark with tags
2. Fetch latest bookmarks
3. Search bookmark by tag
4. Search bookmark by query

... More to follow
