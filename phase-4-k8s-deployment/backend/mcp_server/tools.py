"""MCP Tools for Task Management

FastMCP tools that enable the AI agent to interact with tasks.
All tools enforce user isolation and call existing TaskService methods.
"""

import uuid
from typing import Any

from mcp.server.fastmcp import FastMCP
from sqlmodel import Session

from src.db.session import get_session
from src.models.task import PriorityType
from src.schemas.task import TaskCreate, TaskUpdate
from src.services.task_service import TaskService

# Initialize FastMCP server
mcp = FastMCP(name="todo-task-server")


@mcp.tool()
def add_task(
    user_id: str,
    title: str,
    description: str | None = None,
    priority: str = "Medium",
    due_date: str | None = None,
) -> dict[str, Any]:
    """Create a new task for a user.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        title: Task title (required, 1-200 characters)
        description: Optional task description (0-1000 characters)
        priority: Task priority (High, Medium, Low) - default Medium
        due_date: Optional due date in ISO format (YYYY-MM-DD)

    Returns:
        Dictionary with task details:
        {
            "task_id": "uuid-string",
            "title": "Task title",
            "description": "Task description",
            "priority": "High",
            "completed": false,
            "due_date": "2026-01-20",
            "created_at": "2026-01-15T12:00:00Z"
        }

    Raises:
        ValueError: If priority is invalid or title is empty

    Example:
        >>> add_task(
        ...     user_id="user123",
        ...     title="Buy groceries",
        ...     description="Milk, eggs, bread",
        ...     priority="High"
        ... )
    """
    # Create task using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate priority
        try:
            priority_enum = PriorityType(priority)
        except ValueError:
            raise ValueError(f"Invalid priority: {priority}. Must be High, Medium, or Low")

        # Validate title
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        task_create = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority_enum,
            due_date=due_date,
        )
        task = TaskService.create_task(session, user_id, task_create)

        return {
            "task_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value,
            "completed": task.completed,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
        }
    finally:
        session.close()


@mcp.tool()
def list_tasks(
    user_id: str,
    completed: bool | None = None,
    priority: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """List tasks for a user with optional filters.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        completed: Filter by completion status (None = all tasks)
        priority: Filter by priority (High, Medium, Low) - None = all priorities
        limit: Maximum number of tasks to return (default 50, max 100)

    Returns:
        Dictionary with task list:
        {
            "tasks": [
                {
                    "task_id": "uuid-string",
                    "title": "Task title",
                    "description": "Task description",
                    "priority": "High",
                    "completed": false,
                    "due_date": "2026-01-20",
                    "created_at": "2026-01-15T12:00:00Z"
                },
                ...
            ],
            "count": 5,
            "filters": {
                "completed": false,
                "priority": "High"
            }
        }

    Example:
        >>> list_tasks(user_id="user123", completed=False, priority="High")
    """
    # Get tasks using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate limit
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        # Validate priority if provided
        priority_enum = None
        if priority:
            try:
                priority_enum = PriorityType(priority)
            except ValueError:
                raise ValueError(f"Invalid priority: {priority}. Must be High, Medium, or Low")

        tasks = TaskService.get_tasks_by_user(
            session=session,
            user_id=user_id,
            completed=completed,
            limit=limit,
            offset=0,
        )

        # Filter by priority if specified
        if priority_enum:
            tasks = [task for task in tasks if task.priority == priority_enum]

        # Convert to response format
        task_list = [
            {
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "completed": task.completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        return {
            "tasks": task_list,
            "count": len(task_list),
            "filters": {
                "completed": completed,
                "priority": priority,
            },
        }
    finally:
        session.close()


@mcp.tool()
def get_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Get a specific task by ID.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        task_id: Task UUID (string)

    Returns:
        Dictionary with task details:
        {
            "task_id": "uuid-string",
            "title": "Task title",
            "description": "Task description",
            "priority": "High",
            "completed": false,
            "due_date": "2026-01-20",
            "created_at": "2026-01-15T12:00:00Z",
            "updated_at": "2026-01-15T12:30:00Z"
        }

    Raises:
        ValueError: If task_id is invalid UUID or task not found

    Example:
        >>> get_task(user_id="user123", task_id="550e8400-e29b-41d4-a716-446655440000")
    """
    # Get task using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate task_id is valid UUID
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task_id: {task_id}. Must be a valid UUID")

        task = TaskService.get_task_by_id(session, task_uuid, user_id)

        if not task:
            raise ValueError(f"Task {task_id} not found or not accessible")

        return {
            "task_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value,
            "completed": task.completed,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }
    finally:
        session.close()


@mcp.tool()
def set_priority(user_id: str, task_id: str, priority: str) -> dict[str, Any]:
    """Update the priority of a task.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        task_id: Task UUID (string)
        priority: New priority (High, Medium, Low)

    Returns:
        Dictionary with updated task details:
        {
            "task_id": "uuid-string",
            "title": "Task title",
            "priority": "High",
            "message": "Priority updated successfully"
        }

    Raises:
        ValueError: If task_id is invalid, task not found, or priority is invalid

    Example:
        >>> set_priority(user_id="user123", task_id="550e8400-...", priority="High")
    """
    # Update task using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate task_id is valid UUID
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task_id: {task_id}. Must be a valid UUID")

        # Validate priority
        try:
            priority_enum = PriorityType(priority)
        except ValueError:
            raise ValueError(f"Invalid priority: {priority}. Must be High, Medium, or Low")

        # Get task first to verify ownership
        task = TaskService.get_task_by_id(session, task_uuid, user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found or not accessible")

        # Update priority
        task_update = TaskUpdate(priority=priority_enum)
        updated_task = TaskService.update_task(session, task_uuid, user_id, task_update)

        return {
            "task_id": str(updated_task.id),
            "title": updated_task.title,
            "priority": updated_task.priority.value,
            "message": "Priority updated successfully",
        }
    finally:
        session.close()


@mcp.tool()
def complete_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Mark a task as complete.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        task_id: Task UUID (string)

    Returns:
        Dictionary with updated task details:
        {
            "task_id": "uuid-string",
            "title": "Task title",
            "completed": true,
            "message": "Task marked as complete"
        }

    Raises:
        ValueError: If task_id is invalid or task not found

    Example:
        >>> complete_task(user_id="user123", task_id="550e8400-...")
    """
    # Update task using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate task_id is valid UUID
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task_id: {task_id}. Must be a valid UUID")

        # Get task first to verify ownership
        task = TaskService.get_task_by_id(session, task_uuid, user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found or not accessible")

        # Mark as complete
        task_update = TaskUpdate(completed=True)
        updated_task = TaskService.update_task(session, task_uuid, user_id, task_update)

        return {
            "task_id": str(updated_task.id),
            "title": updated_task.title,
            "completed": updated_task.completed,
            "message": "Task marked as complete",
        }
    finally:
        session.close()


@mcp.tool()
def delete_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Delete a task permanently.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        task_id: Task UUID (string)

    Returns:
        Dictionary with deletion confirmation:
        {
            "task_id": "uuid-string",
            "title": "Task title",
            "message": "Task deleted successfully"
        }

    Raises:
        ValueError: If task_id is invalid or task not found

    Example:
        >>> delete_task(user_id="user123", task_id="550e8400-...")
    """
    # Delete task using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate task_id is valid UUID
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task_id: {task_id}. Must be a valid UUID")

        # Get task first to verify ownership and get title
        task = TaskService.get_task_by_id(session, task_uuid, user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found or not accessible")

        task_title = task.title

        # Delete task
        TaskService.delete_task(session, task_uuid, user_id)

        return {
            "task_id": str(task_uuid),
            "title": task_title,
            "message": "Task deleted successfully",
        }
    finally:
        session.close()


@mcp.tool()
def update_task(
    user_id: str,
    task_id: str,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
) -> dict[str, Any]:
    """Update task details.

    Args:
        user_id: Better Auth user ID (string) for data isolation
        task_id: Task UUID (string)
        title: New task title (optional)
        description: New task description (optional)
        priority: New priority (High, Medium, Low) (optional)
        due_date: New due date in ISO format YYYY-MM-DD (optional)

    Returns:
        Dictionary with updated task details:
        {
            "task_id": "uuid-string",
            "title": "Updated title",
            "description": "Updated description",
            "priority": "High",
            "due_date": "2026-01-20",
            "message": "Task updated successfully"
        }

    Raises:
        ValueError: If task_id is invalid, task not found, or priority is invalid

    Example:
        >>> update_task(
        ...     user_id="user123",
        ...     task_id="550e8400-...",
        ...     title="Buy groceries and cook dinner",
        ...     priority="High"
        ... )
    """
    # Update task using TaskService
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Validate task_id is valid UUID
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task_id: {task_id}. Must be a valid UUID")

        # Validate priority if provided
        priority_enum = None
        if priority:
            try:
                priority_enum = PriorityType(priority)
            except ValueError:
                raise ValueError(f"Invalid priority: {priority}. Must be High, Medium, or Low")

        # Get task first to verify ownership
        task = TaskService.get_task_by_id(session, task_uuid, user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found or not accessible")

        # Build update data
        update_data = {}
        if title is not None:
            update_data["title"] = title.strip()
        if description is not None:
            update_data["description"] = description.strip() if description else None
        if priority_enum is not None:
            update_data["priority"] = priority_enum
        if due_date is not None:
            update_data["due_date"] = due_date

        # Update task
        task_update = TaskUpdate(**update_data)
        updated_task = TaskService.update_task(session, task_uuid, user_id, task_update)

        return {
            "task_id": str(updated_task.id),
            "title": updated_task.title,
            "description": updated_task.description,
            "priority": updated_task.priority.value,
            "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
            "message": "Task updated successfully",
        }
    finally:
        session.close()

