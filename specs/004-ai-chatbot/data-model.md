# Data Model: AI-Powered Conversational Task Management

**Feature**: 004-ai-chatbot
**Date**: 2026-01-12
**Phase**: Phase 1 - Data Model Design

## Overview

This document defines the database schema for conversation persistence in the AI-powered task management chatbot. The schema supports stateless architecture with all conversation history stored in the database, enabling context maintenance across sessions and user isolation.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User (Phase II)                      │
│  - id: string (Better Auth user ID)                         │
│  - email: string                                             │
│  - name: string                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Conversation (NEW)                      │
│  - id: UUID (PK)                                            │
│  - user_id: string (FK, indexed)                            │
│  - thread_id: string (unique, indexed)                      │
│  - title: string                                             │
│  - is_active: boolean (indexed)                             │
│  - created_at: datetime (indexed)                           │
│  - updated_at: datetime (indexed)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Message (NEW)                          │
│  - id: UUID (PK)                                            │
│  - conversation_id: UUID (FK, indexed)                      │
│  - user_id: string (indexed)                                │
│  - role: string (user|assistant|system)                     │
│  - content: text                                             │
│  - created_at: datetime (indexed)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Entities

### 1. Conversation

Represents a distinct chat thread between a user and the AI assistant.

#### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique conversation identifier |
| `user_id` | String | NOT NULL, INDEXED, FK → User | Owner of the conversation |
| `thread_id` | String | NOT NULL, UNIQUE, INDEXED | ChatKit thread identifier |
| `title` | String(500) | NOT NULL, DEFAULT "New Conversation" | Conversation title (auto-generated or user-set) |
| `is_active` | Boolean | NOT NULL, DEFAULT true, INDEXED | Active status for archiving |
| `created_at` | DateTime | NOT NULL, INDEXED | Conversation creation timestamp (UTC) |
| `updated_at` | DateTime | NOT NULL, INDEXED | Last message timestamp (UTC) |

#### Relationships

- **User** (1:N): One user can have many conversations
- **Messages** (1:N): One conversation contains many messages (cascade delete)

#### Indexes

```sql
-- Primary key index (automatic)
CREATE INDEX idx_conversations_pk ON conversations(id);

-- User lookup index
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- ChatKit thread lookup index
CREATE UNIQUE INDEX idx_conversations_thread_id ON conversations(thread_id);

-- Active status index (for archiving queries)
CREATE INDEX idx_conversations_is_active ON conversations(is_active);

-- Creation timestamp index (for FIFO cleanup)
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- Update timestamp index (for sorting)
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);

-- Composite index for user's sorted conversations
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at DESC);
```

#### Business Rules

1. **100-Conversation Limit**: Each user can have maximum 100 conversations
   - Enforced in service layer (not database constraint)
   - When limit exceeded, delete oldest conversation by `created_at` (FIFO)
   - Deletion cascades to all messages in that conversation

2. **Title Generation**:
   - Default title: "New Conversation"
   - Auto-generated from first user message (optional, disabled for performance)
   - User can manually set title via ChatKit UI

3. **Active Status**:
   - `is_active=true`: Normal conversation
   - `is_active=false`: Archived conversation (no messages for 30+ days)
   - Archived conversations excluded from default list queries

4. **Updated Timestamp**:
   - Updated automatically when new message added
   - Used for sorting conversations by recency

#### Validation Rules

- `user_id`: Must match authenticated user from JWT
- `thread_id`: Must be unique across all conversations
- `title`: Maximum 500 characters
- `created_at`, `updated_at`: Must be UTC timestamps

---

### 2. Message

Represents a single message within a conversation (user, assistant, or system).

#### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique message identifier |
| `conversation_id` | UUID | NOT NULL, INDEXED, FK → Conversation | Parent conversation |
| `user_id` | String | NOT NULL, INDEXED | Message owner (for isolation) |
| `role` | String | NOT NULL | Message role: "user", "assistant", "system" |
| `content` | Text | NOT NULL | Message content (markdown supported) |
| `created_at` | DateTime | NOT NULL, INDEXED | Message timestamp (UTC) |

#### Relationships

- **Conversation** (N:1): Many messages belong to one conversation
- **User** (N:1): Many messages belong to one user (for isolation)

#### Indexes

```sql
-- Primary key index (automatic)
CREATE INDEX idx_messages_pk ON messages(id);

-- Conversation lookup index
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

-- User isolation index
CREATE INDEX idx_messages_user_id ON messages(user_id);

-- Timestamp index (for retention cleanup)
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Composite index for ordered conversation messages
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
```

#### Business Rules

1. **2-Day Retention**: Messages older than 2 days automatically deleted
   - Background task runs daily
   - Deletes messages where `created_at < NOW() - INTERVAL '2 days'`
   - Orphaned conversations (no messages) marked as inactive

2. **Role Values**:
   - `user`: Message from the user
   - `assistant`: Message from the AI agent
   - `system`: System messages (context, instructions)

3. **Content Format**:
   - Plain text or markdown
   - Maximum size: 10,000 characters (enforced in application layer)
   - No HTML allowed (sanitized on input)

4. **Ordering**:
   - Messages always ordered by `created_at` ASC within a conversation
   - Newest messages appear at the bottom (chat convention)

#### Validation Rules

- `conversation_id`: Must reference existing conversation
- `user_id`: Must match conversation's user_id (enforced in service layer)
- `role`: Must be one of: "user", "assistant", "system"
- `content`: Required, non-empty, max 10,000 characters
- `created_at`: Must be UTC timestamp

---

## Database Migration

### Alembic Migration Script

```python
"""Add conversation and message tables for AI chatbot

Revision ID: xxx_add_conversation_message
Revises: previous_revision
Create Date: 2026-01-12
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'xxx_add_conversation_message'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('thread_id', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('title', sa.String(500), nullable=False, server_default='New Conversation'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true', index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()'))
    )

    # Create composite indexes for conversations
    op.create_index('idx_conversations_user_created', 'conversations', ['user_id', 'created_at'], postgresql_ops={'created_at': 'DESC'})

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE')
    )

    # Create composite index for messages
    op.create_index('idx_messages_conversation_created', 'messages', ['conversation_id', 'created_at'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

## SQLModel Definitions

### Conversation Model

```python
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

class Conversation(SQLModel, table=True):
    """Conversation entity representing a chat thread."""
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(nullable=False, index=True)
    thread_id: str = Field(nullable=False, unique=True, index=True)
    title: str = Field(default="New Conversation", max_length=500, nullable=False)
    is_active: bool = Field(default=True, nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    # Relationships
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )
```

### Message Model

```python
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

class Message(SQLModel, table=True):
    """Message entity representing a single message in a conversation."""
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    user_id: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False)  # "user" | "assistant" | "system"
    content: str = Field(nullable=False, sa_column_kwargs={"type_": sa.Text})
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

---

## Query Patterns

### Common Queries

**Get user's active conversations (sorted by recency)**:
```python
conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .where(Conversation.is_active == True)
    .order_by(Conversation.updated_at.desc())
    .limit(50)
).all()
```

**Get conversation with messages**:
```python
conversation = session.exec(
    select(Conversation)
    .where(Conversation.thread_id == thread_id)
    .where(Conversation.user_id == user_id)
).first()

messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation.id)
    .order_by(Message.created_at.asc())
).all()
```

**Delete old messages (retention policy)**:
```python
from datetime import datetime, timedelta

cutoff_date = datetime.utcnow() - timedelta(days=2)
session.exec(
    delete(Message)
    .where(Message.created_at < cutoff_date)
)
session.commit()
```

**Enforce 100-conversation limit**:
```python
# Count user's conversations
count = session.exec(
    select(func.count(Conversation.id))
    .where(Conversation.user_id == user_id)
).one()

if count >= 100:
    # Delete oldest conversation
    oldest = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .limit(1)
    ).first()
    session.delete(oldest)  # Cascades to messages
    session.commit()
```

---

## Performance Considerations

### Index Strategy

1. **User Isolation**: `user_id` indexed on both tables for fast filtering
2. **Thread Lookup**: `thread_id` unique index for O(1) conversation lookup
3. **Temporal Queries**: `created_at` and `updated_at` indexed for sorting and retention cleanup
4. **Composite Indexes**: `(user_id, created_at)` for optimized user conversation queries

### Query Optimization

1. **Lazy Loading**: Use `selectin` loading for relationships to avoid N+1 queries
2. **Pagination**: Always use `LIMIT` and `OFFSET` for conversation lists
3. **Retention Cleanup**: Run as background task during low-traffic hours
4. **Connection Pooling**: Reuse database connections via SQLModel session factory

### Storage Estimates

**Assumptions**:
- 1,000 active users
- Average 10 conversations per user
- Average 20 messages per conversation
- Average message size: 200 characters

**Storage Calculation**:
- Conversations: 1,000 users × 10 conversations × 1 KB = 10 MB
- Messages: 1,000 users × 10 conversations × 20 messages × 0.5 KB = 100 MB
- **Total**: ~110 MB for active data
- With 2-day retention, storage remains bounded

---

## Security & Isolation

### User Isolation Enforcement

1. **Query Filtering**: All queries MUST filter by `user_id`
2. **Service Layer**: Validation in service methods before database access
3. **MCP Tools**: Every tool receives `user_id` from JWT and validates
4. **Foreign Keys**: No direct foreign key to User table (Better Auth owns users)

### Data Privacy

1. **Encryption**: Database connection uses SSL/TLS (Neon default)
2. **Retention**: Messages auto-deleted after 2 days
3. **Archiving**: Inactive conversations archived after 30 days
4. **Deletion**: User deletion cascades to all conversations and messages

---

## Testing Strategy

### Unit Tests

- Test Conversation and Message model creation
- Test relationship loading (conversation.messages)
- Test validation rules (max length, required fields)

### Integration Tests

- Test conversation creation and retrieval
- Test message ordering within conversation
- Test user isolation (cannot access other users' data)
- Test retention policy (old messages deleted)
- Test 100-conversation limit enforcement

### Performance Tests

- Test query performance with 1,000+ conversations
- Test message retrieval with 100+ messages per conversation
- Test concurrent conversation creation

---

## Summary

The data model supports stateless conversation persistence with:
- ✅ User isolation via `user_id` filtering
- ✅ ChatKit protocol compatibility via `thread_id`
- ✅ Efficient queries via strategic indexing
- ✅ Storage optimization via retention policies
- ✅ Scalability via bounded storage and connection pooling

All schema design aligns with Phase III constitutional requirements for stateless architecture and user isolation.
