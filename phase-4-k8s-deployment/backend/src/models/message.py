"""Message Model

SQLModel entity representing a single message within a conversation.
Supports user, assistant, and system messages with 2-day retention policy.
"""

import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, Index, SQLModel


class MessageRole(str, Enum):
    """Message role types"""
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(SQLModel, table=True):
    """Message entity with user data isolation enforcement.

    Represents a single message within a conversation (user, assistant, or system).
    Messages are automatically deleted after 2 days (retention policy).

    Attributes:
        id: Primary key, UUID v4
        conversation_id: Parent conversation UUID (foreign key)
        user_id: Better Auth user ID (string) for data isolation
        role: Message role (user, assistant, system)
        content: Message content (plain text or markdown), max 10,000 characters
        created_at: Timestamp when message was created (UTC)

    Business Rules:
        - 2-day retention: Messages older than 2 days automatically deleted
        - Role must be one of: user, assistant, system
        - Content maximum 10,000 characters (enforced in application layer)
        - Messages ordered by created_at ASC within a conversation
        - user_id must match conversation's user_id (enforced in service layer)
    """

    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_conversation_id", "conversation_id"),
        Index("ix_messages_user_id", "user_id"),
        Index("ix_messages_created_at", "created_at"),
        Index("ix_messages_conversation_created", "conversation_id", "created_at"),
    )

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique message identifier (UUID v4)"
    )
    conversation_id: uuid.UUID = Field(
        nullable=False,
        foreign_key="conversations.id",
        description="Parent conversation UUID (foreign key)"
    )
    user_id: str = Field(
        nullable=False,
        description="Better Auth user ID (string) for data isolation"
    )
    role: MessageRole = Field(
        nullable=False,
        description="Message role: user, assistant, or system"
    )
    content: str = Field(
        nullable=False,
        description="Message content (plain text or markdown), max 10,000 characters"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when message was created (UTC)"
    )
