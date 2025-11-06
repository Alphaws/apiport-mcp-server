# ApiPort MCP Server

Model Context Protocol (MCP) server for ApiPort Task Manager integration.

## Features

### Tools
- `list_projects` - List all accessible projects
- `get_project` - Get detailed project information
- `list_sprints` - List sprints for a project
- `get_sprint` - Get detailed sprint information
- `create_sprint` - Create a new sprint
- `activate_sprint` - Activate a planned sprint
- `close_sprint` - Close an active sprint
- `list_work_items` - List work items for a project
- `get_work_item` - Get detailed work item information
- `create_work_item` - Create a new work item
- `update_work_item` - Update work item details
- `get_backlog` - Get backlog items for a project
- `bulk_assign_to_sprint` - Assign multiple work items to a sprint
- `add_sprint_member` - Add a team member to a sprint
- `generate_sprint_report` - Generate sprint statistics and report

### Resources
- `project://{project_id}` - Project details with metadata
- `sprint://{sprint_id}` - Sprint details with statistics
- `backlog://{project_id}` - Project backlog items

## Installation

### Prerequisites
- Python 3.10 or higher
- Access to ApiPort API (https://api.apiport.hu)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -e .
```

3. Create `.env` file in the project root:
```bash
APIPORT_API_URL=https://api.apiport.hu
APIPORT_EMAIL=your-email@example.com
APIPORT_PASSWORD=your-password
```

### Configure Claude Desktop

Add to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "apiport": {
      "command": "python",
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

Or using `uv` (recommended):

```json
{
  "mcpServers": {
    "apiport": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/apiport-mcp-server",
        "run",
        "apiport-mcp-server"
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

## Usage Examples

### List Projects
```
Claude, can you list all my ApiPort projects?
```

### Create a Sprint
```
Create a new sprint for project 4:
- Name: "Sprint 3 - User Authentication"
- Goal: "Complete login and registration"
- Start: 2025-01-13
- End: 2025-01-27
- Velocity target: 25
```

### View Sprint Report
```
Show me the report for sprint 1
```

### Manage Work Items
```
Create a user story for project 4:
- Title: "User password reset"
- Priority: High
- Estimate: 8 points
```

### Sprint Planning
```
Show me the backlog for project 4 and add items 15, 16, 17 to sprint 2
```

## Development

### Run Tests
```bash
pytest
```

### Format Code
```bash
black .
ruff check --fix .
```

### Debug Mode
Set environment variable for verbose logging:
```bash
DEBUG=1 python -m apiport_mcp_server
```

## Authentication

The server automatically handles JWT token authentication:
- Tokens are obtained on first request
- Tokens are cached and refreshed when expired
- No manual token management needed

## API Endpoints

Base URL: `https://api.apiport.hu/api`

- **Auth**: `POST /accounts/token/`
- **Projects**: `GET/POST /tracker/projects/`
- **Sprints**: `GET/POST /tracker/projects/{id}/sprints/`
- **Work Items**: `GET/POST /tracker/projects/{id}/work-items/`
- **Backlog**: `GET /tracker/projects/{id}/backlog/`

## Troubleshooting

### Connection Issues
- Verify API URL is correct (`https://api.apiport.hu`)
- Check credentials in `.env` or config
- Ensure network connectivity

### Token Expiration
- Tokens expire after 1 hour
- Server automatically refreshes tokens
- If issues persist, restart Claude Desktop

### SSL Certificate Errors
- Development: Set `VERIFY_SSL=false` in config
- Production: Ensure valid SSL certificates

## License

Internal use only - ApiPort project

## Version

- **Version**: 0.1.0
- **Last Updated**: 2025-11-06
- **MCP Protocol**: 0.9.0+
- **Python**: 3.10+
