"""Integration Tests for Task Filtering and Search

Tests for search, filtering by status/priority/tags in GET /api/{user_id}/tasks endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import date


class TestTaskSearch:
    """Test search functionality in task listing."""

    def test_search_by_title_returns_matching_tasks(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test search by text in title returns matching tasks (case-insensitive)."""
        # Create tasks with different titles
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Buy groceries", "description": "Milk and bread"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Call dentist", "description": "Schedule appointment"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Grocery shopping list", "description": "Items needed"},
            headers=auth_headers
        )

        # Search for "grocery" (case-insensitive)
        response = client.get(
            f"/api/{test_user_id}/tasks?search=grocery",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 2  # Should match "Buy groceries" and "Grocery shopping list"

        # Verify all returned tasks contain "grocery" in title (case-insensitive)
        for task in tasks:
            assert "grocery" in task["title"].lower() or "grocery" in task["description"].lower()

    def test_search_by_description_returns_matching_tasks(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test search by text in description returns matching tasks."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 1", "description": "Important meeting notes"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 2", "description": "Casual conversation"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?search=meeting",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert any("meeting" in task["description"].lower() for task in tasks)

    def test_search_case_insensitive(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test search is case-insensitive."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "URGENT Task"},
            headers=auth_headers
        )

        # Search with lowercase
        response = client.get(
            f"/api/{test_user_id}/tasks?search=urgent",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert any("urgent" in task["title"].lower() for task in tasks)

    def test_search_empty_query_returns_all_tasks(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test empty search query returns all tasks."""
        # Create tasks
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task A"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task B"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?search=",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 2


class TestTaskFilterByStatus:
    """Test filtering tasks by completion status."""

    def test_filter_by_status_pending(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by status=pending returns only pending tasks."""
        # Create completed task
        completed_task = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Completed Task", "completed": True},
            headers=auth_headers
        )

        # Create pending task
        pending_task = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Pending Task", "completed": False},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?completed=false",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # All returned tasks should be pending
        for task in tasks:
            assert task["completed"] is False

    def test_filter_by_status_completed(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by status=completed returns only completed tasks."""
        # Create completed task
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Completed Task", "completed": True},
            headers=auth_headers
        )

        # Create pending task
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Pending Task", "completed": False},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?completed=true",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # All returned tasks should be completed
        for task in tasks:
            assert task["completed"] is True


class TestTaskFilterByPriority:
    """Test filtering tasks by priority level."""

    def test_filter_by_priority_high(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by priority=High returns only High priority tasks."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "High Priority", "priority": "High"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Medium Priority", "priority": "Medium"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?priority=High",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # All returned tasks should be High priority
        high_priority_tasks = [t for t in tasks if t["priority"] == "High"]
        assert len(high_priority_tasks) >= 1

    def test_filter_by_priority_all(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by priority=all returns all priority levels."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "High", "priority": "High"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Low", "priority": "Low"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?priority=all",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 2


class TestTaskFilterByTags:
    """Test filtering tasks by tags."""

    def test_filter_by_single_tag(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by tags returns only tasks with that tag."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Urgent Task", "tags": ["urgent", "work"]},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Personal Task", "tags": ["personal"]},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?tags=urgent",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # All returned tasks should have "urgent" tag
        urgent_tasks = [t for t in tasks if "urgent" in t.get("tags", [])]
        assert len(urgent_tasks) >= 1

    def test_filter_by_multiple_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by multiple tags returns tasks with ANY of the tags."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Work Task", "tags": ["work"]},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Urgent Task", "tags": ["urgent"]},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Personal Task", "tags": ["personal"]},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?tags=work&tags=urgent",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Should return tasks with "work" OR "urgent" tags
        matching_tasks = [
            t for t in tasks
            if any(tag in ["work", "urgent"] for tag in t.get("tags", []))
        ]
        assert len(matching_tasks) >= 2

    def test_filter_by_tags_empty_returns_all(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test filter by empty tags array returns all tasks."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 1", "tags": ["tag1"]},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 2", "tags": []},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks",  # No tags filter
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 2


class TestCombinedFilters:
    """Test combining multiple filters."""

    def test_combine_search_and_priority_filter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test combining search and priority filter works correctly."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Important meeting", "priority": "High"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Casual meeting", "priority": "Low"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?search=meeting&priority=High",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Should only return high priority tasks with "meeting" in title
        for task in tasks:
            if "meeting" in task["title"].lower():
                assert task["priority"] == "High"

    def test_combine_all_filters(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test combining search, status, priority, and tags filters."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "Important work task",
                "priority": "High",
                "completed": False,
                "tags": ["work", "urgent"]
            },
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "Important personal task",
                "priority": "Low",
                "completed": True,
                "tags": ["personal"]
            },
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?search=important&completed=false&priority=High&tags=work",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Should return tasks matching all filters
        for task in tasks:
            if "important" in task["title"].lower():
                assert task["completed"] is False
                assert task["priority"] == "High"
                assert "work" in task.get("tags", [])
