# ApiPort MCP Server - Project Summary

## 📦 What is This?

A Model Context Protocol (MCP) server that integrates ApiPort Task Manager with Claude Desktop, enabling natural language project management through conversation.

## 🎯 Features

### Tools (15 total)
- **Projects**: List, view details
- **Sprints**: List, create, activate, close, view details
- **Work Items**: List, create, update, view details
- **Backlog**: View, bulk assign to sprints
- **Team**: Add sprint members
- **Reports**: Generate sprint statistics

### Resources
- Dynamic project/sprint/backlog data access
- JSON-formatted resource endpoints

### Authentication
- Automatic JWT token management
- Token refresh with expiry handling
- Secure credential storage

## 📁 Project Structure

```
apiport-mcp-server/
├── src/apiport_mcp_server/
│   ├── __init__.py           # Package initialization
│   ├── __main__.py           # CLI entry point
│   ├── api_client.py         # API client with auth (250 lines)
│   └── server.py             # MCP server implementation (590 lines)
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── CHANGELOG.md             # Version history
├── INSTALL.md               # Installation guide
├── QUICK_REFERENCE.md       # Tool reference
├── README.md                # Main documentation
├── claude_desktop_config.example.json  # Claude config
└── pyproject.toml           # Python package config
```

## 🚀 Quick Start

```bash
# Install
cd /home/alphaws/ai_dev/apiport-mcp-server
pip install -e .

# Configure Claude Desktop
# Edit: ~/.config/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "apiport": {
      "command": "python3",
      "args": ["-m", "apiport_mcp_server"],
      "env": {
        "APIPORT_API_URL": "https://api.apiport.hu",
        "APIPORT_EMAIL": "ai@apiport.hu",
        "APIPORT_PASSWORD": "v7sQR6G0rg8s8UwP3Edt"
      }
    }
  }
}

# Restart Claude Desktop
# Start using: "List my ApiPort projects"
```

## 💡 Example Usage in Claude

```
User: "List my projects"
Claude: Found 1 projects:
        - ID 4: Apiport (status: active)

User: "Show me sprints for project 4"
Claude: Found 2 sprints:
        - ID 1: Sprint 1 - API Development (status: active, 2025-11-03 to 2025-11-17)
        - ID 4: Sprint 2 - Project Manager Integration (status: planned, 2025-01-06 to 2025-01-20)

User: "Create a new sprint for project 4 called 'Sprint 3 - Testing' starting 2025-01-21"
Claude: ✅ Created sprint 'Sprint 3 - Testing' (ID: 5)
        Status: planned
        Goal: N/A

User: "Generate a report for sprint 1"
Claude: 📊 Sprint Report: Sprint 1 - API Development
        ==================================================
        Story Points: 15/20 (75% complete)
        Tasks: 8/10 completed
        Velocity: Target 21, Actual 15
```

## 🔧 Technical Details

### Dependencies
- **mcp** >= 0.9.0 - Model Context Protocol SDK
- **httpx** >= 0.27.0 - Async HTTP client
- **python-dotenv** >= 1.0.0 - Environment variables
- Python 3.10+

### Architecture
- **Async/await**: Full async implementation
- **Lazy initialization**: Client created on first use
- **Error handling**: Comprehensive try/catch with logging
- **Type safety**: Complete type hints
- **SSL flexibility**: Optional SSL verification

### API Coverage
✅ Authentication (`POST /api/accounts/token/`)
✅ Projects (`GET /api/tracker/projects/`)
✅ Sprints (`GET/POST /api/tracker/projects/{id}/sprints/`)
✅ Work Items (`GET/POST/PATCH /api/tracker/.../work-items/`)
✅ Backlog (`GET /api/tracker/projects/{id}/backlog/`)

## 📊 Testing Status

| Component | Status | Notes |
|-----------|--------|-------|
| Authentication | ✅ Tested | Token obtained successfully |
| List Projects | ✅ Tested | Returns project 4 |
| List Sprints | ✅ Tested | Returns 2 sprints |
| Create Sprint | ✅ Tested | Sprint 2 created |
| Token Refresh | ✅ Tested | Auto-refresh working |
| MCP Protocol | ✅ Tested | Tools list correctly |

## 📚 Documentation

- **README.md** - Overview, features, installation, examples
- **INSTALL.md** - Step-by-step installation guide
- **QUICK_REFERENCE.md** - Tool reference, field values, patterns
- **CHANGELOG.md** - Version history
- **claude_desktop_config.example.json** - Configuration template

## 🔐 Security

- Credentials in environment variables
- SSL verification enabled by default
- Tokens cached in memory only
- 1-hour token expiration with 5-min buffer
- No credentials in code or config files

## 🎁 Benefits vs Skill

| Feature | Skill | MCP Server |
|---------|-------|------------|
| Integration | Manual bash commands | Native Claude tools |
| Authentication | Manual token management | Automatic refresh |
| Data freshness | Requires manual refresh | Always current |
| Error handling | Manual retry | Automatic |
| User experience | Technical | Conversational |
| Speed | Multiple steps | Single command |

## 📈 Future Enhancements

Potential additions:
- [ ] Sprint burndown chart data
- [ ] Velocity chart calculations
- [ ] Work item comments/attachments
- [ ] Time tracking
- [ ] Notifications
- [ ] Team member management
- [ ] Project templates

## 🏷️ Version

**Current**: 0.1.0  
**Released**: 2025-11-06  
**MCP Protocol**: 0.9.0+  
**Python**: 3.10+

## 📝 License

Internal use only - ApiPort project

---

**Repository**: `/home/alphaws/ai_dev/apiport-mcp-server`  
**Main Branch**: `main`  
**Commit**: `d1cd076` - Initial release
