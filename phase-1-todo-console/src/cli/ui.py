from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from src.models.task import Task, TaskStatus


class UIHelper:
    def __init__(self) -> None:
        self.console = Console()

    def display_menu(self) -> None:
        self.console.print("\n[bold]Todo App[/bold]")
        self.console.print("1. Add task")
        self.console.print("2. View tasks")
        self.console.print("3. Edit task")
        self.console.print("4. Delete task")
        self.console.print("5. Toggle status")
        self.console.print("6. Exit")

    def get_user_choice(self) -> str:
        return input().strip()

    def display_tasks(self, tasks: List[Task]) -> None:
        if not tasks:
            self.console.print("[yellow]No tasks[/yellow]")
            return
        table = Table()
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Status", style="blue")
        for task in tasks:
            symbol = "✅" if task.status == TaskStatus.COMPLETED else "⏳"
            table.add_row(str(task.id), task.title, f"{symbol} {task.status.value}")
        self.console.print(table)

    def get_task_input(self) -> tuple[str, Optional[str]]:
        title = Prompt.ask("Title").strip()
        desc = Prompt.ask("Description (optional)", default="")
        return title, desc if desc else None

    def get_task_id(self, prompt: str = "Task ID") -> int:
        return int(Prompt.ask(prompt))

    def display_message(self, msg: str) -> None:
        self.console.print(f"[green]{msg}[/green]")

    def display_error(self, err: str) -> None:
        self.console.print(f"[red]{err}[/red]")

    def confirm_action(self, msg: str) -> bool:
        return Confirm.ask(msg)
