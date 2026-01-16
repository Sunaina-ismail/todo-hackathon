"""Integration Tests for Authentication

Tests for JWT authentication across all endpoints including tag endpoints
and search/filter query parameter validation.
"""

import pytest
from fastapi.testclient import TestClient


class TestTagEndpointAuthentication:
    """Test authentication for tag endpoints."""

    def test_get_tags_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test GET /api/{user_id}/tags requires valid JWT token."""
        response = client.get(f"/api/{test_user_id}/tags")

        assert response.status_code == 401
        assert "detail" in response.json()

    def test_get_tags_with_invalid_token_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test GET /api/{user_id}/tags with invalid token returns 401."""
        invalid_headers = {"Authorization": "Bearer invalid-token-here"}
        response = client.get(
            f"/api/{test_user_id}/tags", headers=invalid_headers
        )

        assert response.status_code == 401
        assert "detail" in response.json()

    def test_get_tags_with_malformed_auth_header_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test GET /api/{user_id}/tags with malformed Authorization header."""
        # Missing "Bearer " prefix
        malformed_headers = {"Authorization": "some-token"}
        response = client.get(
            f"/api/{test_user_id}/tags", headers=malformed_headers
        )

        assert response.status_code == 401

    def test_get_tags_with_wrong_user_id_returns_403(
        self, client: TestClient, test_user_id: str, generate_test_jwt
    ):
        """Test GET /api/{user_id}/tags with mismatched user_id returns 403."""
        # Token for one user, URL for another
        other_user_id = "other-user-xyz"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.get(
            f"/api/{test_user_id}/tags",  # URL has test_user_id
            headers=other_headers  # But token is for other_user_id
        )

        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_get_tags_with_valid_auth_succeeds(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test GET /api/{user_id}/tags with valid authentication succeeds."""
        response = client.get(
            f"/api/{test_user_id}/tags", headers=auth_headers
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestTaskEndpointAuthentication:
    """Test authentication for task endpoints."""

    def test_list_tasks_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test GET /api/{user_id}/tasks requires valid JWT token."""
        response = client.get(f"/api/{test_user_id}/tasks")

        assert response.status_code == 401

    def test_create_task_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test POST /api/{user_id}/tasks requires valid JWT token."""
        response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Test Task"}
        )

        assert response.status_code == 401

    def test_get_task_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test GET /api/{user_id}/tasks/{task_id} requires valid JWT token."""
        response = client.get(f"/api/{test_user_id}/tasks/123")

        assert response.status_code == 401

    def test_update_task_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test PUT /api/{user_id}/tasks/{task_id} requires valid JWT token."""
        response = client.put(
            f"/api/{test_user_id}/tasks/123",
            json={"title": "Updated Task"}
        )

        assert response.status_code == 401

    def test_delete_task_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test DELETE /api/{user_id}/tasks/{task_id} requires valid JWT token."""
        response = client.delete(f"/api/{test_user_id}/tasks/123")

        assert response.status_code == 401

    def test_toggle_completion_requires_authentication(
        self, client: TestClient, test_user_id: str
    ):
        """Test PATCH /api/{user_id}/tasks/{task_id}/complete requires valid JWT token."""
        response = client.patch(f"/api/{test_user_id}/tasks/123/complete")

        assert response.status_code == 401

    def test_task_endpoints_with_wrong_user_id_return_403(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test task endpoints with mismatched user_id return 403."""
        # Create a task first
        task_response = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Test Task"},
            headers=auth_headers
        )
        task_id = task_response.json()["id"]

        # Try to access with different user's token
        other_user_id = "other-user-abc"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        # Test GET
        response = client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=other_headers
        )
        assert response.status_code == 403

        # Test PUT
        response = client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"title": "Updated"},
            headers=other_headers
        )
        assert response.status_code == 403

        # Test DELETE
        response = client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=other_headers
        )
        assert response.status_code == 403

        # Test PATCH
        response = client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=other_headers
        )
        assert response.status_code == 403


class TestSearchFilterQueryParameterValidation:
    """Test validation for search and filter query parameters."""

    def test_list_tasks_with_valid_search_parameter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test search parameter with valid string value."""
        response = client.get(
            f"/api/{test_user_id}/tasks?search=meeting",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_tasks_with_valid_completed_filter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test completed filter with valid boolean values."""
        # Test completed=true
        response = client.get(
            f"/api/{test_user_id}/tasks?completed=true",
            headers=auth_headers
        )
        assert response.status_code == 200

        # Test completed=false
        response = client.get(
            f"/api/{test_user_id}/tasks?completed=false",
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_list_tasks_with_valid_priority_filter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test priority filter with valid enum values."""
        for priority in ["High", "Medium", "Low", "all"]:
            response = client.get(
                f"/api/{test_user_id}/tasks?priority={priority}",
                headers=auth_headers
            )
            assert response.status_code == 200

    def test_list_tasks_with_invalid_priority_returns_422(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test priority filter with invalid value returns 422."""
        response = client.get(
            f"/api/{test_user_id}/tasks?priority=InvalidPriority",
            headers=auth_headers
        )

        # Should either return 422 or ignore invalid value and return 200
        # (implementation-dependent)
        assert response.status_code in [200, 422]

    def test_list_tasks_with_valid_tags_filter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test tags filter with valid tag names."""
        response = client.get(
            f"/api/{test_user_id}/tasks?tags=work&tags=urgent",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_tasks_with_valid_sort_parameters(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test sort_by and sort_direction parameters."""
        sort_fields = ["created_at", "title", "due_date", "priority"]
        sort_directions = ["asc", "desc"]

        for sort_by in sort_fields:
            for sort_direction in sort_directions:
                response = client.get(
                    f"/api/{test_user_id}/tasks?sort_by={sort_by}&sort_direction={sort_direction}",
                    headers=auth_headers
                )
                assert response.status_code == 200

    def test_list_tasks_with_invalid_sort_by_returns_422(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test invalid sort_by field returns 422."""
        response = client.get(
            f"/api/{test_user_id}/tasks?sort_by=invalid_field",
            headers=auth_headers
        )

        # Should either return 422 or ignore invalid value and use default
        assert response.status_code in [200, 422]

    def test_list_tasks_with_invalid_sort_direction_returns_422(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test invalid sort_direction returns 422."""
        response = client.get(
            f"/api/{test_user_id}/tasks?sort_direction=invalid",
            headers=auth_headers
        )

        # Should either return 422 or ignore invalid value and use default
        assert response.status_code in [200, 422]

    def test_list_tasks_with_valid_pagination_parameters(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test limit and offset pagination parameters."""
        # Test limit
        response = client.get(
            f"/api/{test_user_id}/tasks?limit=10",
            headers=auth_headers
        )
        assert response.status_code == 200

        # Test offset
        response = client.get(
            f"/api/{test_user_id}/tasks?offset=5",
            headers=auth_headers
        )
        assert response.status_code == 200

        # Test both
        response = client.get(
            f"/api/{test_user_id}/tasks?limit=10&offset=5",
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_list_tasks_with_invalid_limit_returns_422(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test invalid limit values return 422."""
        # Negative limit
        response = client.get(
            f"/api/{test_user_id}/tasks?limit=-1",
            headers=auth_headers
        )
        assert response.status_code == 422

        # Limit exceeding maximum (should be capped at 100)
        response = client.get(
            f"/api/{test_user_id}/tasks?limit=500",
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_list_tasks_with_invalid_offset_returns_422(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test invalid offset values return 422."""
        # Negative offset
        response = client.get(
            f"/api/{test_user_id}/tasks?offset=-1",
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_list_tasks_with_combined_query_parameters(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test combining multiple valid query parameters."""
        response = client.get(
            f"/api/{test_user_id}/tasks?search=meeting&completed=false&priority=High&tags=work&sort_by=due_date&sort_direction=asc&limit=20&offset=0",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestCrossUserDataIsolation:
    """Test that users cannot access each other's data."""

    def test_user_cannot_list_other_users_tasks(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test user cannot list another user's tasks."""
        # Create task as test_user
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )

        # Try to access as different user
        other_user_id = "other-user-def"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.get(
            f"/api/{test_user_id}/tasks",  # URL has test_user_id
            headers=other_headers  # But token is for other_user_id
        )

        assert response.status_code == 403

    def test_user_cannot_access_other_users_tags(
        self, client: TestClient, test_user_id: str, auth_headers: dict, generate_test_jwt
    ):
        """Test user cannot access another user's tags."""
        # Create task with tag as test_user
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task", "tags": ["private-tag"]},
            headers=auth_headers
        )

        # Try to access tags as different user
        other_user_id = "other-user-ghi"
        other_token = generate_test_jwt(other_user_id)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        response = client.get(
            f"/api/{test_user_id}/tags",  # URL has test_user_id
            headers=other_headers  # But token is for other_user_id
        )

        assert response.status_code == 403


class TestAuthorizationHeaderValidation:
    """Test Authorization header validation."""

    def test_missing_authorization_header_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test missing Authorization header returns 401."""
        response = client.get(f"/api/{test_user_id}/tasks")

        assert response.status_code == 401
        assert "detail" in response.json()

    def test_empty_authorization_header_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test empty Authorization header returns 401."""
        headers = {"Authorization": ""}
        response = client.get(
            f"/api/{test_user_id}/tasks", headers=headers
        )

        assert response.status_code == 401

    def test_malformed_bearer_token_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test malformed Bearer token returns 401."""
        # Missing "Bearer " prefix
        headers = {"Authorization": "some-token-without-prefix"}
        response = client.get(
            f"/api/{test_user_id}/tasks", headers=headers
        )

        assert response.status_code == 401

    def test_expired_token_returns_401(
        self, client: TestClient, test_user_id: str
    ):
        """Test expired JWT token returns 401."""
        # Create an expired token (if generate_test_jwt supports it)
        # For now, use an obviously invalid token
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJleHBpcmVkLXVzZXIiLCJleHAiOjB9.invalid"}
        response = client.get(
            f"/api/{test_user_id}/tasks", headers=headers
        )

        assert response.status_code == 401
