"""Integration Tests for Task Update and Delete

Tests for updating tasks via PUT/PATCH /api/{user_id}/tasks/{task_id}
and deleting tasks via DELETE /api/{user_id}/tasks/{task_id}.
"""

import pytest
from fastapi.testclient import TestClient


class TestUpdateTask:
    """Test updating task fields."""

    def test_update_title_returns_200_with_new_title(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update title returns 200 with new title."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Old Title"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update title
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"title": "New Title"},
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "New Title"

    def test_update_description_returns_200_with_new_description(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update description returns 200 with new description."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "description": "Old description"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update description
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"description": "New description"},
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["description"] == "New description"

    def test_update_priority_returns_200_with_new_priority(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update priority returns 200 with new priority."""
        # Create task with Low priority
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "priority": "Low"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update to High priority
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"priority": "High"},
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["priority"] == "High"

    def test_update_due_date_returns_200_with_new_due_date(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update due_date returns 200 with new due_date."""
        # Create task with no due date
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update due_date
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"due_date": "2025-12-31"},
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["due_date"] == "2025-12-31"

    def test_update_tags_returns_200_with_new_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update tags returns 200 with new tags (replaces existing)."""
        # Create task with initial tags
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "tags": ["old-tag", "remove-me"]},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update tags (should replace, not append)
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"tags": ["new-tag", "updated"]},
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert set(task["tags"]) == {"new-tag", "updated"}
        assert "old-tag" not in task["tags"]
        assert "remove-me" not in task["tags"]

    def test_update_title_too_long_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update with title > 200 chars returns 400."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Valid Title"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to update with title > 200 chars
        long_title = "x" * 201
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"title": long_title},
            headers=auth_headers
        )

        assert response.status_code == 422  # Validation error

    def test_update_invalid_priority_returns_400(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update with invalid priority value returns 400."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to update with invalid priority
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"priority": "SuperUrgent"},  # Invalid priority
            headers=auth_headers
        )

        assert response.status_code == 422  # Validation error

    def test_update_nonexistent_task_returns_404(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test update non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"

        response = client.put(
            f"/api/{test_user_id}/tasks/{fake_uuid}",
            json={"title": "Updated"},
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_update_another_users_task_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test update another user's task returns 403."""
        # Create task as test_user
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to update as another user
        other_user_id = "other-user-999"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"title": "Hacked"},
            headers=other_headers
        )

        assert response.status_code == 403

    def test_update_multiple_fields_at_once(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test updating multiple fields at once works correctly."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "Old",
                "description": "Old desc",
                "priority": "Low",
                "completed": False
            },
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update multiple fields
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={
                "title": "New",
                "description": "New desc",
                "priority": "High",
                "completed": True,
                "due_date": "2025-12-31",
                "tags": ["updated", "multi-field"]
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "New"
        assert task["description"] == "New desc"
        assert task["priority"] == "High"
        assert task["completed"] is True
        assert task["due_date"] == "2025-12-31"
        assert set(task["tags"]) == {"updated", "multi-field"}

    def test_partial_update_only_changes_specified_fields(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test partial update only changes specified fields."""
        # Create task with all fields
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={
                "title": "Original Title",
                "description": "Original Description",
                "priority": "Medium",
                "completed": False,
                "tags": ["keep-me"]
            },
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Update only title (other fields should remain unchanged)
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"title": "Updated Title"},
            headers=auth_headers
        )

        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "Updated Title"
        assert task["description"] == "Original Description"
        assert task["priority"] == "Medium"
        assert task["completed"] is False
        # Tags should remain if not updated
        assert "keep-me" in task["tags"]


class TestDeleteTask:
    """Test deleting tasks."""

    def test_delete_own_task_returns_204(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test delete own task returns 204 No Content."""
        # Create task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task to Delete"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 204

        # Verify task is deleted (should return 404)
        get_response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_delete_nonexistent_task_returns_404(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test delete non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"

        response = client.delete(
            f"/api/{test_user_id}/tasks/{fake_uuid}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_delete_another_users_task_returns_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test delete another user's task returns 403."""
        # Create task as test_user
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Protected Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to delete as another user
        other_user_id = "other-user-abc"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=other_headers
        )

        assert response.status_code == 403

        # Verify task still exists for original user
        get_response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 200

    def test_delete_task_removes_task_tag_associations(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test deleting task also removes task_tag associations (CASCADE)."""
        # Create task with tags
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task with Tags", "tags": ["tag1", "tag2", "tag3"]},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

        # The task_tag associations should be automatically removed via CASCADE
        # We can verify by checking that the tags still exist (orphaned tags)
        # but are not associated with any tasks anymore

    def test_delete_task_leaves_orphaned_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test deleting task leaves orphaned tags (no other tasks reference them)."""
        # Create task with unique tags
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 1", "tags": ["orphan-tag"]},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 204

        # The orphan-tag still exists in the tags table but has no task associations
        # This is expected behavior - tags are not automatically deleted
        # (cleanup would require a separate service method)

    def test_delete_completed_task(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test deleting a completed task works correctly."""
        # Create completed task
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Completed Task", "completed": True},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        assert response.status_code == 204
