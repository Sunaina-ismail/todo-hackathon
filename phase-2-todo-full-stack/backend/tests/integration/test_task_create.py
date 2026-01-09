"""Integration Tests for Task Creation

Tests for POST /api/{user_id}/tasks endpoint with authentication and validation.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import date
from src.models.task import PriorityType


class TestCreateTask:
    """Test task creation endpoint with priority, due_date, and tags."""

    def test_create_task_with_all_fields_returns_201(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with all fields returns 201 Created."""
        task_data = {
            "title": "Buy groceries",
            "description": "Milk, bread, eggs, butter",
            "priority": "High",
            "due_date": "2025-01-15",
            "tags": ["shopping", "urgent"]
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, bread, eggs, butter"
        assert data["priority"] == "High"
        assert data["due_date"] == "2025-01-15"
        assert data["completed"] is False
        assert data["user_id"] == test_user_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert set(data["tags"]) == {"shopping", "urgent"}

    def test_create_task_with_minimal_fields_returns_201(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with only required title field."""
        task_data = {
            "title": "Simple task"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["priority"] == "Medium"  # Default priority
        assert data["due_date"] is None
        assert data["completed"] is False
        assert data["tags"] == []

    def test_create_task_with_priority_medium(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with Medium priority."""
        task_data = {
            "title": "Medium priority task",
            "priority": "Medium"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["priority"] == "Medium"

    def test_create_task_with_priority_low(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with Low priority."""
        task_data = {
            "title": "Low priority task",
            "priority": "Low"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["priority"] == "Low"

    def test_create_task_with_due_date(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with due date."""
        task_data = {
            "title": "Task with due date",
            "due_date": "2025-12-31"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["due_date"] == "2025-12-31"

    def test_create_task_with_single_tag(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with a single tag."""
        task_data = {
            "title": "Task with tag",
            "tags": ["work"]
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["tags"] == ["work"]

    def test_create_task_with_multiple_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with multiple tags."""
        task_data = {
            "title": "Task with multiple tags",
            "tags": ["work", "urgent", "important"]
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert set(response.json()["tags"]) == {"work", "urgent", "important"}

    def test_create_task_tags_properly_associated(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test that tags are properly associated with created task."""
        task_data = {
            "title": "Task for tag association test",
            "tags": ["test-tag-1", "test-tag-2"]
        }

        # Create task
        create_response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Retrieve task to verify tags
        get_response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 200
        assert set(get_response.json()["tags"]) == {"test-tag-1", "test-tag-2"}


class TestCreateTaskValidation:
    """Test task creation validation errors."""

    def test_create_task_missing_title_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task without title returns 400 Bad Request."""
        task_data = {
            "description": "Task without title"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # FastAPI validation error
        assert "title" in response.text.lower()

    def test_create_task_empty_title_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with empty title returns 400 Bad Request."""
        task_data = {
            "title": ""
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Pydantic validation error
        assert "title" in response.text.lower()

    def test_create_task_title_exceeds_max_length_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with title > 200 chars returns 400."""
        task_data = {
            "title": "A" * 201  # 201 characters
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Pydantic validation error
        assert "title" in response.text.lower()

    def test_create_task_description_exceeds_max_length_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with description > 1000 chars returns 400."""
        task_data = {
            "title": "Valid title",
            "description": "B" * 1001  # 1001 characters
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Pydantic validation error
        assert "description" in response.text.lower()

    def test_create_task_invalid_priority_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with invalid priority value returns 400."""
        task_data = {
            "title": "Task with invalid priority",
            "priority": "VeryHigh"  # Invalid priority
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Pydantic validation error
        assert "priority" in response.text.lower()

    def test_create_task_invalid_due_date_format_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with invalid due_date format returns 400."""
        task_data = {
            "title": "Task with invalid due date",
            "due_date": "invalid-date"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Pydantic validation error

    def test_create_task_due_date_wrong_format_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with wrong date format returns 400."""
        task_data = {
            "title": "Task with wrong date format",
            "due_date": "01/15/2025"  # Should be YYYY-MM-DD
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Pydantic validation error


class TestCreateTaskAuthentication:
    """Test task creation authentication and authorization."""

    def test_create_task_unauthenticated_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test creating a task without authentication returns 401 Unauthorized."""
        task_data = {
            "title": "Unauthenticated task"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data
            # No auth headers
        )

        assert response.status_code == 401

    def test_create_task_invalid_token_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test creating a task with invalid JWT token returns 401."""
        task_data = {
            "title": "Task with invalid token"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401

    def test_create_task_user_id_mismatch_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task for different user_id returns 403 Forbidden."""
        task_data = {
            "title": "Task for different user"
        }

        # Try to create task for different user
        different_user_id = "different-user-456"
        response = client.post(
            f"/api/{different_user_id}/tasks",
            json=task_data,
            headers=auth_headers  # Token is for test_user_id
        )

        assert response.status_code == 403
        assert "not authorized" in response.text.lower()


class TestCreateTaskEdgeCases:
    """Test edge cases for task creation."""

    def test_create_task_with_exact_max_title_length(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with exactly 200 character title."""
        task_data = {
            "title": "A" * 200
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert len(response.json()["title"]) == 200

    def test_create_task_with_exact_max_description_length(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with exactly 1000 character description."""
        task_data = {
            "title": "Task with max description",
            "description": "B" * 1000
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert len(response.json()["description"]) == 1000

    def test_create_task_with_empty_tags_list(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with empty tags list."""
        task_data = {
            "title": "Task with empty tags",
            "tags": []
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["tags"] == []

    def test_create_task_with_duplicate_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with duplicate tags (should deduplicate)."""
        task_data = {
            "title": "Task with duplicate tags",
            "tags": ["work", "urgent", "work", "urgent"]
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        # Tags should be deduplicated
        tags = response.json()["tags"]
        assert len(tags) == 2
        assert set(tags) == {"work", "urgent"}

    def test_create_task_with_special_characters_in_title(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with special characters in title."""
        task_data = {
            "title": "Task with special chars: @#$%^&*()!?"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["title"] == "Task with special chars: @#$%^&*()!?"

    def test_create_task_with_unicode_in_title(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test creating a task with unicode characters in title."""
        task_data = {
            "title": "Task with unicode: 你好 🎉 مرحبا"
        }

        response = client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["title"] == "Task with unicode: 你好 🎉 مرحبا"
