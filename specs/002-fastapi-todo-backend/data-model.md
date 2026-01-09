# Data Model: FastAPI Todo Backend (Phase II)

## Entities

### Task Entity

**Source**: `phase-2-todo-full-stack/backend/src/models/task.py`

SQLModel entity representing a user's task with strict user isolation.

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

from enum import Enum
from datetime import date
import uuid

class PriorityType(str, Enum):
    """Priority levels for tasks"""
    High = "High"
    Medium = "Medium"
    Low = "Low"

class Task(SQLModel, table=True):
    """Task entity with user data isolation enforcement."""
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique task identifier (UUID v4)"
    )
    user_id: str = Field(
        index=True,
        nullable=False,
        description="Better Auth user ID (UUID) for strict data isolation"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Task title, required, 1-200 characters"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional task description, 0-1000 characters"
    )
    completed: bool = Field(
        default=False,
        description="Task completion status"
    )
    priority: PriorityType = Field(
        default=PriorityType.Medium,
        description="Task priority level: High, Medium, or Low (default: Medium)"
    )
    due_date: date | None = Field(
        default=None,
        description="Optional task due date (ISO 8601 format: YYYY-MM-DD)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when task was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when task was last updated"
    )

    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_user_id_completed", "user_id", "completed"),
    )
```

### Tag Entity

**Source**: `phase-2-todo-full-stack/backend/src/models/tag.py`

SQLModel entity representing a user-defined tag for organizing tasks.

```python
import uuid
from sqlmodel import SQLModel, Field, Index

class Tag(SQLModel, table=True):
    """Tag entity with user data isolation enforcement."""
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique tag identifier (UUID v4)"
    )
    name: str = Field(
        max_length=50,
        nullable=False,
        description="Tag name, required, max 50 characters"
    )
    user_id: str = Field(
        index=True,
        nullable=False,
        description="Better Auth user ID (UUID) for strict data isolation"
    )

    __tablename__ = "tags"
    __table_args__ = (
        Index("ix_tags_user_id_name", "user_id", "name", unique=True),
    )
```

### TaskTag Entity (Junction Table)

**Source**: `phase-2-todo-full-stack/backend/src/models/task_tag.py`

SQLModel entity representing the many-to-many relationship between tasks and tags.

```python
import uuid
from sqlmodel import SQLModel, Field

class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship."""
    task_id: uuid.UUID = Field(
        foreign_key="tasks.id",
        primary_key=True,
        ondelete="CASCADE",
        description="Foreign key to tasks table"
    )
    tag_id: uuid.UUID = Field(
        foreign_key="tags.id",
        primary_key=True,
        ondelete="CASCADE",
        description="Foreign key to tags table"
    )

    __tablename__ = "task_tags"
```

### Indexes

| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_task_user_id` | `user_id` | Filter tasks by user (required for data isolation) |
| `ix_tasks_user_id_completed` | `user_id`, `completed` | Filter tasks by user + status (composite index) |
| `ix_tags_user_id_name` | `user_id`, `name` | Ensure tag names are unique per user + fast lookup |
| `task_tags_pkey` | `task_id`, `tag_id` | Primary key for junction table (composite) |

### Validation Rules

| Field | Constraint | Error Message |
|-------|------------|---------------|
| `title` | `min_length=1` | "Title cannot be empty" |
| `title` | `max_length=200` | "Title must be 200 characters or less" |
| `description` | `max_length=1000` | "Description must be 1000 characters or less" |
| `user_id` | Required, indexed | (enforced by database FK) |

## Pydantic Schemas

### TaskCreate Schema

**Source**: `phase-2-todo-full-stack/backend/src/schemas/task.py`

Request schema for creating a new task.

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import List

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(
        min_length=1,
        max_length=200,
        examples=["Buy groceries"],
        description="Task title, required, 1-200 characters"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Milk, bread, eggs, butter"],
        description="Optional task description, 0-1000 characters"
    )
    priority: PriorityType = Field(
        default=PriorityType.Medium,
        description="Task priority level: High, Medium, or Low (default: Medium)"
    )
    due_date: date | None = Field(
        default=None,
        description="Optional task due date (ISO 8601 format: YYYY-MM-DD)"
    )
    tags: List[str] = Field(
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
```

### TaskUpdate Schema

Request schema for updating an existing task. All fields are optional.

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Task title, optional, 1-200 characters"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional task description, 0-1000 characters"
    )
    completed: bool | None = Field(
        default=None,
        description="Task completion status"
    )
    priority: PriorityType | None = Field(
        default=None,
        description="Task priority level: High, Medium, or Low"
    )
    due_date: date | None = Field(
        default=None,
        description="Task due date (ISO 8601 format: YYYY-MM-DD)"
    )
    tags: List[str] | None = Field(
        default=None,
        description="List of tag names (replaces existing tags)"
    )

    model_config = {
        "populate_by_name": True,
        "exclude_none": True
    }
```

### TaskResponse Schema

Response schema for task data in API responses.

```python
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
import uuid

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
    tags: List[str] = Field(
        default_factory=list,
        description="List of tag names associated with this task"
    )

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        }
    }
```

### TagWithUsage Schema

Schema for tag autocomplete responses showing tag usage statistics.

```python
from pydantic import BaseModel, Field

class TagWithUsage(BaseModel):
    """Schema for tag autocomplete responses."""
    name: str = Field(description="Tag name")
    usage_count: int = Field(description="Number of tasks using this tag")
```

### Pagination Response Schema

```python
from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    data: List[T]
    total: int
    limit: int
    offset: int

    @property
    def has_more(self) -> bool:
        return (self.offset + len(self.data)) < self.total
```

## State Transitions

### Task Lifecycle

```
CREATED → (toggle) → COMPLETED → (toggle) → PENDING
             ↓
         DELETED (permanent)
```

### Valid State Changes

| From | To | Allowed | Condition |
|------|-----|---------|-----------|
| PENDING | COMPLETED | ✅ | User owns task |
| COMPLETED | PENDING | ✅ | User owns task |
| Any | DELETED | ✅ | User owns task (DELETE operation) |

## Relationships

**Task** belongs to **User** (via `user_id` foreign key)
- Cardinality: Many-to-One (many tasks per user)
- No reverse relationship exposed in API (enforces data isolation)

**Task** has many **Tags** (via `task_tags` junction table)
- Cardinality: Many-to-Many (many tasks can have many tags)
- Tags are user-specific (data isolation enforced on Tag.user_id)
- Cascade delete: deleting a task removes its tag associations
- Orphaned tags (no task references) are automatically cleaned up

**Tag** belongs to **User** (via `user_id` foreign key)
- Cardinality: Many-to-One (many tags per user)
- Tag names are unique per user (enforced by composite unique index)

## Database Constraints

| Constraint | Type | Expression |
|------------|------|------------|
| `task_title_not_empty` | Check | `LENGTH(TRIM(title)) > 0` |
| `task_title_max_length` | Check | `LENGTH(title) <= 200` |
| `task_description_max_length` | Check | `LENGTH(description) <= 1000` |

## Migration Files

**Source**: `phase-2-todo-full-stack/backend/alembic/versions/`

| Version | Description |
|---------|-------------|
| `001_create_tasks_table.py` | Create tasks table with all columns and indexes (UUID id, priority, due_date) |
| `002_create_tags_table.py` | Create tags table with user_id and unique constraint on (user_id, name) |
| `003_create_task_tags_junction.py` | Create task_tags junction table for many-to-many relationship |

## Audit Fields

| Field | Managed By | Updated On |
|-------|------------|------------|
| `created_at` | Database trigger/ORM default | INSERT only |
| `updated_at` | Database trigger/ORM `onupdate` | INSERT + UPDATE |
