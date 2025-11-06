# Quick Reference - ApiPort MCP Server

## Available Tools

### Projects
```
list_projects                    # List all projects
get_project(project_id)          # Get project details
```

### Sprints
```
list_sprints(project_id)                                    # List project sprints
get_sprint(sprint_id)                                        # Get sprint details
create_sprint(project_id, name, goal?, start_date?, ...)    # Create new sprint
activate_sprint(sprint_id)                                   # Start sprint
close_sprint(sprint_id)                                      # Close sprint
```

### Work Items
```
list_work_items(project_id)                                  # List all work items
get_work_item(work_item_id)                                  # Get item details
create_work_item(project_id, title, type?, priority?, ...)  # Create work item
update_work_item(work_item_id, status?, assignee_id?, ...)  # Update work item
```

### Backlog & Planning
```
get_backlog(project_id)                                # Get backlog items
bulk_assign_to_sprint(sprint_id, work_item_ids[])     # Assign multiple items
add_sprint_member(sprint_id, user_id)                  # Add team member
```

### Reporting
```
generate_sprint_report(sprint_id, project_id)  # Sprint statistics
```

## Resources

```
project://list           # All projects
project://{id}           # Specific project
sprint://{id}            # Specific sprint
backlog://{project_id}   # Project backlog
```

## Common Patterns

### Create Sprint with Tasks
```
1. create_sprint(4, "Sprint 3", goal="Complete auth")
2. get_backlog(4)
3. bulk_assign_to_sprint(sprint_id, [item_ids...])
4. activate_sprint(sprint_id)
```

### Daily Updates
```
1. list_work_items(4)
2. update_work_item(item_id, status="in_progress")
3. update_work_item(item_id, status="done")
```

### Sprint Planning
```
1. list_sprints(4)
2. get_sprint(sprint_id)
3. generate_sprint_report(sprint_id, 4)
4. close_sprint(sprint_id)
```

### Work Item Creation
```
# User Story
create_work_item(4, "Login feature",
  item_type="user_story",
  priority=4,
  estimate_points=8)

# Task
create_work_item(4, "Design login UI",
  item_type="task",
  parent_id=story_id)

# Bug
create_work_item(4, "Fix validation",
  item_type="bug",
  priority=5)
```

## Field Values

### item_type
- `task` - Regular task
- `user_story` - User story with points
- `bug` - Bug report
- `epic` - Large feature

### status
- `todo` - Not started
- `in_progress` - Currently working
- `done` - Completed

### priority
- `1` - Lowest
- `2` - Low
- `3` - Medium (default)
- `4` - High
- `5` - Critical

### sprint.status
- `planned` - Not started
- `active` - Currently running
- `completed` - Finished

## Example Prompts for Claude

```
"List all projects"
"Show me sprints for project 4"
"Create a sprint called 'Sprint 3' for project 4 starting 2025-01-13"
"What's in the backlog for project 4?"
"Add items 10, 11, 12 to sprint 2"
"Create a user story: 'Password reset' with 5 points"
"Update work item 60 status to done"
"Generate a report for sprint 1"
"Show me all high priority bugs"
```

## Environment Variables

```bash
APIPORT_API_URL      # API base URL (default: https://api.apiport.hu)
APIPORT_EMAIL        # User email
APIPORT_PASSWORD     # User password
VERIFY_SSL           # SSL verification (default: true)
DEBUG                # Enable debug logging
```

## Quick Debug

```bash
# Test authentication
python3 -c "from src.apiport_mcp_server.api_client import ApiPortClient; import asyncio; asyncio.run(ApiPortClient(verify_ssl=False)._get_token())"

# List projects
python3 test_client.py
```

## Useful Links

- [Full README](README.md)
- [Installation Guide](INSTALL.md)
- [Changelog](CHANGELOG.md)
- [ApiPort API](https://api.apiport.hu)
