"""Task Schemas

Pydantic schemas for task request/response validation and serialization.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from src.models.task import PriorityType


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        min_length=1,
        max_length=200,
        examples=["Buy groceries"],
        description="Task title, required, 1-200 characters",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Milk, bread, eggs, butter"],
        description="Optional task description, 0-1000 characters",
    )
    priority: PriorityType = Field(
        default=PriorityType.Medium,
        description="Task priority level: High, Medium, or Low (default: Medium)"
    )
    due_date: date | None = Field(
        default=None,
        description="Optional task due date (ISO 8601 format: YYYY-MM-DD)"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="List of tag names to associate with the task"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, bread, eggs",
                    "priority": "High",
                    "due_date": "2025-01-05",
                    "tags": ["shopping", "urgent"]
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional to support partial updates.
    """

    title: str | None = Field(
        default=None, min_length=1, max_length=200, description="Task title, optional, 1-200 characters"
    )
    description: str | None = Field(
        default=None, max_length=1000, description="Optional task description, 0-1000 characters"
    )
    completed: bool | None = Field(default=None, description="Task completion status")
    priority: PriorityType | None = Field(
        default=None,
        description="Task priority level: High, Medium, or Low"
    )
    due_date: date | None = Field(
        default=None,
        description="Task due date (ISO 8601 format: YYYY-MM-DD)"
    )
    tags: list[str] | None = Field(
        default=None,
        description="List of tag names (replaces existing tags)"
    )

    model_config = {
        "populate_by_name": True,
        "exclude_none": True
    }


class TaskResponse(BaseModel):
    """Schema for task data in API responses."""

    id: uuid.UUID
    user_id: str
    title: str
    description: str | None
    completed: bool
    priority: PriorityType
    due_date: date | None
    created_at: datetime
    updated_at: datetime
    tags: list[str] = Field(
        default_factory=list,
        description="List of tag names associated with this task"
    )

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        },
    }


class TaskListResponse(BaseModel):
    """Schema for paginated task list responses."""

    tasks: list[TaskResponse] = Field(
        description="List of tasks matching the query"
    )
    total: int = Field(
        description="Total number of tasks matching the query (before pagination)"
    )
    limit: int = Field(
        description="Maximum number of tasks returned"
    )
    offset: int = Field(
        description="Number of tasks skipped"
    )
