"""Integration Tests for Tags Endpoint

Tests for viewing tags with usage counts via GET /api/{user_id}/tags.
"""

import pytest
from fastapi.testclient import TestClient


class TestTagsEndpoint:
    """Test tags endpoint for autocomplete and tag management."""

    def test_get_tags_returns_all_user_tags_with_usage_counts(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test GET /tags returns all user's unique tags with usage counts."""
        # Create tasks with various tags
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 1", "tags": ["work", "urgent"]},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 2", "tags": ["work", "meeting"]},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 3", "tags": ["personal"]},
            headers=auth_headers
        )

        # Get tags
        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()
        assert isinstance(tags, list)

        # Find specific tags and check usage counts
        work_tag = next((t for t in tags if t["name"] == "work"), None)
        urgent_tag = next((t for t in tags if t["name"] == "urgent"), None)
        meeting_tag = next((t for t in tags if t["name"] == "meeting"), None)
        personal_tag = next((t for t in tags if t["name"] == "personal"), None)

        assert work_tag is not None
        assert work_tag["usage_count"] == 2  # Used in Task 1 and Task 2

        assert urgent_tag is not None
        assert urgent_tag["usage_count"] == 1  # Used in Task 1

        assert meeting_tag is not None
        assert meeting_tag["usage_count"] == 1  # Used in Task 2

        assert personal_tag is not None
        assert personal_tag["usage_count"] == 1  # Used in Task 3

    def test_get_tags_different_users_isolated(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test tags from different users are not returned (data isolation)."""
        # Create task as test_user
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Task", "tags": ["user1-tag"]},
            headers=auth_headers
        )

        # Create task as another user
        other_user_id = "other-user-def"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        client.post(
            f"/api/{other_user_id}/tasks",
            json={"title": "User 2 Task", "tags": ["user2-tag"]},
            headers=other_headers
        )

        # Get tags for test_user
        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()
        tag_names = [t["name"] for t in tags]

        # Should only see user1-tag, not user2-tag
        assert "user1-tag" in tag_names
        assert "user2-tag" not in tag_names

    def test_get_tags_usage_count_accurate(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test usage count is accurate (counts tasks associated with each tag)."""
        # Create multiple tasks with overlapping tags
        for i in range(5):
            client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Task {i+1}", "tags": ["common-tag"]},
                headers=auth_headers
            )

        # Create one task with a different tag
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Unique Task", "tags": ["rare-tag"]},
            headers=auth_headers
        )

        # Get tags
        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()

        common_tag = next((t for t in tags if t["name"] == "common-tag"), None)
        rare_tag = next((t for t in tags if t["name"] == "rare-tag"), None)

        assert common_tag is not None
        assert common_tag["usage_count"] == 5

        assert rare_tag is not None
        assert rare_tag["usage_count"] == 1

    def test_get_tags_empty_list_for_user_with_no_tasks(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test empty tag list returns [] for user with no tasks."""
        # Don't create any tasks

        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()
        assert tags == []

    def test_get_tags_sorted_by_name_alphabetically(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test tags are sorted by name alphabetically."""
        # Create tasks with tags in random order
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task 1", "tags": ["zebra", "alpha", "mike"]},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()
        tag_names = [t["name"] for t in tags]

        # Check alphabetical order
        assert tag_names == sorted(tag_names)

    def test_get_tags_unauthenticated_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test unauthenticated request returns 401."""
        response = client.get(f"/api/{test_user_id}/tags")

        assert response.status_code == 401

    def test_get_tags_wrong_user_id_returns_403(
        self, client: TestClient, test_user_id: str, generate_test_jwt
    ):
        """Test wrong user_id in URL returns 403."""
        # Try to get tags for test_user_id but with a different user's token
        other_user_id = "other-user-ghi"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.get(
            f"/api/{test_user_id}/tags",  # URL has test_user_id
            headers=other_headers  # But token is for other_user_id
        )

        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_get_tags_after_task_deletion(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test tag usage count updates when task is deleted."""
        # Create task with tag
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "tags": ["deletable-tag"]},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Verify tag exists with usage_count = 1
        response1 = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )
        tags1 = response1.json()
        tag1 = next((t for t in tags1 if t["name"] == "deletable-tag"), None)
        assert tag1 is not None
        assert tag1["usage_count"] == 1

        # Delete the task
        client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers
        )

        # Check tags again - should have usage_count = 0 or not appear
        response2 = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )
        tags2 = response2.json()
        tag2 = next((t for t in tags2 if t["name"] == "deletable-tag"), None)

        # Tag might still exist but with usage_count = 0, or be excluded from results
        if tag2 is not None:
            assert tag2["usage_count"] == 0

    def test_get_tags_with_duplicate_tags_on_same_task(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test duplicate tags on same task are counted only once."""
        # Create task with duplicate tags (should be deduplicated)
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "tags": ["dup", "dup", "dup"]},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()
        dup_tag = next((t for t in tags if t["name"] == "dup"), None)

        assert dup_tag is not None
        # Should count as 1 task, not 3
        assert dup_tag["usage_count"] == 1

    def test_get_tags_returns_correct_schema(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test tags endpoint returns correct schema (TagWithUsage)."""
        # Create task with tag
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "tags": ["sample-tag"]},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tags",
            headers=auth_headers
        )

        assert response.status_code == 200
        tags = response.json()
        assert len(tags) > 0

        # Check schema of first tag
        tag = tags[0]
        assert "name" in tag
        assert "usage_count" in tag
        assert isinstance(tag["name"], str)
        assert isinstance(tag["usage_count"], int)
        assert tag["usage_count"] >= 0
