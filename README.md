### Raindrop.io MCP Server

## What is Raindrop?

[Raindrop](https://raindrop.io/) is an all in one bookmark manager, It is the best place to keep all your favorite books, songs, articles or whatever else you come across while browsing.

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

## Command Supported

1. Add a bookmark with tags
2. Fetch latest bookmarks
   ... More to follow
