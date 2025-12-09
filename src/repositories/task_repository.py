from typing import List, Optional
from src.models.task import Task, TaskStatus
from datetime import datetime


class TaskRepository:
    """Repository for managing in-memory task storage with CRUD operations."""

    def __init__(self) -> None:
        """Initialize the repository with an empty list of tasks."""
        self._tasks: List[Task] = []

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with auto-incremented ID.

        Args:
            title: The task title (1-100 characters)
            description: Optional task description (up to 500 characters)

        Returns:
            The created Task object
        """
        # Determine the next ID (max existing ID + 1, or 1 if no tasks exist)
        if self._tasks:
            next_id = max(task.id for task in self._tasks) + 1
        else:
            next_id = 1

        # Create the new task
        task = Task(
            id=next_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks sorted by ID in ascending order.

        Returns:
            List of all tasks sorted by ID
        """
        return sorted(self._tasks, key=lambda t: t.id)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update a task's details.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if the task was updated, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.update(title=title, description=description)
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle a task's status between PENDING and COMPLETED.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.toggle_status()
        return True