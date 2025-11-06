# Installation Guide - ApiPort MCP Server

## Quick Start

### 1. Install the Package

```bash
cd /home/alphaws/ai_dev/apiport-mcp-server
pip install -e .
```

Or using uv (recommended):

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
# Edit .env with your credentials
```

Or export environment variables:

```bash
export APIPORT_API_URL="https://api.apiport.hu"
export APIPORT_EMAIL="your-email@example.com"
export APIPORT_PASSWORD="your-password"
```

### 3. Test the Installation

```bash
# Quick test
python3 -c "
import asyncio
import os
from src.apiport_mcp_server.api_client import ApiPortClient

async def test():
    client = ApiPortClient(verify_ssl=False)
    projects = await client.list_projects()
    print(f'✅ Found {len(projects)} projects')
    for p in projects:
        print(f'   - {p[\"id\"]}: {p[\"name\"]}')

asyncio.run(test())
"
```

### 4. Configure Claude Desktop

**Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "apiport": {
      "command": "python3",
      "args": [
        "-m",
        "apiport_mcp_server"
      ],
      "env": {
        "APIPORT_API_URL": "https://api.apiport.hu",
        "APIPORT_EMAIL": "your-email@example.com",
        "APIPORT_PASSWORD": "your-password"
      }
    }
  }
}
```

Or with `uv` (recommended):

```json
{
  "mcpServers": {
    "apiport": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/alphaws/ai_dev/apiport-mcp-server",
        "run",
        "apiport-mcp"
      ],
      "env": {
        "APIPORT_API_URL": "https://api.apiport.hu",
        "APIPORT_EMAIL": "your-email@example.com",
        "APIPORT_PASSWORD": "your-password"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

After editing the config file, restart Claude Desktop for the changes to take effect.

### 6. Verify in Claude

In Claude Desktop, you should see the ApiPort MCP server in the available tools. Try:

```
List my ApiPort projects
```

## Troubleshooting

### Server Not Showing Up

1. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`
   - Linux: `~/.config/Claude/logs/mcp*.log`

2. Verify Python version:
   ```bash
   python3 --version  # Should be 3.10 or higher
   ```

3. Test the server manually:
   ```bash
   python3 -m apiport_mcp_server
   ```

### Authentication Errors

1. Verify credentials in config
2. Test API access:
   ```bash
   curl -X POST "https://api.apiport.hu/api/accounts/token/" \
     -H "Content-Type: application/json" \
     -d '{"email":"your-email@example.com","password":"your-password"}' -k
   ```

### SSL Certificate Errors

Add to your config `env` section:
```json
"VERIFY_SSL": "false"
```

## Development Setup

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Format Code

```bash
black .
ruff check --fix .
```

## Updating

```bash
cd /home/alphaws/ai_dev/apiport-mcp-server
git pull
pip install -e . --upgrade
```

Then restart Claude Desktop.

## Uninstalling

```bash
pip uninstall apiport-mcp-server
```

And remove the `apiport` section from Claude Desktop config.
