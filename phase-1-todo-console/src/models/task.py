from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Invalid ID")
        if len(self.title) < 1 or len(self.title) > 100:
            raise ValueError("Title must be 1-100 chars")
        if self.description and len(self.description) > 500:
            raise ValueError("Description max 500 chars")

    def update(self, title: Optional[str] = None, desc: Optional[str] = None) -> None:
        if title:
            self.title = title
        if desc is not None:
            self.description = desc
        self.updated_at = datetime.now()

    def toggle_status(self) -> None:
        self.status = TaskStatus.COMPLETED if self.status == TaskStatus.PENDING else TaskStatus.PENDING
        self.updated_at = datetime.now()
