"""ApiPort API Client with authentication and request handling"""

import os
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ApiPortClient:
    """Client for ApiPort Task Manager API with JWT authentication"""

    def __init__(
        self,
        api_url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        verify_ssl: bool = True,
    ):
        self.api_url = api_url or os.getenv("APIPORT_API_URL", "https://api.apiport.hu")
        self.email = email or os.getenv("APIPORT_EMAIL")
        self.password = password or os.getenv("APIPORT_PASSWORD")
        self.verify_ssl = verify_ssl if verify_ssl else os.getenv("VERIFY_SSL", "true").lower() == "true"

        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None

        if not self.email or not self.password:
            raise ValueError("APIPORT_EMAIL and APIPORT_PASSWORD must be set")

    async def _get_token(self) -> str:
        """Get access token, refreshing if necessary"""
        if self.access_token and self.token_expires_at:
            # Check if token is still valid (with 5 min buffer)
            if datetime.now() < self.token_expires_at - timedelta(minutes=5):
                return self.access_token

        # Get new token
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.post(
                f"{self.api_url}/api/accounts/token/",
                json={"email": self.email, "password": self.password},
            )
            response.raise_for_status()
            data = response.json()

            self.access_token = data["access"]
            self.refresh_token = data.get("refresh")
            # Tokens expire after 1 hour
            self.token_expires_at = datetime.now() + timedelta(hours=1)

            logger.info("Successfully obtained new access token")
            return self.access_token

    async def _request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make authenticated API request"""
        token = await self._get_token()

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.request(
                method,
                f"{self.api_url}/api/tracker/{endpoint}",
                headers={"Authorization": f"Bearer {token}"},
                json=json,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    # Project methods
    async def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        data = await self._request("GET", "projects/")
        return data.get("projects", [])

    async def get_project(self, project_id: int) -> Dict[str, Any]:
        """Get project details"""
        data = await self._request("GET", f"projects/{project_id}/")
        return data.get("project", {})

    # Sprint methods
    async def list_sprints(self, project_id: int) -> List[Dict[str, Any]]:
        """List sprints for a project"""
        data = await self._request("GET", f"projects/{project_id}/sprints/")
        return data.get("sprints", [])

    async def get_sprint(self, sprint_id: int) -> Dict[str, Any]:
        """Get sprint details"""
        data = await self._request("GET", f"sprints/{sprint_id}/")
        return data.get("sprint", {})

    async def create_sprint(
        self,
        project_id: int,
        name: str,
        goal: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        velocity_target: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a new sprint"""
        payload = {
            "name": name,
            "status": "planned",
        }
        if goal:
            payload["goal"] = goal
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        if velocity_target:
            payload["velocity_target"] = velocity_target

        data = await self._request("POST", f"projects/{project_id}/sprints/", json=payload)
        return data.get("sprint", {})

    async def activate_sprint(self, sprint_id: int) -> Dict[str, Any]:
        """Activate a planned sprint"""
        data = await self._request("POST", f"sprints/{sprint_id}/activate/")
        return data.get("sprint", {})

    async def close_sprint(self, sprint_id: int) -> Dict[str, Any]:
        """Close an active sprint"""
        data = await self._request("POST", f"sprints/{sprint_id}/close/")
        return data.get("sprint", {})

    # Work Item methods
    async def list_work_items(self, project_id: int) -> List[Dict[str, Any]]:
        """List work items for a project"""
        data = await self._request("GET", f"projects/{project_id}/work-items/")
        return data.get("work_items", [])

    async def get_work_item(self, work_item_id: int) -> Dict[str, Any]:
        """Get work item details"""
        data = await self._request("GET", f"work-items/{work_item_id}/")
        return data.get("work_item", {})

    async def create_work_item(
        self,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        item_type: str = "task",
        priority: int = 2,
        estimate_points: Optional[int] = None,
        assignee_id: Optional[int] = None,
        sprint_id: Optional[int] = None,
        parent_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a new work item"""
        payload = {
            "title": title,
            "item_type": item_type,
            "priority": priority,
            "status": "todo",
        }
        if description:
            payload["description"] = description
        if estimate_points:
            payload["estimate_points"] = estimate_points
        if assignee_id:
            payload["assignee_id"] = assignee_id
        if sprint_id:
            payload["sprint_id"] = sprint_id
        if parent_id:
            payload["parent_id"] = parent_id

        data = await self._request("POST", f"projects/{project_id}/work-items/", json=payload)
        return data.get("work_item", {})

    async def update_work_item(
        self,
        work_item_id: int,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Update work item fields"""
        data = await self._request("PATCH", f"work-items/{work_item_id}/", json=kwargs)
        return data.get("work_item", {})

    # Backlog methods
    async def get_backlog(self, project_id: int) -> List[Dict[str, Any]]:
        """Get backlog items for a project"""
        data = await self._request("GET", f"projects/{project_id}/backlog/")
        return data.get("work_items", [])

    async def bulk_assign_to_sprint(
        self, sprint_id: int, work_item_ids: List[int]
    ) -> Dict[str, Any]:
        """Bulk assign work items to a sprint"""
        data = await self._request(
            "POST",
            f"sprints/{sprint_id}/bulk-assign/",
            json={"work_item_ids": work_item_ids},
        )
        return data

    # Sprint Members methods
    async def add_sprint_member(self, sprint_id: int, user_id: int) -> Dict[str, Any]:
        """Add a team member to a sprint"""
        data = await self._request(
            "POST", f"sprints/{sprint_id}/members/", json={"user_id": user_id}
        )
        return data

    async def remove_sprint_member(self, sprint_id: int, member_id: int) -> Dict[str, Any]:
        """Remove a team member from a sprint"""
        data = await self._request("DELETE", f"sprints/{sprint_id}/members/{member_id}/")
        return data
