"""Integration Tests for ChatKit API Endpoint

Tests for ChatKit REST API with JWT authentication, database persistence,
and agent integration. Uses real database (test database) for integration testing.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
from agents import Runner

from src.main import app


# Mock RunResult for testing
class MockRunResult:
    """Mock RunResult for testing agent responses."""
    def __init__(self, messages=None, final_output=""):
        self.messages = messages or []
        self.final_output = final_output


# Mock Message for testing
class MockMessage:
    """Mock Message for testing agent responses."""
    def __init__(self, role, content):
        self.role = role
        self.content = content


class TestCreateThread:
    """Test POST /api/chatkit/threads endpoint."""

    def test_create_thread_success(self, client: TestClient, auth_headers: dict):
        """Test successful thread creation with JWT authentication."""
        response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Conversation"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Conversation"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_thread_default_title(self, client: TestClient, auth_headers: dict):
        """Test thread creation with default title."""
        response = client.post(
            "/api/chatkit/threads",
            json={},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Conversation"

    def test_create_thread_no_auth(self, client: TestClient):
        """Test thread creation without JWT token returns 401."""
        response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Conversation"},
        )

        assert response.status_code == 401

    def test_create_thread_invalid_token(self, client: TestClient):
        """Test thread creation with invalid JWT token returns 403."""
        response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Conversation"},
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 403


class TestGetThread:
    """Test GET /api/chatkit/threads/{thread_id} endpoint."""

    def test_get_thread_success(self, client: TestClient, auth_headers: dict):
        """Test successful thread retrieval."""
        # Create thread first
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Conversation"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Get thread
        response = client.get(
            f"/api/chatkit/threads/{thread_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == thread_id
        assert data["title"] == "Test Conversation"

    def test_get_thread_not_found(self, client: TestClient, auth_headers: dict):
        """Test get thread with non-existent thread_id returns 404."""
        response = client.get(
            "/api/chatkit/threads/thread_nonexistent",
            headers=auth_headers,
        )

        assert response.status_code == 404

    def test_get_thread_no_auth(self, client: TestClient):
        """Test get thread without JWT token returns 401."""
        response = client.get("/api/chatkit/threads/thread_abc123")

        assert response.status_code == 401

    def test_get_thread_user_isolation(
        self, client: TestClient, generate_test_jwt
    ):
        """Test user cannot access another user's thread."""
        # User A creates thread
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "User A Thread"},
            headers=user_a_headers,
        )
        thread_id = create_response.json()["id"]

        # User B tries to access User A's thread
        user_b_token = generate_test_jwt("user-b")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        response = client.get(
            f"/api/chatkit/threads/{thread_id}",
            headers=user_b_headers,
        )

        assert response.status_code == 404


class TestGetMessages:
    """Test GET /api/chatkit/threads/{thread_id}/messages endpoint."""

    def test_get_messages_empty_thread(self, client: TestClient, auth_headers: dict):
        """Test get messages for thread with no messages."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Empty Thread"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Get messages
        response = client.get(
            f"/api/chatkit/threads/{thread_id}/messages",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_messages_with_messages(self, client: TestClient, auth_headers: dict):
        """Test get messages returns messages in order."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Thread"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock agent response
        mock_result = MockRunResult(
            messages=[
                MockMessage(role="assistant", content="Task created successfully!")
            ]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            # Send message
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_id,
                    "content": "Add a task to buy milk",
                },
                headers=auth_headers,
            )

        # Get messages
        response = client.get(
            f"/api/chatkit/threads/{thread_id}/messages",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # User message + assistant response
        assert data[0]["role"] == "user"
        assert data[0]["content"] == "Add a task to buy milk"
        assert data[1]["role"] == "assistant"
        assert data[1]["content"] == "Task created successfully!"

    def test_get_messages_thread_not_found(self, client: TestClient, auth_headers: dict):
        """Test get messages for non-existent thread returns 404."""
        response = client.get(
            "/api/chatkit/threads/thread_nonexistent/messages",
            headers=auth_headers,
        )

        assert response.status_code == 404

    def test_get_messages_no_auth(self, client: TestClient):
        """Test get messages without JWT token returns 401."""
        response = client.get("/api/chatkit/threads/thread_abc123/messages")

        assert response.status_code == 401


class TestSendMessage:
    """Test POST /api/chatkit/messages endpoint."""

    def test_send_message_success(self, client: TestClient, auth_headers: dict):
        """Test successful message sending with agent response."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Thread"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock agent response
        mock_result = MockRunResult(
            messages=[
                MockMessage(role="assistant", content="Task created successfully!")
            ]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            # Send message
            response = client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_id,
                    "content": "Add a task to buy milk",
                },
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "assistant"
        assert data["content"] == "Task created successfully!"
        assert data["thread_id"] == thread_id

    def test_send_message_thread_not_found(self, client: TestClient, auth_headers: dict):
        """Test send message to non-existent thread returns 404."""
        response = client.post(
            "/api/chatkit/messages",
            json={
                "thread_id": "thread_nonexistent",
                "content": "Test message",
            },
            headers=auth_headers,
        )

        assert response.status_code == 404

    def test_send_message_no_auth(self, client: TestClient):
        """Test send message without JWT token returns 401."""
        response = client.post(
            "/api/chatkit/messages",
            json={
                "thread_id": "thread_abc123",
                "content": "Test message",
            },
        )

        assert response.status_code == 401

    def test_send_message_empty_content(self, client: TestClient, auth_headers: dict):
        """Test send message with empty content returns 422."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Test Thread"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Send empty message
        response = client.post(
            "/api/chatkit/messages",
            json={
                "thread_id": thread_id,
                "content": "",
            },
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_send_message_agent_integration(self, client: TestClient, auth_headers: dict):
        """Test message sending integrates with agent and MCP tools."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Agent Test"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock agent response with tool call
        mock_result = MockRunResult(
            messages=[
                MockMessage(
                    role="assistant",
                    content="I've created a task 'Buy milk' with medium priority.",
                )
            ]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            response = client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_id,
                    "content": "Add a task to buy milk",
                },
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert "created a task" in data["content"].lower()

    def test_send_message_conversation_history(
        self, client: TestClient, auth_headers: dict
    ):
        """Test conversation history is maintained across messages."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "History Test"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock agent responses
        mock_result_1 = MockRunResult(
            messages=[MockMessage(role="assistant", content="First response")]
        )
        mock_result_2 = MockRunResult(
            messages=[MockMessage(role="assistant", content="Second response")]
        )

        with patch.object(Runner, "run", side_effect=[mock_result_1, mock_result_2]):
            # Send first message
            client.post(
                "/api/chatkit/messages",
                json={"thread_id": thread_id, "content": "First message"},
                headers=auth_headers,
            )

            # Send second message
            client.post(
                "/api/chatkit/messages",
                json={"thread_id": thread_id, "content": "Second message"},
                headers=auth_headers,
            )

        # Get messages
        response = client.get(
            f"/api/chatkit/threads/{thread_id}/messages",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4  # 2 user messages + 2 assistant responses
        assert data[0]["content"] == "First message"
        assert data[1]["content"] == "First response"
        assert data[2]["content"] == "Second message"
        assert data[3]["content"] == "Second response"


class TestListThreads:
    """Test GET /api/chatkit/threads endpoint."""

    def test_list_threads_empty(self, client: TestClient, auth_headers: dict):
        """Test list threads returns empty list for new user."""
        response = client.get(
            "/api/chatkit/threads",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_threads_with_threads(self, client: TestClient, auth_headers: dict):
        """Test list threads returns user's threads."""
        # Create multiple threads
        thread_ids = []
        for i in range(3):
            create_response = client.post(
                "/api/chatkit/threads",
                json={"title": f"Thread {i+1}"},
                headers=auth_headers,
            )
            thread_ids.append(create_response.json()["id"])

        # List threads
        response = client.get(
            "/api/chatkit/threads",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(thread["id"] in thread_ids for thread in data)

    def test_list_threads_ordered_by_updated_at(
        self, client: TestClient, auth_headers: dict
    ):
        """Test list threads returns threads ordered by updated_at DESC."""
        # Create threads
        thread1_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Thread 1"},
            headers=auth_headers,
        )
        thread1_id = thread1_response.json()["id"]

        thread2_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Thread 2"},
            headers=auth_headers,
        )
        thread2_id = thread2_response.json()["id"]

        # Send message to thread 1 (updates its updated_at)
        mock_result = MockRunResult(
            messages=[MockMessage(role="assistant", content="Response")]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            client.post(
                "/api/chatkit/messages",
                json={"thread_id": thread1_id, "content": "Test message"},
                headers=auth_headers,
            )

        # List threads
        response = client.get(
            "/api/chatkit/threads",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        # Thread 1 should be first (most recently updated)
        assert data[0]["id"] == thread1_id
        assert data[1]["id"] == thread2_id

    def test_list_threads_limit(self, client: TestClient, auth_headers: dict):
        """Test list threads respects limit parameter."""
        # Create 5 threads
        for i in range(5):
            client.post(
                "/api/chatkit/threads",
                json={"title": f"Thread {i+1}"},
                headers=auth_headers,
            )

        # List with limit=3
        response = client.get(
            "/api/chatkit/threads?limit=3",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_list_threads_no_auth(self, client: TestClient):
        """Test list threads without JWT token returns 401."""
        response = client.get("/api/chatkit/threads")

        assert response.status_code == 401

    def test_list_threads_user_isolation(self, client: TestClient, generate_test_jwt):
        """Test list threads only returns user's own threads."""
        # User A creates threads
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        client.post(
            "/api/chatkit/threads",
            json={"title": "User A Thread 1"},
            headers=user_a_headers,
        )
        client.post(
            "/api/chatkit/threads",
            json={"title": "User A Thread 2"},
            headers=user_a_headers,
        )

        # User B creates threads
        user_b_token = generate_test_jwt("user-b")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        client.post(
            "/api/chatkit/threads",
            json={"title": "User B Thread 1"},
            headers=user_b_headers,
        )

        # User A lists threads
        response_a = client.get(
            "/api/chatkit/threads",
            headers=user_a_headers,
        )

        # User B lists threads
        response_b = client.get(
            "/api/chatkit/threads",
            headers=user_b_headers,
        )

        assert response_a.status_code == 200
        assert response_b.status_code == 200

        data_a = response_a.json()
        data_b = response_b.json()

        # User A should see 2 threads
        assert len(data_a) == 2
        assert all("User A" in thread["title"] for thread in data_a)

        # User B should see 1 thread
        assert len(data_b) == 1
        assert "User B" in data_b[0]["title"]


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_json_body(self, client: TestClient, auth_headers: dict):
        """Test invalid JSON body returns 422."""
        response = client.post(
            "/api/chatkit/threads",
            data="invalid json",
            headers={**auth_headers, "Content-Type": "application/json"},
        )

        assert response.status_code == 422

    def test_missing_required_fields(self, client: TestClient, auth_headers: dict):
        """Test missing required fields returns 422."""
        response = client.post(
            "/api/chatkit/messages",
            json={"thread_id": "thread_abc123"},  # Missing content
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_agent_error_handling(self, client: TestClient, auth_headers: dict):
        """Test agent errors are handled gracefully."""
        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Error Test"},
            headers=auth_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock agent error
        with patch.object(Runner, "run", side_effect=Exception("Agent error")):
            response = client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_id,
                    "content": "Test message",
                },
                headers=auth_headers,
            )

        assert response.status_code == 500
        assert "Failed to send message" in response.json()["detail"]
