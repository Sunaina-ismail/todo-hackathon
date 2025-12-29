from typing import List, Optional
from src.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def create_task(self, title: str, desc: Optional[str] = None) -> Task:
        next_id = max((t.id for t in self._tasks), default=0) + 1
        task = Task(id=next_id, title=title, description=desc)
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        return sorted(self._tasks, key=lambda t: t.id)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, desc: Optional[str] = None) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.update(title, desc)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def toggle_task_status(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.toggle_status()
            return True
        return False
