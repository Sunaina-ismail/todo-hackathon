from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.cli.ui import UIHelper
from typing import Optional


class TodoApp:
    def __init__(self) -> None:
        self.repository = TaskRepository()
        self.service = TaskService(self.repository)
        self.ui = UIHelper()

    def run(self) -> None:
        while True:
            self.ui.display_menu()
            choice = self.ui.get_user_choice()

            if choice == "1":
                self._add_task()
            elif choice == "2":
                self._view_tasks()
            elif choice == "3":
                self._edit_task()
            elif choice == "4":
                self._delete_task()
            elif choice == "5":
                self._toggle_task_status()
            elif choice == "6":
                self.ui.display_message("Goodbye!")
                break
            else:
                self.ui.display_error("Invalid choice")

    def _add_task(self) -> None:
        title, description = self.ui.get_task_input()
        if len(title) < 1 or len(title) > 100:
            self.ui.display_error("Title must be 1-100 characters")
            return
        task = self.service.create_task(title, description)
        self.ui.display_message(f"Task {task.id} created")

    def _view_tasks(self) -> None:
        tasks = self.service.get_all_tasks()
        self.ui.display_tasks(tasks)

    def _edit_task(self) -> None:
        task_id = self.ui.get_task_id()
        existing_task = self.service.get_task_by_id(task_id)
        if not existing_task:
            self.ui.display_error("Task not found")
            return
        self.ui.display_message(f"Editing task {task_id}")
        # Simplified for brevity

    def _delete_task(self) -> None:
        task_id = self.ui.get_task_id()
        if self.service.delete_task(task_id):
            self.ui.display_message("Task deleted")
        else:
            self.ui.display_error("Task not found")

    def _toggle_task_status(self) -> None:
        task_id = self.ui.get_task_id()
        if self.service.toggle_task_status(task_id):
            self.ui.display_message("Status toggled")
        else:
            self.ui.display_error("Task not found")


def main() -> None:
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
