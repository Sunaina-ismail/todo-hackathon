"""Task Model

SQLModel entity representing a user's task with strict user isolation.
"""

import uuid
from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, Index, SQLModel


class PriorityType(str, Enum):
    """Priority levels for tasks"""
    High = "High"
    Medium = "Medium"
    Low = "Low"


class Task(SQLModel, table=True):
    """Task entity with user data isolation enforcement.

    Attributes:
        id: Primary key, UUID v4
        user_id: Better Auth user ID (UUID) for strict data isolation
        title: Task title, required, 1-200 characters
        description: Optional task description, 0-1000 characters
        completed: Task completion status, default False
        priority: Task priority level (High/Medium/Low), default Medium
        due_date: Optional task due date
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_user_id_completed", "user_id", "completed"),
    )

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique task identifier (UUID v4)"
    )
    user_id: str = Field(
        index=True, nullable=False, description="Better Auth user ID (UUID) for data isolation"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Task title, required, 1-200 characters",
    )
    description: str | None = Field(
        default=None, max_length=1000, description="Optional task description, 0-1000 characters"
    )
    completed: bool = Field(default=False, description="Task completion status")
    priority: PriorityType = Field(
        default=PriorityType.Medium,
        description="Task priority level: High, Medium, or Low (default: Medium)"
    )
    due_date: date | None = Field(
        default=None,
        description="Optional task due date (ISO 8601 format: YYYY-MM-DD)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when task was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when task was last updated"
    )
