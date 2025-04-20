# 🌧️ Raindrop.io MCP Server
[![Smithery Badge](https://smithery.ai/badge/@sachin-philip/raindrop-io-mcp)](https://smithery.ai/server/@sachin-philip/raindrop-io-mcp)

## Overview
[Raindrop.io](https://raindrop.io/) is an all-in-one bookmark manager. This MCP server integration lets you manage your bookmarks programmatically—add, search, and organize your favorite links right from your LLM apps.

---

## ✨ Features
- **Add a bookmark** (with tags, description, collection)
- **Get latest bookmarks**
- **Search bookmarks by tag**
- **Search bookmarks by keyword/text**

---

## 🚀 Quickstart

### Prerequisites
- Python **3.11**
- [UV](https://astral.sh/uv/) package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv activate && uv install
```

---

### MCP Server Configuration
1. Grab an API token from [Raindrop.io Developer Portal](https://developer.raindrop.io/v1/authentication/token)
2. Add the following to your MCP config:

```jsonc
{
  "mcpServers": {
    "Raindrop": {
      "command": "uv",
      "args": [
        "--directory",
        "<location to project clone>",
        "run",
        "raindrop.py"
      ],
      "env": {
        "RAINDROP_TOKEN": "<your_raindrop_token>"
      }
    }
  }
}
```

3. Restart your LLM app (Claude, Cursor, etc.)

---

### 📦 Install via Smithery
Install automatically for Claude Desktop:

```bash
npx -y @smithery/cli install @sachin-philip/raindrop-io-mcp --client claude
```

---

## 🛠️ Supported Commands
- Add a bookmark (with tags, description, collection)
- Get latest bookmarks
- Search bookmarks by tag
- Search bookmarks by keyword/text

... More to follow
---

## 📝 License
MIT

---

## 🙌 Credits
Built by [Sachin Philip](https://github.com/sachin-philip)
