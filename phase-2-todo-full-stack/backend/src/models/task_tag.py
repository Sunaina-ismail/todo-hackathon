"""TaskTag Junction Table

SQLModel entity representing the many-to-many relationship between tasks and tags.
"""

import uuid

from sqlmodel import Field, Index, SQLModel


class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship.

    Attributes:
        task_id: Foreign key to tasks table (CASCADE delete)
        tag_id: Foreign key to tags table (CASCADE delete)

    Indexes:
        - Composite primary key on (task_id, tag_id)
        - Index on tag_id for reverse lookups

    When a task is deleted, all task_tag associations are automatically removed.
    When a tag is deleted, all task_tag associations are automatically removed.
    """

    __tablename__ = "task_tags"
    __table_args__ = (
        Index("ix_task_tags_tag_id", "tag_id"),
    )

    task_id: uuid.UUID = Field(
        foreign_key="tasks.id",
        primary_key=True,
        nullable=False,
        description="Foreign key to tasks table"
    )
    tag_id: uuid.UUID = Field(
        foreign_key="tags.id",
        primary_key=True,
        nullable=False,
        description="Foreign key to tags table"
    )
