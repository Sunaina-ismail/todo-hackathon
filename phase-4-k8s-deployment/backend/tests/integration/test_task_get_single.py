"""Integration Tests for Getting Single Task

Tests for retrieving a specific task via GET /api/{user_id}/tasks/{task_id}.
"""

import pytest
from fastapi.testclient import TestClient


class TestGetSingleTask:
    """Test retrieving a specific task by ID."""

    def test_get_own_task_returns_200_with_all_fields(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test get own task returns 200 with task data including priority, due_date, tags."""
        # Create a task with all fields
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "Full Featured Task",
                "description": "Task with all advanced fields",
                "priority": "High",
                "due_date": "2025-12-31",
                "tags": ["urgent", "work", "important"],
                "completed": False
            },
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Get the task
        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "Full Featured Task"
        assert task["description"] == "Task with all advanced fields"
        assert task["priority"] == "High"
        assert task["due_date"] == "2025-12-31"
        assert task["completed"] is False
        assert set(task["tags"]) == {"urgent", "work", "important"}
        assert "created_at" in task
        assert "updated_at" in task

    def test_get_nonexistent_task_returns_404(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test get non-existent task returns 404."""
        # Use a random UUID that doesn't exist
        fake_uuid = "00000000-0000-0000-0000-000000000000"

        response = client.get(
            f"/api/{test_user_id}/tasks/{fake_uuid}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_another_users_task_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test get another user's task returns 403."""
        # Create task as test_user
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Private Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to get as another user
        other_user_id = "other-user-789"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=other_headers
        )

        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_get_task_without_optional_fields(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test get task without optional fields returns correctly."""
        # Create minimal task (only title)
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Minimal Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Get the task
        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "Minimal Task"
        assert task["description"] is None or task["description"] == ""
        assert task["priority"] == "Medium"  # Default priority
        assert task["due_date"] is None
        assert task["tags"] == []
        assert task["completed"] is False

    def test_get_completed_task(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test get completed task returns correct completion status."""
        # Create completed task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Completed Task", "completed": True},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Get the task
        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["completed"] is True

    def test_get_task_with_multiple_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test get task with multiple tags returns all tags."""
        # Create task with multiple tags
        tags = ["tag1", "tag2", "tag3", "tag4", "tag5"]
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Multi-Tag Task", "tags": tags},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Get the task
        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert set(task["tags"]) == set(tags)

    def test_get_task_with_invalid_uuid_format_returns_422(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test get task with invalid UUID format returns 422."""
        # Use an invalid UUID format
        invalid_uuid = "not-a-valid-uuid"

        response = client.get(
            f"/api/{test_user_id}/tasks/{invalid_uuid}",
            headers=auth_headers
        )

        # FastAPI returns 422 for validation errors
        assert response.status_code == 422
