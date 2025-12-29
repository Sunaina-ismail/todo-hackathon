from typing import List, Optional
from src.models.task import Task
from src.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def create_task(self, title: str, desc: Optional[str] = None) -> Task:
        return self._repo.create_task(title, desc)

    def get_all_tasks(self) -> List[Task]:
        return self._repo.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self._repo.get_task_by_id(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, desc: Optional[str] = None) -> bool:
        return self._repo.update_task(task_id, title, desc)

    def delete_task(self, task_id: int) -> bool:
        return self._repo.delete_task(task_id)

    def toggle_task_status(self, task_id: int) -> bool:
        return self._repo.toggle_task_status(task_id)
