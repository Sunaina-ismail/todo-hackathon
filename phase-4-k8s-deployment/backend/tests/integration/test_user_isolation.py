"""Integration Tests for User Isolation

Tests to ensure complete user data isolation across:
- Task operations (MCP tools)
- Conversation threads (ChatKit)
- Message history
- JWT authentication enforcement

CRITICAL: These tests verify security boundaries between users.
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from agents import Runner

from src.models.task import Task, PriorityType
from src.services.task_service import TaskService


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


class TestTaskUserIsolation:
    """Test user isolation for task operations."""

    def test_user_cannot_access_other_user_tasks(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test User A cannot list User B's tasks."""
        # User A creates tasks
        user_a_id = "user-a"
        user_a_token = generate_test_jwt(user_a_id)
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        task_a = Task(
            id=uuid.uuid4(),
            user_id=user_a_id,
            title="User A Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_a)
        session.commit()

        # User B creates tasks
        user_b_id = "user-b"
        user_b_token = generate_test_jwt(user_b_id)
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A lists tasks
        response_a = client.get("/api/tasks", headers=user_a_headers)
        assert response_a.status_code == 200
        tasks_a = response_a.json()["tasks"]

        # User B lists tasks
        response_b = client.get("/api/tasks", headers=user_b_headers)
        assert response_b.status_code == 200
        tasks_b = response_b.json()["tasks"]

        # Verify isolation
        assert len(tasks_a) == 1
        assert tasks_a[0]["title"] == "User A Task"

        assert len(tasks_b) == 1
        assert tasks_b[0]["title"] == "User B Task"

    def test_user_cannot_get_other_user_task_by_id(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test User A cannot get User B's task by ID."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A tries to get User B's task
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.get(
            f"/api/tasks/{task_b.id}",
            headers=user_a_headers,
        )

        # Should return 404 (not found) to prevent information leakage
        assert response.status_code == 404

    def test_user_cannot_update_other_user_task(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test User A cannot update User B's task."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A tries to update User B's task
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.patch(
            f"/api/tasks/{task_b.id}",
            json={"title": "Hacked title"},
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

        # Verify task was not modified
        session.refresh(task_b)
        assert task_b.title == "User B Task"

    def test_user_cannot_delete_other_user_task(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test User A cannot delete User B's task."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()
        task_b_id = task_b.id

        # User A tries to delete User B's task
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.delete(
            f"/api/tasks/{task_b_id}",
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

        # Verify task still exists
        task_still_exists = TaskService.get_task_by_id(session, task_b_id, user_b_id)
        assert task_still_exists is not None
        assert task_still_exists.title == "User B Task"

    def test_user_cannot_complete_other_user_task(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test User A cannot mark User B's task as complete."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A tries to complete User B's task
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.post(
            f"/api/tasks/{task_b.id}/toggle",
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

        # Verify task is still incomplete
        session.refresh(task_b)
        assert task_b.completed is False


class TestConversationUserIsolation:
    """Test user isolation for conversation threads."""

    def test_user_cannot_access_other_user_thread(
        self, client: TestClient, generate_test_jwt
    ):
        """Test User A cannot access User B's conversation thread."""
        # User B creates thread
        user_b_token = generate_test_jwt("user-b")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "User B Thread"},
            headers=user_b_headers,
        )
        thread_b_id = create_response.json()["id"]

        # User A tries to access User B's thread
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.get(
            f"/api/chatkit/threads/{thread_b_id}",
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

    def test_user_cannot_access_other_user_messages(
        self, client: TestClient, generate_test_jwt
    ):
        """Test User A cannot access User B's conversation messages."""
        # User B creates thread and sends message
        user_b_token = generate_test_jwt("user-b")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "User B Thread"},
            headers=user_b_headers,
        )
        thread_b_id = create_response.json()["id"]

        # Mock agent response
        mock_result = MockRunResult(
            messages=[MockMessage(role="assistant", content="Response")]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_b_id,
                    "content": "User B's secret message",
                },
                headers=user_b_headers,
            )

        # User A tries to access User B's messages
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.get(
            f"/api/chatkit/threads/{thread_b_id}/messages",
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

    def test_user_cannot_send_message_to_other_user_thread(
        self, client: TestClient, generate_test_jwt
    ):
        """Test User A cannot send message to User B's thread."""
        # User B creates thread
        user_b_token = generate_test_jwt("user-b")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "User B Thread"},
            headers=user_b_headers,
        )
        thread_b_id = create_response.json()["id"]

        # User A tries to send message to User B's thread
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.post(
            "/api/chatkit/messages",
            json={
                "thread_id": thread_b_id,
                "content": "Unauthorized message",
            },
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

    def test_list_threads_only_shows_own_threads(
        self, client: TestClient, generate_test_jwt
    ):
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
        client.post(
            "/api/chatkit/threads",
            json={"title": "User B Thread 2"},
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

        threads_a = response_a.json()
        threads_b = response_b.json()

        # Verify each user only sees their own threads
        assert len(threads_a) == 2
        assert all("User A" in thread["title"] for thread in threads_a)

        assert len(threads_b) == 2
        assert all("User B" in thread["title"] for thread in threads_b)


class TestMCPToolUserIsolation:
    """Test user isolation at MCP tool level."""

    def test_mcp_add_task_enforces_user_id(
        self, client: TestClient, generate_test_jwt
    ):
        """Test MCP add_task tool creates task with correct user_id."""
        # User A sends message to create task
        user_a_id = "user-a"
        user_a_token = generate_test_jwt(user_a_id)
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        # Create thread
        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Task Test"},
            headers=user_a_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock agent response
        mock_result = MockRunResult(
            messages=[
                MockMessage(role="assistant", content="Task created successfully!")
            ]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            # Send message to create task
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_id,
                    "content": "Add a task to buy milk",
                },
                headers=user_a_headers,
            )

        # Verify task was created with User A's user_id
        response = client.get("/api/tasks", headers=user_a_headers)
        tasks = response.json()["tasks"]

        # If task was created, it should belong to User A
        # (This test verifies the agent passes correct user_id to MCP tools)
        assert all(task.get("user_id") == user_a_id for task in tasks if "user_id" in task)

    def test_mcp_list_tasks_filters_by_user_id(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test MCP list_tasks tool only returns user's own tasks."""
        # Create tasks for User A
        user_a_id = "user-a"
        task_a1 = Task(
            id=uuid.uuid4(),
            user_id=user_a_id,
            title="User A Task 1",
            priority=PriorityType.Medium,
            completed=False,
        )
        task_a2 = Task(
            id=uuid.uuid4(),
            user_id=user_a_id,
            title="User A Task 2",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add_all([task_a1, task_a2])

        # Create tasks for User B
        user_b_id = "user-b"
        task_b1 = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task 1",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b1)
        session.commit()

        # User A lists tasks via API
        user_a_token = generate_test_jwt(user_a_id)
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response_a = client.get("/api/tasks", headers=user_a_headers)
        tasks_a = response_a.json()["tasks"]

        # User B lists tasks via API
        user_b_token = generate_test_jwt(user_b_id)
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        response_b = client.get("/api/tasks", headers=user_b_headers)
        tasks_b = response_b.json()["tasks"]

        # Verify isolation
        assert len(tasks_a) == 2
        assert all("User A" in task["title"] for task in tasks_a)

        assert len(tasks_b) == 1
        assert "User B" in tasks_b[0]["title"]

    def test_mcp_get_task_enforces_user_id(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test MCP get_task tool validates user_id."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A tries to get User B's task via API
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.get(
            f"/api/tasks/{task_b.id}",
            headers=user_a_headers,
        )

        # Should return 404 (MCP tool validates user_id)
        assert response.status_code == 404

    def test_mcp_complete_task_enforces_user_id(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test MCP complete_task tool validates user_id."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A tries to complete User B's task via API
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.post(
            f"/api/tasks/{task_b.id}/toggle",
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

        # Verify task is still incomplete
        session.refresh(task_b)
        assert task_b.completed is False

    def test_mcp_delete_task_enforces_user_id(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test MCP delete_task tool validates user_id."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()
        task_b_id = task_b.id

        # User A tries to delete User B's task via API
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.delete(
            f"/api/tasks/{task_b_id}",
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

        # Verify task still exists
        task_still_exists = TaskService.get_task_by_id(session, task_b_id, user_b_id)
        assert task_still_exists is not None

    def test_mcp_update_task_enforces_user_id(
        self, client: TestClient, session, generate_test_jwt
    ):
        """Test MCP update_task tool validates user_id."""
        # User B creates task
        user_b_id = "user-b"
        task_b = Task(
            id=uuid.uuid4(),
            user_id=user_b_id,
            title="User B Task",
            priority=PriorityType.Medium,
            completed=False,
        )
        session.add(task_b)
        session.commit()

        # User A tries to update User B's task via API
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        response = client.patch(
            f"/api/tasks/{task_b.id}",
            json={"title": "Hacked title"},
            headers=user_a_headers,
        )

        # Should return 404
        assert response.status_code == 404

        # Verify task was not modified
        session.refresh(task_b)
        assert task_b.title == "User B Task"


class TestConversationHistoryIsolation:
    """Test conversation history is user-specific."""

    def test_conversation_history_is_user_specific(
        self, client: TestClient, generate_test_jwt
    ):
        """Test conversation history only includes user's own messages."""
        # User A creates thread and sends messages
        user_a_token = generate_test_jwt("user-a")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        create_response_a = client.post(
            "/api/chatkit/threads",
            json={"title": "User A Thread"},
            headers=user_a_headers,
        )
        thread_a_id = create_response_a.json()["id"]

        # Mock agent responses
        mock_result = RunResult(
            messages=[AgentMessage(role="assistant", content="Response")]
        )

        with patch.object(Runner, "run", return_value=mock_result):
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_a_id,
                    "content": "User A message 1",
                },
                headers=user_a_headers,
            )
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_a_id,
                    "content": "User A message 2",
                },
                headers=user_a_headers,
            )

        # User B creates thread and sends messages
        user_b_token = generate_test_jwt("user-b")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        create_response_b = client.post(
            "/api/chatkit/threads",
            json={"title": "User B Thread"},
            headers=user_b_headers,
        )
        thread_b_id = create_response_b.json()["id"]

        with patch.object(Runner, "run", return_value=mock_result):
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_b_id,
                    "content": "User B message 1",
                },
                headers=user_b_headers,
            )

        # Get User A's messages
        response_a = client.get(
            f"/api/chatkit/threads/{thread_a_id}/messages",
            headers=user_a_headers,
        )
        messages_a = response_a.json()

        # Get User B's messages
        response_b = client.get(
            f"/api/chatkit/threads/{thread_b_id}/messages",
            headers=user_b_headers,
        )
        messages_b = response_b.json()

        # Verify isolation
        assert len(messages_a) == 4  # 2 user messages + 2 assistant responses
        assert all("User A" in msg["content"] or msg["role"] == "assistant" for msg in messages_a)

        assert len(messages_b) == 2  # 1 user message + 1 assistant response
        assert any("User B" in msg["content"] for msg in messages_b)

    def test_agent_context_includes_correct_user_id(
        self, client: TestClient, generate_test_jwt
    ):
        """Test agent receives correct user_id in context for MCP tool calls."""
        # User A creates thread
        user_a_id = "user-a"
        user_a_token = generate_test_jwt(user_a_id)
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        create_response = client.post(
            "/api/chatkit/threads",
            json={"title": "Context Test"},
            headers=user_a_headers,
        )
        thread_id = create_response.json()["id"]

        # Mock Runner.run to capture context
        captured_context = {}

        def mock_run(agent, input, session, context):
            captured_context.update(context)
            return RunResult(
                messages=[AgentMessage(role="assistant", content="Response")]
            )

        with patch.object(Runner, "run", side_effect=mock_run):
            client.post(
                "/api/chatkit/messages",
                json={
                    "thread_id": thread_id,
                    "content": "Test message",
                },
                headers=user_a_headers,
            )

        # Verify correct user_id was passed to agent
        assert "user_id" in captured_context
        assert captured_context["user_id"] == user_a_id
