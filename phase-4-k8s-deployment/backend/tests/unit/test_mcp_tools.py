"""Unit Tests for MCP Tools

Tests for all 7 MCP tools with mocked TaskService to isolate tool logic.
Validates user_id isolation, input validation, error handling, and return formats.
"""

import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime

from mcp_server.tools import (
    add_task,
    list_tasks,
    get_task,
    complete_task,
    delete_task,
    update_task,
    set_priority,
)
from src.models.task import Task, PriorityType


class TestAddTask:
    """Test add_task MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.create_task")
    def test_add_task_success(self, mock_create_task, mock_get_session):
        """Test successful task creation."""
        # Setup mocks
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority=PriorityType.High,
            completed=False,
            created_at=datetime(2026, 1, 15, 10, 0, 0),
        )
        mock_create_task.return_value = mock_task

        # Execute
        result = add_task(
            user_id="user123",
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority="High",
        )

        # Verify
        assert result["task_id"] == str(task_id)
        assert result["title"] == "Buy groceries"
        assert result["description"] == "Milk, eggs, bread"
        assert result["priority"] == "High"
        assert result["completed"] is False
        assert "created_at" in result

        mock_create_task.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_add_task_invalid_priority(self, mock_get_session):
        """Test add_task with invalid priority raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid priority"):
            add_task(
                user_id="user123",
                title="Test task",
                priority="InvalidPriority",
            )

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_add_task_empty_title(self, mock_get_session):
        """Test add_task with empty title raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Title is required"):
            add_task(user_id="user123", title="   ")

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.create_task")
    def test_add_task_default_priority(self, mock_create_task, mock_get_session):
        """Test add_task uses Medium priority by default."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_create_task.return_value = mock_task

        result = add_task(user_id="user123", title="Test task")

        assert result["priority"] == "Medium"
        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.create_task")
    def test_add_task_with_due_date(self, mock_create_task, mock_get_session):
        """Test add_task with due_date."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        due_date = date(2026, 1, 20)
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            priority=PriorityType.Medium,
            due_date=due_date,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_create_task.return_value = mock_task

        result = add_task(
            user_id="user123",
            title="Test task",
            due_date="2026-01-20",
        )

        assert result["due_date"] == "2026-01-20"
        mock_session.close.assert_called_once()


class TestListTasks:
    """Test list_tasks MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_tasks_by_user")
    def test_list_tasks_success(self, mock_get_tasks, mock_get_session):
        """Test successful task listing."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task1 = Task(
            id=uuid.uuid4(),
            user_id="user123",
            title="Task 1",
            priority=PriorityType.High,
            completed=False,
            created_at=datetime.utcnow(),
        )
        task2 = Task(
            id=uuid.uuid4(),
            user_id="user123",
            title="Task 2",
            priority=PriorityType.Medium,
            completed=True,
            created_at=datetime.utcnow(),
        )
        mock_get_tasks.return_value = [task1, task2]

        result = list_tasks(user_id="user123")

        assert result["count"] == 2
        assert len(result["tasks"]) == 2
        assert result["tasks"][0]["title"] == "Task 1"
        assert result["tasks"][1]["title"] == "Task 2"
        assert result["filters"]["completed"] is None
        assert result["filters"]["priority"] is None

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_tasks_by_user")
    def test_list_tasks_filter_completed(self, mock_get_tasks, mock_get_session):
        """Test list_tasks with completed filter."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task1 = Task(
            id=uuid.uuid4(),
            user_id="user123",
            title="Completed task",
            priority=PriorityType.Medium,
            completed=True,
            created_at=datetime.utcnow(),
        )
        mock_get_tasks.return_value = [task1]

        result = list_tasks(user_id="user123", completed=True)

        assert result["count"] == 1
        assert result["filters"]["completed"] is True

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_tasks_by_user")
    def test_list_tasks_filter_priority(self, mock_get_tasks, mock_get_session):
        """Test list_tasks with priority filter."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task1 = Task(
            id=uuid.uuid4(),
            user_id="user123",
            title="High priority task",
            priority=PriorityType.High,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_get_tasks.return_value = [task1, task1]

        result = list_tasks(user_id="user123", priority="High")

        # Priority filter is applied after TaskService call
        assert result["count"] == 2
        assert result["filters"]["priority"] == "High"

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_list_tasks_invalid_limit(self, mock_get_session):
        """Test list_tasks with invalid limit raises ValueError."""
        # Create separate mock sessions for each call
        mock_session1 = Mock()
        mock_session2 = Mock()

        # First call with limit=0
        mock_get_session.return_value = iter([mock_session1])
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            list_tasks(user_id="user123", limit=0)
        mock_session1.close.assert_called_once()

        # Second call with limit=101
        mock_get_session.return_value = iter([mock_session2])
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            list_tasks(user_id="user123", limit=101)
        mock_session2.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_list_tasks_invalid_priority(self, mock_get_session):
        """Test list_tasks with invalid priority raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid priority"):
            list_tasks(user_id="user123", priority="InvalidPriority")

        mock_session.close.assert_called_once()


class TestGetTask:
    """Test get_task MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    def test_get_task_success(self, mock_get_task, mock_get_session):
        """Test successful task retrieval."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            description="Test description",
            priority=PriorityType.High,
            completed=False,
            created_at=datetime(2026, 1, 15, 10, 0, 0),
            updated_at=datetime(2026, 1, 15, 11, 0, 0),
        )
        mock_get_task.return_value = mock_task

        result = get_task(user_id="user123", task_id=str(task_id))

        assert result["task_id"] == str(task_id)
        assert result["title"] == "Test task"
        assert result["description"] == "Test description"
        assert result["priority"] == "High"
        assert result["completed"] is False
        assert "created_at" in result
        assert "updated_at" in result

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_get_task_invalid_uuid(self, mock_get_session):
        """Test get_task with invalid UUID raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid task_id"):
            get_task(user_id="user123", task_id="not-a-uuid")

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    def test_get_task_not_found(self, mock_get_task, mock_get_session):
        """Test get_task with non-existent task raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_get_task.return_value = None

        with pytest.raises(ValueError, match="not found or not accessible"):
            get_task(user_id="user123", task_id=str(task_id))

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    def test_get_task_user_isolation(self, mock_get_task, mock_get_session):
        """Test get_task enforces user isolation via TaskService."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_get_task.return_value = None  # TaskService returns None for wrong user

        with pytest.raises(ValueError, match="not found or not accessible"):
            get_task(user_id="user123", task_id=str(task_id))

        # Verify TaskService was called with correct user_id
        mock_get_task.assert_called_once_with(mock_session, task_id, "user123")
        mock_session.close.assert_called_once()


class TestCompleteTask:
    """Test complete_task MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    @patch("mcp_server.tools.TaskService.update_task")
    def test_complete_task_success(self, mock_update, mock_get_task, mock_get_session):
        """Test successful task completion."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_get_task.return_value = mock_task

        updated_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            priority=PriorityType.Medium,
            completed=True,
            created_at=datetime.utcnow(),
        )
        mock_update.return_value = updated_task

        result = complete_task(user_id="user123", task_id=str(task_id))

        assert result["task_id"] == str(task_id)
        assert result["title"] == "Test task"
        assert result["completed"] is True
        assert result["message"] == "Task marked as complete"

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_complete_task_invalid_uuid(self, mock_get_session):
        """Test complete_task with invalid UUID raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid task_id"):
            complete_task(user_id="user123", task_id="not-a-uuid")

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    def test_complete_task_not_found(self, mock_get_task, mock_get_session):
        """Test complete_task with non-existent task raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_get_task.return_value = None

        with pytest.raises(ValueError, match="not found or not accessible"):
            complete_task(user_id="user123", task_id=str(task_id))

        mock_session.close.assert_called_once()


class TestDeleteTask:
    """Test delete_task MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    @patch("mcp_server.tools.TaskService.delete_task")
    def test_delete_task_success(self, mock_delete, mock_get_task, mock_get_session):
        """Test successful task deletion."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Task to delete",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_get_task.return_value = mock_task

        result = delete_task(user_id="user123", task_id=str(task_id))

        assert result["task_id"] == str(task_id)
        assert result["title"] == "Task to delete"
        assert result["message"] == "Task deleted successfully"

        mock_delete.assert_called_once_with(mock_session, task_id, "user123")
        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_delete_task_invalid_uuid(self, mock_get_session):
        """Test delete_task with invalid UUID raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid task_id"):
            delete_task(user_id="user123", task_id="not-a-uuid")

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    def test_delete_task_not_found(self, mock_get_task, mock_get_session):
        """Test delete_task with non-existent task raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_get_task.return_value = None

        with pytest.raises(ValueError, match="not found or not accessible"):
            delete_task(user_id="user123", task_id=str(task_id))

        mock_session.close.assert_called_once()


class TestUpdateTask:
    """Test update_task MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    @patch("mcp_server.tools.TaskService.update_task")
    def test_update_task_title(self, mock_update, mock_get_task, mock_get_session):
        """Test updating task title."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Old title",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_get_task.return_value = mock_task

        updated_task = Task(
            id=task_id,
            user_id="user123",
            title="New title",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_update.return_value = updated_task

        result = update_task(
            user_id="user123",
            task_id=str(task_id),
            title="New title",
        )

        assert result["task_id"] == str(task_id)
        assert result["title"] == "New title"
        assert result["message"] == "Task updated successfully"

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    @patch("mcp_server.tools.TaskService.update_task")
    def test_update_task_multiple_fields(self, mock_update, mock_get_task, mock_get_session):
        """Test updating multiple task fields."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Old title",
            description="Old description",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_get_task.return_value = mock_task

        updated_task = Task(
            id=task_id,
            user_id="user123",
            title="New title",
            description="New description",
            priority=PriorityType.High,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_update.return_value = updated_task

        result = update_task(
            user_id="user123",
            task_id=str(task_id),
            title="New title",
            description="New description",
            priority="High",
        )

        assert result["title"] == "New title"
        assert result["description"] == "New description"
        assert result["priority"] == "High"

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_update_task_invalid_uuid(self, mock_get_session):
        """Test update_task with invalid UUID raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid task_id"):
            update_task(user_id="user123", task_id="not-a-uuid", title="New title")

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_update_task_invalid_priority(self, mock_get_session):
        """Test update_task with invalid priority raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()

        with pytest.raises(ValueError, match="Invalid priority"):
            update_task(
                user_id="user123",
                task_id=str(task_id),
                priority="InvalidPriority",
            )

        mock_session.close.assert_called_once()


class TestSetPriority:
    """Test set_priority MCP tool."""

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    @patch("mcp_server.tools.TaskService.update_task")
    def test_set_priority_success(self, mock_update, mock_get_task, mock_get_session):
        """Test successful priority update."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            priority=PriorityType.Medium,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_get_task.return_value = mock_task

        updated_task = Task(
            id=task_id,
            user_id="user123",
            title="Test task",
            priority=PriorityType.High,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_update.return_value = updated_task

        result = set_priority(user_id="user123", task_id=str(task_id), priority="High")

        assert result["task_id"] == str(task_id)
        assert result["title"] == "Test task"
        assert result["priority"] == "High"
        assert result["message"] == "Priority updated successfully"

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_set_priority_invalid_uuid(self, mock_get_session):
        """Test set_priority with invalid UUID raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        with pytest.raises(ValueError, match="Invalid task_id"):
            set_priority(user_id="user123", task_id="not-a-uuid", priority="High")

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    def test_set_priority_invalid_priority(self, mock_get_session):
        """Test set_priority with invalid priority raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()

        with pytest.raises(ValueError, match="Invalid priority"):
            set_priority(
                user_id="user123",
                task_id=str(task_id),
                priority="InvalidPriority",
            )

        mock_session.close.assert_called_once()

    @patch("mcp_server.tools.get_session")
    @patch("mcp_server.tools.TaskService.get_task_by_id")
    def test_set_priority_not_found(self, mock_get_task, mock_get_session):
        """Test set_priority with non-existent task raises ValueError."""
        mock_session = Mock()
        mock_get_session.return_value = iter([mock_session])

        task_id = uuid.uuid4()
        mock_get_task.return_value = None

        with pytest.raises(ValueError, match="not found or not accessible"):
            set_priority(user_id="user123", task_id=str(task_id), priority="High")

        mock_session.close.assert_called_once()
