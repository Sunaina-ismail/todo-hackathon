from typing import List, Optional
from src.models.task import Task
from src.repositories.task_repository import TaskRepository


class TaskService:
    """Service layer implementing business logic for task operations."""

    def __init__(self, repository: TaskRepository):
        """
        Initialize the service with a task repository.

        Args:
            repository: The task repository to use for data operations
        """
        self._repository = repository

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with validation.

        Args:
            title: The task title (1-100 characters)
            description: Optional task description (up to 500 characters)

        Returns:
            The created Task object

        Raises:
            ValueError: If the title or description don't meet validation requirements
        """
        # The validation is handled by the Task model itself
        return self._repository.create_task(title, description)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks sorted by ID
        """
        return self._repository.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self._repository.get_task_by_id(task_id)

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
        return self._repository.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        return self._repository.delete_task(task_id)

    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle a task's status between PENDING and COMPLETED.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if not found
        """
        return self._repository.toggle_task_status(task_id)