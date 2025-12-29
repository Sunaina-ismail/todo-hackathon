from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from src.models.task import Task, TaskStatus


class UIHelper:
    """Helper class for user interface operations."""

    def __init__(self) -> None:
        """Initialize the UI helper with a rich console."""
        self.console = Console()

    def display_menu(self) -> None:
        """Display the main menu options."""
        self.console.print("\n[bold blue]Todo App - Main Menu[/bold blue]")
        self.console.print("1. Add new task")
        self.console.print("2. View all tasks")
        self.console.print("3. Edit task")
        self.console.print("4. Delete task")
        self.console.print("5. Toggle task completion")
        self.console.print("6. Exit")
        self.console.print("\nEnter your choice (1-6):", end=" ")

    def get_user_choice(self) -> str:
        """Get user choice from the menu."""
        try:
            choice = input().strip()
            return choice
        except EOFError:
            return "6"  # Return 'Exit' option on EOF

    def display_tasks(self, tasks: List[Task]) -> None:
        """Display tasks in a rich table format."""
        if not tasks:
            self.console.print("[yellow]No tasks available[/yellow]")
            return

        table = Table(title="Task List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Status", style="blue")
        table.add_column("Created At", style="yellow")
        table.add_column("Updated At", style="yellow")

        for task in tasks:
            status_symbol = "✅" if task.status == TaskStatus.COMPLETED else "⏳"
            status_text = f"{status_symbol} {task.status.value}"

            table.add_row(
                str(task.id),
                task.title,
                task.description or "",
                status_text,
                task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                task.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            )

        self.console.print(table)

    def get_task_input(self) -> tuple[str, Optional[str]]:
        """Get task title and description from user input."""
        title = Prompt.ask("[bold]Enter task title (1-100 characters)[/bold]")
        description_input = Prompt.ask("[bold]Enter task description (optional, up to 500 characters)[/bold]", default="")

        description: Optional[str] = description_input if description_input != "" else None

        return title.strip(), description

    def get_task_id(self, prompt_text: str = "Enter task ID") -> int:
        """Get task ID from user input."""
        while True:
            try:
                task_id_str = Prompt.ask(f"[bold]{prompt_text}[/bold]")
                task_id = int(task_id_str)
                if task_id <= 0:
                    self.console.print("[red]Task ID must be a positive integer[/red]")
                    continue
                return task_id
            except ValueError:
                self.console.print("[red]Please enter a valid integer for task ID[/red]")

    def display_message(self, message: str, style: str = "green") -> None:
        """Display a message with the specified style."""
        self.console.print(f"[{style}]{message}[/{style}]")

    def display_error(self, error: str) -> None:
        """Display an error message."""
        self.console.print(f"[red]{error}[/red]")

    def confirm_action(self, message: str) -> bool:
        """Ask user to confirm an action."""
        return Confirm.ask(f"[bold]{message}[/bold]")