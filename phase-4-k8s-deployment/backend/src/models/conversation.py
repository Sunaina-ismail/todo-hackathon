"""Conversation Model

SQLModel entity representing a chat conversation between a user and the AI assistant.
Supports conversation persistence for context maintenance across sessions.
"""

import uuid
from datetime import datetime

from sqlmodel import Field, Index, SQLModel


class Conversation(SQLModel, table=True):
    """Conversation entity with user data isolation enforcement.

    Represents a distinct chat thread between a user and the AI assistant.
    Supports ChatKit protocol with thread_id for session management.

    Attributes:
        id: Primary key, UUID v4
        user_id: Better Auth user ID (string) for strict data isolation
        thread_id: ChatKit thread identifier, unique across all conversations
        title: Conversation title, default "New Conversation"
        is_active: Active status for archiving (default True)
        created_at: Timestamp when conversation was created (UTC)
        updated_at: Timestamp when conversation was last updated (UTC)

    Business Rules:
        - Maximum 100 conversations per user (enforced in service layer)
        - When limit exceeded, delete oldest conversation by created_at (FIFO)
        - Archived conversations (is_active=false) excluded from default queries
        - Updated timestamp refreshed when new message added
    """

    __tablename__ = "conversations"
    __table_args__ = (
        Index("ix_conversations_user_id", "user_id"),
        Index("ix_conversations_thread_id", "thread_id", unique=True),
        Index("ix_conversations_is_active", "is_active"),
        Index("ix_conversations_created_at", "created_at"),
        Index("ix_conversations_updated_at", "updated_at"),
        Index("ix_conversations_user_created", "user_id", "created_at"),
    )

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique conversation identifier (UUID v4)"
    )
    user_id: str = Field(
        nullable=False,
        description="Better Auth user ID (string) for data isolation"
    )
    thread_id: str = Field(
        nullable=False,
        description="ChatKit thread identifier, unique across all conversations"
    )
    title: str = Field(
        default="New Conversation",
        max_length=500,
        nullable=False,
        description="Conversation title, max 500 characters"
    )
    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Active status for archiving (default True)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when conversation was created (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when conversation was last updated (UTC)"
    )
