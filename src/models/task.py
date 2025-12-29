from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import re


class TaskStatus(Enum):
    """Enum representing the status of a task."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class Task:
    """Represents a single to-do item with validation."""
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate the task after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate task fields according to specification."""
        # Validate ID
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {self.id}")

        # Validate title
        if not isinstance(self.title, str):
            raise ValueError(f"Task title must be a string, got {type(self.title)}")

        if len(self.title) < 1 or len(self.title) > 100:
            raise ValueError(f"Task title must be between 1 and 100 characters, got {len(self.title)}")

        # Check for printable Unicode characters in title
        if not all(self._is_printable_unicode(char) for char in self.title):
            raise ValueError("Task title must contain only printable Unicode characters")

        # Validate description if provided
        if self.description is not None:
            if not isinstance(self.description, str):
                raise ValueError(f"Task description must be a string, got {type(self.description)}")

            if len(self.description) > 500:
                raise ValueError(f"Task description must be at most 500 characters, got {len(self.description)}")

            # Check for printable Unicode characters in description
            if not all(self._is_printable_unicode(char) for char in self.description):
                raise ValueError("Task description must contain only printable Unicode characters")

        # Validate status
        if not isinstance(self.status, TaskStatus):
            raise ValueError(f"Task status must be a TaskStatus enum value, got {type(self.status)}")

    @staticmethod
    def _is_printable_unicode(char: str) -> bool:
        """Check if a character is a printable Unicode character."""
        return char.isprintable()

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update task details and update the timestamp."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()
        self._validate()

    def toggle_status(self) -> None:
        """Toggle the task status between PENDING and COMPLETED."""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.COMPLETED
        else:
            self.status = TaskStatus.PENDING
        self.updated_at = datetime.now()