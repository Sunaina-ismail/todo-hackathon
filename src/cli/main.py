from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.cli.ui import UIHelper
from typing import Optional


class TodoApp:
    """Main application class for the Todo console application."""

    def __init__(self) -> None:
        """Initialize the application with required services."""
        self.repository = TaskRepository()
        self.service = TaskService(self.repository)
        self.ui = UIHelper()

    def run(self) -> None:
        """Run the main application loop."""
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
                self.ui.display_message("Thank you for using the Todo App. Goodbye!")
                break
            else:
                self.ui.display_error("Invalid choice. Please enter a number between 1-6.")

    def _add_task(self) -> None:
        """Handle adding a new task."""
        try:
            title, description = self.ui.get_task_input()

            # Validate title length
            if len(title) < 1 or len(title) > 100:
                self.ui.display_error(f"Title must be between 1 and 100 characters. You entered {len(title)} characters.")
                return

            # Validate description length if provided
            if description and len(description) > 500:
                self.ui.display_error(f"Description must be at most 500 characters. You entered {len(description)} characters.")
                return

            task = self.service.create_task(title, description)
            self.ui.display_message(f"Task '{task.title}' created successfully with ID {task.id}")
        except ValueError as e:
            self.ui.display_error(f"Error creating task: {str(e)}")
        except Exception as e:
            self.ui.display_error(f"Unexpected error creating task: {str(e)}")

    def _view_tasks(self) -> None:
        """Handle viewing all tasks."""
        try:
            tasks = self.service.get_all_tasks()
            self.ui.display_tasks(tasks)
        except Exception as e:
            self.ui.display_error(f"Error viewing tasks: {str(e)}")

    def _edit_task(self) -> None:
        """Handle editing a task."""
        try:
            task_id = self.ui.get_task_id("Enter the ID of the task to edit")

            # Check if task exists
            existing_task = self.service.get_task_by_id(task_id)
            if not existing_task:
                self.ui.display_error("Task ID not found")
                return

            # Get new values (allow keeping existing values)
            self.ui.display_message(f"Editing task ID {task_id}: {existing_task.title}")
            title_input = input(f"Enter new title (leave blank to keep '{existing_task.title}'): ").strip()
            description_input = input(f"Enter new description (leave blank to keep current): ").strip()

            # Use existing values if user didn't provide new ones
            new_title = title_input if title_input else existing_task.title
            new_description: Optional[str] = description_input if description_input != "" else existing_task.description

            # Validate title length if it was changed
            if title_input and (len(new_title) < 1 or len(new_title) > 100):
                self.ui.display_error(f"Title must be between 1 and 100 characters. You entered {len(new_title)} characters.")
                return

            # Validate description length if it was changed
            if description_input and new_description and len(new_description) > 500:
                self.ui.display_error(f"Description must be at most 500 characters. You entered {len(new_description)} characters.")
                return

            success = self.service.update_task(task_id, new_title, new_description)
            if success:
                self.ui.display_message(f"Task ID {task_id} updated successfully")
            else:
                self.ui.display_error("Failed to update task")
        except ValueError as e:
            self.ui.display_error(f"Error editing task: {str(e)}")
        except Exception as e:
            self.ui.display_error(f"Unexpected error editing task: {str(e)}")

    def _delete_task(self) -> None:
        """Handle deleting a task."""
        try:
            task_id = self.ui.get_task_id("Enter the ID of the task to delete")

            # Confirm deletion
            existing_task = self.service.get_task_by_id(task_id)
            if not existing_task:
                self.ui.display_error("Task ID not found")
                return

            confirmed = self.ui.confirm_action(f"Are you sure you want to delete task '{existing_task.title}' (ID: {task_id})?")
            if not confirmed:
                self.ui.display_message("Task deletion cancelled")
                return

            success = self.service.delete_task(task_id)
            if success:
                self.ui.display_message(f"Task ID {task_id} deleted successfully")
            else:
                self.ui.display_error("Failed to delete task")
        except ValueError as e:
            self.ui.display_error(f"Error deleting task: {str(e)}")
        except Exception as e:
            self.ui.display_error(f"Unexpected error deleting task: {str(e)}")

    def _toggle_task_status(self) -> None:
        """Handle toggling a task's completion status."""
        try:
            task_id = self.ui.get_task_id("Enter the ID of the task to toggle")

            # Check if task exists
            existing_task = self.service.get_task_by_id(task_id)
            if not existing_task:
                self.ui.display_error("Task ID not found")
                return

            success = self.service.toggle_task_status(task_id)
            if success:
                new_status = existing_task.status.value
                self.ui.display_message(f"Task ID {task_id} status updated to {new_status}")
            else:
                self.ui.display_error("Failed to toggle task status")
        except ValueError as e:
            self.ui.display_error(f"Error toggling task status: {str(e)}")
        except Exception as e:
            self.ui.display_error(f"Unexpected error toggling task status: {str(e)}")


def main() -> None:
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()