"""Tag Model

SQLModel entity representing a user-defined tag for organizing tasks.
"""

import uuid
from datetime import datetime

from sqlmodel import Field, Index, SQLModel


class Tag(SQLModel, table=True):
    """Tag entity with user data isolation enforcement.

    Attributes:
        id: Primary key, UUID v4
        name: Tag name, required, max 50 characters
        user_id: Better Auth user ID (UUID) for strict data isolation
        created_at: Timestamp when tag was created

    Indexes:
        - Primary key on id (UUID)
        - Composite unique index on (user_id, name) to ensure tag names are unique per user
    """

    __tablename__ = "tags"
    __table_args__ = (
        Index("ix_tags_user_id_name", "user_id", "name", unique=True),
    )

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
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when tag was created"
    )
