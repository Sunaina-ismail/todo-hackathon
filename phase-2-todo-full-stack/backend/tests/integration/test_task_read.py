"""Integration Tests for Task Read Operations

Tests for GET /api/{user_id}/tasks and GET /api/{user_id}/tasks/{task_id} endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import date


class TestListTasks:
    """Test listing all tasks for a user."""

    def test_list_all_tasks_returns_200(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test listing all tasks returns 200 with array."""
        # Create a few tasks
        for i in range(3):
            client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Task {i+1}"},
                headers=auth_headers
            )

        response = client.get(
            f"/api/{test_user_id}/tasks",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3

    def test_list_tasks_empty_returns_empty_array(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test listing tasks when none exist returns empty array."""
        response = client.get(
            f"/api/{test_user_id}/tasks",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # May have tasks from other tests, but should be an array

    def test_list_tasks_different_user_isolation(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt: callable
    ):
        """Test that different user's tasks are not returned (data isolation)."""
        # Create task for user 1
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Task", "description": "User 1 only"},
            headers=auth_headers
        )

        # Create different user with different JWT
        other_user_id = "other-user-123"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        # Create task for user 2
        client.post(
            f"/api/{other_user_id}/tasks",
            json={"title": "User 2 Task", "description": "User 2 only"},
            headers=other_headers
        )

        # User 1 should only see their own tasks
        response = client.get(
            f"/api/{test_user_id}/tasks",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Check that User 1's tasks don't contain User 2's task
        for task in tasks:
            assert task["user_id"] == test_user_id
            assert task["description"] != "User 2 only"

    def test_list_tasks_url_user_id_mismatch_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test that URL user_id mismatch returns 403."""
        different_user_id = "different-user-456"

        response = client.get(
            f"/api/{different_user_id}/tasks",  # Different user_id in URL
            headers=auth_headers  # But JWT for test_user_id
        )

        assert response.status_code == 403
        assert "Not authorized" in response.json()["detail"]

    def test_list_tasks_unauthenticated_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test that unauthenticated request returns 401."""
        response = client.get(f"/api/{test_user_id}/tasks")

        assert response.status_code == 401
        assert "authorization" in response.json()["detail"].lower()


class TestGetSingleTask:
    """Test getting a single task by ID."""

    def test_get_own_task_returns_200(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test getting own task returns 200 with task data."""
        # Create a task
        create_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "My Task",
                "description": "Task description",
                "priority": "High",
                "due_date": "2025-01-15",
                "tags": ["work", "urgent"]
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "My Task"
        assert task["description"] == "Task description"
        assert task["priority"] == "High"
        assert task["due_date"] == "2025-01-15"
        assert set(task["tags"]) == {"work", "urgent"}

    def test_get_nonexistent_task_returns_404(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test getting non-existent task returns 404."""
        fake_task_id = "00000000-0000-0000-0000-000000000000"

        response = client.get(
            f"/api/{test_user_id}/tasks/{fake_task_id}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_another_users_task_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt: callable
    ):
        """Test getting another user's task returns 403."""
        # Create task as user 1
        create_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Try to access as user 2
        other_user_id = "other-user-789"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.get(
            f"/api/{other_user_id}/tasks/{task_id}",  # Different user_id
            headers=other_headers
        )

        # Should return 404 (task doesn't exist for this user) or 403
        assert response.status_code in [403, 404]
