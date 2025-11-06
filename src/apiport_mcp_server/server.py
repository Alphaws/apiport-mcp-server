"""ApiPort MCP Server implementation"""

import logging
import os
from typing import Any
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl
import mcp.server.stdio

from .api_client import ApiPortClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
app = Server("apiport-mcp-server")

# API client will be initialized lazily
_client: ApiPortClient = None


def get_client() -> ApiPortClient:
    """Get or create API client instance"""
    global _client
    if _client is None:
        _client = ApiPortClient()
    return _client


# Tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="list_projects",
            description="List all accessible ApiPort projects",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_project",
            description="Get detailed information about a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID"},
                },
                "required": ["project_id"],
            },
        ),
        Tool(
            name="list_sprints",
            description="List all sprints for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID"},
                },
                "required": ["project_id"],
            },
        ),
        Tool(
            name="get_sprint",
            description="Get detailed information about a specific sprint",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprint_id": {"type": "integer", "description": "Sprint ID"},
                },
                "required": ["sprint_id"],
            },
        ),
        Tool(
            name="create_sprint",
            description="Create a new sprint for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID"},
                    "name": {"type": "string", "description": "Sprint name"},
                    "goal": {"type": "string", "description": "Sprint goal (optional)"},
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD, optional)",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD, optional)",
                    },
                    "velocity_target": {
                        "type": "integer",
                        "description": "Velocity target in story points (optional)",
                    },
                },
                "required": ["project_id", "name"],
            },
        ),
        Tool(
            name="activate_sprint",
            description="Activate a planned sprint to start work",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprint_id": {"type": "integer", "description": "Sprint ID to activate"},
                },
                "required": ["sprint_id"],
            },
        ),
        Tool(
            name="close_sprint",
            description="Close an active sprint",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprint_id": {"type": "integer", "description": "Sprint ID to close"},
                },
                "required": ["sprint_id"],
            },
        ),
        Tool(
            name="list_work_items",
            description="List all work items for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID"},
                },
                "required": ["project_id"],
            },
        ),
        Tool(
            name="get_work_item",
            description="Get detailed information about a specific work item",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                },
                "required": ["work_item_id"],
            },
        ),
        Tool(
            name="create_work_item",
            description="Create a new work item (task, user story, bug, or epic)",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID"},
                    "title": {"type": "string", "description": "Work item title"},
                    "description": {"type": "string", "description": "Description (optional)"},
                    "item_type": {
                        "type": "string",
                        "enum": ["task", "user_story", "bug", "epic"],
                        "description": "Type of work item (default: task)",
                    },
                    "priority": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Priority 1-5 (default: 2)",
                    },
                    "estimate_points": {
                        "type": "integer",
                        "description": "Story points estimate (optional)",
                    },
                    "assignee_id": {
                        "type": "integer",
                        "description": "User ID to assign to (optional)",
                    },
                    "sprint_id": {
                        "type": "integer",
                        "description": "Sprint ID to assign to (optional)",
                    },
                    "parent_id": {
                        "type": "integer",
                        "description": "Parent work item ID for subtasks (optional)",
                    },
                },
                "required": ["project_id", "title"],
            },
        ),
        Tool(
            name="update_work_item",
            description="Update work item fields (status, assignee, sprint, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                    "status": {
                        "type": "string",
                        "enum": ["todo", "in_progress", "done"],
                        "description": "Work item status (optional)",
                    },
                    "assignee_id": {
                        "type": "integer",
                        "description": "User ID to assign to (optional)",
                    },
                    "sprint_id": {
                        "type": "integer",
                        "description": "Sprint ID to assign to (optional)",
                    },
                    "priority": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Priority 1-5 (optional)",
                    },
                    "estimate_points": {
                        "type": "integer",
                        "description": "Story points estimate (optional)",
                    },
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"},
                },
                "required": ["work_item_id"],
            },
        ),
        Tool(
            name="get_backlog",
            description="Get all backlog items (unassigned to sprint) for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID"},
                },
                "required": ["project_id"],
            },
        ),
        Tool(
            name="bulk_assign_to_sprint",
            description="Assign multiple work items to a sprint at once",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprint_id": {"type": "integer", "description": "Sprint ID"},
                    "work_item_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of work item IDs to assign",
                    },
                },
                "required": ["sprint_id", "work_item_ids"],
            },
        ),
        Tool(
            name="add_sprint_member",
            description="Add a team member to a sprint",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprint_id": {"type": "integer", "description": "Sprint ID"},
                    "user_id": {"type": "integer", "description": "User ID to add"},
                },
                "required": ["sprint_id", "user_id"],
            },
        ),
        Tool(
            name="generate_sprint_report",
            description="Generate comprehensive sprint report with statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprint_id": {"type": "integer", "description": "Sprint ID"},
                    "project_id": {"type": "integer", "description": "Project ID"},
                },
                "required": ["sprint_id", "project_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "list_projects":
            projects = await get_client().list_projects()
            return [
                TextContent(
                    type="text",
                    text=f"Found {len(projects)} projects:\n\n"
                    + "\n".join(
                        [
                            f"- ID {p['id']}: {p['name']} (status: {p.get('status', 'N/A')})"
                            for p in projects
                        ]
                    ),
                )
            ]

        elif name == "get_project":
            project = await get_client().get_project(arguments["project_id"])
            return [
                TextContent(
                    type="text",
                    text=f"Project: {project['name']}\n"
                    f"ID: {project['id']}\n"
                    f"Status: {project.get('status', 'N/A')}\n"
                    f"Description: {project.get('description', 'N/A')}\n"
                    f"Created: {project.get('created_at', 'N/A')}",
                )
            ]

        elif name == "list_sprints":
            sprints = await get_client().list_sprints(arguments["project_id"])
            return [
                TextContent(
                    type="text",
                    text=f"Found {len(sprints)} sprints:\n\n"
                    + "\n".join(
                        [
                            f"- ID {s['id']}: {s['name']} (status: {s['status']}, "
                            f"{s.get('start_date', 'N/A')} to {s.get('end_date', 'N/A')})"
                            for s in sprints
                        ]
                    ),
                )
            ]

        elif name == "get_sprint":
            sprint = await get_client().get_sprint(arguments["sprint_id"])
            return [
                TextContent(
                    type="text",
                    text=f"Sprint: {sprint['name']}\n"
                    f"ID: {sprint['id']}\n"
                    f"Status: {sprint['status']}\n"
                    f"Goal: {sprint.get('goal', 'N/A')}\n"
                    f"Period: {sprint.get('start_date', 'N/A')} to {sprint.get('end_date', 'N/A')}\n"
                    f"Velocity Target: {sprint.get('velocity_target', 'N/A')}",
                )
            ]

        elif name == "create_sprint":
            sprint = await get_client().create_sprint(
                project_id=arguments["project_id"],
                name=arguments["name"],
                goal=arguments.get("goal"),
                start_date=arguments.get("start_date"),
                end_date=arguments.get("end_date"),
                velocity_target=arguments.get("velocity_target"),
            )
            return [
                TextContent(
                    type="text",
                    text=f"✅ Created sprint '{sprint['name']}' (ID: {sprint['id']})\n"
                    f"Status: {sprint['status']}\n"
                    f"Goal: {sprint.get('goal', 'N/A')}",
                )
            ]

        elif name == "activate_sprint":
            sprint = await get_client().activate_sprint(arguments["sprint_id"])
            return [
                TextContent(
                    type="text",
                    text=f"✅ Activated sprint '{sprint['name']}' (ID: {sprint['id']})\n"
                    f"Status: {sprint['status']}",
                )
            ]

        elif name == "close_sprint":
            sprint = await get_client().close_sprint(arguments["sprint_id"])
            return [
                TextContent(
                    type="text",
                    text=f"✅ Closed sprint '{sprint['name']}' (ID: {sprint['id']})\n"
                    f"Status: {sprint['status']}",
                )
            ]

        elif name == "list_work_items":
            items = await get_client().list_work_items(arguments["project_id"])
            return [
                TextContent(
                    type="text",
                    text=f"Found {len(items)} work items:\n\n"
                    + "\n".join(
                        [
                            f"- ID {i['id']}: {i['title']} [{i['item_type']}] "
                            f"(status: {i['status']}, priority: {i.get('priority', 'N/A')}, "
                            f"points: {i.get('estimate_points', 'N/A')})"
                            for i in items
                        ]
                    ),
                )
            ]

        elif name == "get_work_item":
            item = await get_client().get_work_item(arguments["work_item_id"])
            assignee = item.get("assignee")
            assignee_str = (
                f"{assignee.get('email', 'N/A')}" if assignee else "Unassigned"
            )
            return [
                TextContent(
                    type="text",
                    text=f"Work Item: {item['title']}\n"
                    f"ID: {item['id']}\n"
                    f"Type: {item['item_type']}\n"
                    f"Status: {item['status']}\n"
                    f"Priority: {item.get('priority', 'N/A')}\n"
                    f"Estimate: {item.get('estimate_points', 'N/A')} points\n"
                    f"Assignee: {assignee_str}\n"
                    f"Sprint: {item.get('sprint', 'Backlog')}\n"
                    f"Description: {item.get('description', 'N/A')}",
                )
            ]

        elif name == "create_work_item":
            item = await get_client().create_work_item(
                project_id=arguments["project_id"],
                title=arguments["title"],
                description=arguments.get("description"),
                item_type=arguments.get("item_type", "task"),
                priority=arguments.get("priority", 2),
                estimate_points=arguments.get("estimate_points"),
                assignee_id=arguments.get("assignee_id"),
                sprint_id=arguments.get("sprint_id"),
                parent_id=arguments.get("parent_id"),
            )
            return [
                TextContent(
                    type="text",
                    text=f"✅ Created {item['item_type']}: {item['title']} (ID: {item['id']})\n"
                    f"Status: {item['status']}\n"
                    f"Priority: {item['priority']}",
                )
            ]

        elif name == "update_work_item":
            work_item_id = arguments.pop("work_item_id")
            item = await get_client().update_work_item(work_item_id, **arguments)
            return [
                TextContent(
                    type="text",
                    text=f"✅ Updated work item: {item['title']} (ID: {item['id']})\n"
                    f"Status: {item['status']}\n"
                    f"Priority: {item.get('priority', 'N/A')}",
                )
            ]

        elif name == "get_backlog":
            items = await get_client().get_backlog(arguments["project_id"])
            return [
                TextContent(
                    type="text",
                    text=f"Found {len(items)} backlog items:\n\n"
                    + "\n".join(
                        [
                            f"- ID {i['id']}: {i['title']} [{i['item_type']}] "
                            f"(priority: {i.get('priority', 'N/A')}, "
                            f"points: {i.get('estimate_points', 'N/A')})"
                            for i in items
                        ]
                    ),
                )
            ]

        elif name == "bulk_assign_to_sprint":
            result = await get_client().bulk_assign_to_sprint(
                arguments["sprint_id"], arguments["work_item_ids"]
            )
            return [
                TextContent(
                    type="text",
                    text=f"✅ Assigned {len(arguments['work_item_ids'])} items to sprint {arguments['sprint_id']}",
                )
            ]

        elif name == "add_sprint_member":
            await get_client().add_sprint_member(arguments["sprint_id"], arguments["user_id"])
            return [
                TextContent(
                    type="text",
                    text=f"✅ Added user {arguments['user_id']} to sprint {arguments['sprint_id']}",
                )
            ]

        elif name == "generate_sprint_report":
            sprint = await get_client().get_sprint(arguments["sprint_id"])
            items = await get_client().list_work_items(arguments["project_id"])

            # Filter items for this sprint
            sprint_items = [
                i
                for i in items
                if i.get("sprint")
                and (
                    i["sprint"] == arguments["sprint_id"]
                    or (isinstance(i["sprint"], dict) and i["sprint"].get("id") == arguments["sprint_id"])
                )
            ]

            # Calculate statistics
            user_stories = [i for i in sprint_items if i["item_type"] == "user_story"]
            total_points = sum(i.get("estimate_points", 0) for i in user_stories)
            completed_points = sum(
                i.get("estimate_points", 0) for i in user_stories if i["status"] == "done"
            )
            total_tasks = len(sprint_items)
            completed_tasks = len([i for i in sprint_items if i["status"] == "done"])
            completion = (completed_points / total_points * 100) if total_points > 0 else 0

            return [
                TextContent(
                    type="text",
                    text=f"📊 Sprint Report: {sprint['name']}\n"
                    f"{'=' * 50}\n"
                    f"Sprint ID: {sprint['id']}\n"
                    f"Status: {sprint['status']}\n"
                    f"Goal: {sprint.get('goal', 'N/A')}\n"
                    f"Period: {sprint.get('start_date', 'N/A')} to {sprint.get('end_date', 'N/A')}\n\n"
                    f"📈 Story Points:\n"
                    f"  Completed: {completed_points}\n"
                    f"  Total: {total_points}\n"
                    f"  Progress: {completion:.1f}%\n\n"
                    f"✅ Tasks:\n"
                    f"  Completed: {completed_tasks}\n"
                    f"  Total: {total_tasks}\n\n"
                    f"🎯 Velocity:\n"
                    f"  Target: {sprint.get('velocity_target', 'N/A')}\n"
                    f"  Actual: {completed_points}",
                )
            ]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# Resources
@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri=AnyUrl("project://list"),
            name="Projects List",
            mimeType="application/json",
            description="List of all accessible projects",
        ),
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read a resource"""
    uri_str = str(uri)

    if uri_str == "project://list":
        projects = await get_client().list_projects()
        import json
        return json.dumps(projects, indent=2)

    elif uri_str.startswith("project://"):
        project_id = int(uri_str.split("//")[1])
        project = await get_client().get_project(project_id)
        import json
        return json.dumps(project, indent=2)

    elif uri_str.startswith("sprint://"):
        sprint_id = int(uri_str.split("//")[1])
        sprint = await get_client().get_sprint(sprint_id)
        import json
        return json.dumps(sprint, indent=2)

    elif uri_str.startswith("backlog://"):
        project_id = int(uri_str.split("//")[1])
        items = await get_client().get_backlog(project_id)
        import json
        return json.dumps(items, indent=2)

    raise ValueError(f"Unknown resource: {uri}")


def main():
    """Main entry point"""
    import asyncio

    async def run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
