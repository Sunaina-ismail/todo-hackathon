"""Integration Tests for Task Toggle Completion

Tests for toggling task completion status via PATCH /api/{user_id}/tasks/{task_id}/complete.
"""

import pytest
from fastapi.testclient import TestClient


class TestToggleTaskCompletion:
    """Test toggling task completion status."""

    def test_toggle_pending_to_complete(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test toggle pending task to complete returns 200 with completed=true."""
        # Create a pending task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Pending Task", "completed": False},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Toggle to complete
        response = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["completed"] is True
        assert task["title"] == "Pending Task"

    def test_toggle_complete_to_pending(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test toggle complete task to pending returns 200 with completed=false."""
        # Create a completed task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Completed Task", "completed": True},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Toggle to pending
        response = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["completed"] is False
        assert task["title"] == "Completed Task"

    def test_toggle_nonexistent_task_returns_404(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test toggle non-existent task returns 404."""
        # Use a random UUID that doesn't exist
        fake_uuid = "00000000-0000-0000-0000-000000000000"

        response = client.patch(
            f"/api/{test_user_id}/tasks/{fake_uuid}/complete",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_toggle_another_users_task_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test toggle another user's task returns 403."""
        # Create task as test_user
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to toggle as another user
        other_user_id = "other-user-456"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=other_headers
        )

        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_toggle_returns_task_with_all_fields(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test toggle returns task with priority, due_date, tags."""
        # Create task with all fields
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "Full Task",
                "description": "With all fields",
                "priority": "High",
                "due_date": "2025-12-31",
                "tags": ["urgent", "work"],
                "completed": False
            },
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Toggle completion
        response = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["completed"] is True
        assert task["priority"] == "High"
        assert task["due_date"] == "2025-12-31"
        assert "urgent" in task["tags"]
        assert "work" in task["tags"]

    def test_toggle_updates_timestamp(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test toggle updates the updated_at timestamp."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task to Toggle"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]
        original_updated_at = task_response.json()["updated_at"]

        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.1)

        # Toggle completion
        response = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        # updated_at should be different (newer)
        assert task["updated_at"] != original_updated_at

    def test_toggle_multiple_times(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test toggling a task multiple times works correctly."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Toggle Me", "completed": False},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # First toggle (pending -> complete)
        response1 = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )
        assert response1.status_code == 200
        assert response1.json()["completed"] is True

        # Second toggle (complete -> pending)
        response2 = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )
        assert response2.status_code == 200
        assert response2.json()["completed"] is False

        # Third toggle (pending -> complete again)
        response3 = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers
        )
        assert response3.status_code == 200
        assert response3.json()["completed"] is True
