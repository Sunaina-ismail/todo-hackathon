"""Unit Tests for ChatKit Store Implementations

Tests for DatabaseStore and MemoryStore with mocked database connections.
Validates conversation persistence, message ordering, and user isolation.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import uuid

from src.services.chatkit_store import DatabaseStore, MemoryStore
from src.models.conversation import Conversation
from src.models.message import Message, MessageRole


class TestDatabaseStore:
    """Test DatabaseStore implementation."""

    @pytest.mark.asyncio
    async def test_create_thread_success(self):
        """Test successful thread creation."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session and generator
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_result.scalar_one_or_none.return_value = None  # Thread doesn't exist
        mock_session.execute.return_value = mock_result

        # Mock conversation object
        mock_conversation = Conversation(
            id=1,
            user_id="user123",
            thread_id=thread_id,
            title="New Conversation",
            created_at=datetime(2026, 1, 15, 10, 0, 0),
            updated_at=datetime(2026, 1, 15, 10, 0, 0),
        )

        # Mock async generator
        async def mock_async_gen():
            yield mock_session

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            mock_get_session.return_value = mock_async_gen()

            # Mock refresh to set conversation attributes
            async def mock_refresh(obj):
                obj.id = mock_conversation.id
                obj.created_at = mock_conversation.created_at
                obj.updated_at = mock_conversation.updated_at

            mock_session.refresh = mock_refresh

            result = await store.create_thread(thread_id, "New Conversation")

            assert result["id"] == thread_id
            assert result["title"] == "New Conversation"
            assert "created_at" in result
            assert "updated_at" in result

            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_thread_duplicate(self):
        """Test creating duplicate thread raises ValueError."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_result.scalar_one_or_none.return_value = Mock()  # Thread exists
        mock_session.execute.return_value = mock_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            with pytest.raises(ValueError, match="already exists"):
                await store.create_thread(thread_id)

    @pytest.mark.asyncio
    async def test_get_thread_success(self):
        """Test successful thread retrieval."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_conversation = Conversation(
            id=1,
            user_id="user123",
            thread_id=thread_id,
            title="Test Conversation",
            created_at=datetime(2026, 1, 15, 10, 0, 0),
            updated_at=datetime(2026, 1, 15, 11, 0, 0),
        )
        mock_result.scalar_one_or_none.return_value = mock_conversation
        mock_session.execute.return_value = mock_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            result = await store.get_thread(thread_id)

            assert result is not None
            assert result["id"] == thread_id
            assert result["title"] == "Test Conversation"
            assert result["created_at"] == "2026-01-15T10:00:00"
            assert result["updated_at"] == "2026-01-15T11:00:00"

    @pytest.mark.asyncio
    async def test_get_thread_not_found(self):
        """Test get_thread returns None for non-existent thread."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_nonexistent"

        # Mock async session
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            result = await store.get_thread(thread_id)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_thread_user_isolation(self):
        """Test get_thread enforces user isolation."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session - returns None for wrong user
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            result = await store.get_thread(thread_id)

            assert result is None

    @pytest.mark.asyncio
    async def test_add_message_success(self):
        """Test successful message addition."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session
        mock_session = AsyncMock()

        # Mock conversation lookup
        mock_conv_result = Mock()  # Regular Mock, not AsyncMock
        mock_conversation = Conversation(
            id=1,
            user_id="user123",
            thread_id=thread_id,
            title="Test Conversation",
            created_at=datetime(2026, 1, 15, 10, 0, 0),
            updated_at=datetime(2026, 1, 15, 10, 0, 0),
        )
        mock_conv_result.scalar_one_or_none.return_value = mock_conversation
        mock_session.execute.return_value = mock_conv_result

        # Mock message object
        mock_message = Message(
            id=uuid.uuid4(),
            conversation_id=1,
            user_id="user123",
            role=MessageRole.user,
            content="Test message",
            created_at=datetime(2026, 1, 15, 10, 0, 0),
        )

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            # Mock refresh to set message attributes
            async def mock_refresh(obj):
                if isinstance(obj, Message):
                    obj.id = mock_message.id
                    obj.created_at = mock_message.created_at

            mock_session.refresh = mock_refresh

            result = await store.add_message(thread_id, "user", "Test message")

            assert result["role"] == "user"
            assert result["content"] == "Test message"
            assert "id" in result
            assert "created_at" in result

            mock_session.add.assert_called()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_message_thread_not_found(self):
        """Test add_message raises ValueError for non-existent thread."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_nonexistent"

        # Mock async session
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            with pytest.raises(ValueError, match="Thread .* not found"):
                await store.add_message(thread_id, "user", "Test message")

    @pytest.mark.asyncio
    async def test_add_message_invalid_role(self):
        """Test add_message raises ValueError for invalid role."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session
        mock_session = AsyncMock()
        mock_conv_result = AsyncMock()
        mock_conversation = Conversation(
            id=1,
            user_id="user123",
            thread_id=thread_id,
            title="Test Conversation",
        )
        mock_conv_result.scalar_one_or_none.return_value = mock_conversation
        mock_session.execute.return_value = mock_conv_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            with pytest.raises(ValueError, match="Invalid role"):
                await store.add_message(thread_id, "invalid_role", "Test message")

    @pytest.mark.asyncio
    async def test_get_messages_success(self):
        """Test successful message retrieval."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session
        mock_session = AsyncMock()

        # Mock conversation lookup
        mock_conv_result = Mock()  # Regular Mock, not AsyncMock
        mock_conversation = Conversation(
            id=1,
            user_id="user123",
            thread_id=thread_id,
            title="Test Conversation",
        )
        mock_conv_result.scalar_one_or_none.return_value = mock_conversation

        # Mock messages lookup
        mock_msg_result = Mock()  # Regular Mock, not AsyncMock
        mock_messages = [
            Message(
                id=uuid.uuid4(),
                conversation_id=1,
                user_id="user123",
                role=MessageRole.user,
                content="User message",
                created_at=datetime(2026, 1, 15, 10, 0, 0),
            ),
            Message(
                id=uuid.uuid4(),
                conversation_id=1,
                user_id="user123",
                role=MessageRole.assistant,
                content="Assistant message",
                created_at=datetime(2026, 1, 15, 10, 0, 5),
            ),
        ]
        mock_msg_result.scalars.return_value.all.return_value = mock_messages

        # Setup execute to return different results for different queries
        mock_session.execute.side_effect = [mock_conv_result, mock_msg_result]

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            result = await store.get_messages(thread_id)

            assert len(result) == 2
            assert result[0]["role"] == "user"
            assert result[0]["content"] == "User message"
            assert result[1]["role"] == "assistant"
            assert result[1]["content"] == "Assistant message"

    @pytest.mark.asyncio
    async def test_get_messages_empty_thread(self):
        """Test get_messages returns empty list for thread with no messages."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_abc123"

        # Mock async session
        mock_session = AsyncMock()

        # Mock conversation lookup
        mock_conv_result = Mock()  # Regular Mock, not AsyncMock
        mock_conversation = Conversation(
            id=1,
            user_id="user123",
            thread_id=thread_id,
            title="Test Conversation",
        )
        mock_conv_result.scalar_one_or_none.return_value = mock_conversation

        # Mock empty messages
        mock_msg_result = Mock()  # Regular Mock, not AsyncMock
        mock_msg_result.scalars.return_value.all.return_value = []

        mock_session.execute.side_effect = [mock_conv_result, mock_msg_result]

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            result = await store.get_messages(thread_id)

            assert result == []

    @pytest.mark.asyncio
    async def test_get_messages_nonexistent_thread(self):
        """Test get_messages returns empty list for non-existent thread."""
        store = DatabaseStore(user_id="user123")
        thread_id = "thread_nonexistent"

        # Mock async session
        mock_session = AsyncMock()
        mock_result = Mock()  # Regular Mock, not AsyncMock
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with patch("src.services.chatkit_store.get_async_session") as mock_get_session:
            async def async_gen():
                yield mock_session

            mock_get_session.return_value = async_gen()

            result = await store.get_messages(thread_id)

            assert result == []


class TestMemoryStore:
    """Test MemoryStore implementation."""

    @pytest.mark.asyncio
    async def test_create_thread_success(self):
        """Test successful thread creation."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        result = await store.create_thread(thread_id, "Test Conversation")

        assert result["id"] == thread_id
        assert result["title"] == "Test Conversation"
        assert "created_at" in result
        assert "updated_at" in result

    @pytest.mark.asyncio
    async def test_create_thread_duplicate(self):
        """Test creating duplicate thread raises ValueError."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id)

        with pytest.raises(ValueError, match="already exists"):
            await store.create_thread(thread_id)

    @pytest.mark.asyncio
    async def test_get_thread_success(self):
        """Test successful thread retrieval."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id, "Test Conversation")
        result = await store.get_thread(thread_id)

        assert result is not None
        assert result["id"] == thread_id
        assert result["title"] == "Test Conversation"

    @pytest.mark.asyncio
    async def test_get_thread_not_found(self):
        """Test get_thread returns None for non-existent thread."""
        store = MemoryStore(user_id="user123")

        result = await store.get_thread("thread_nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_add_message_success(self):
        """Test successful message addition."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id)
        result = await store.add_message(thread_id, "user", "Test message")

        assert result["role"] == "user"
        assert result["content"] == "Test message"
        assert "id" in result
        assert "created_at" in result

    @pytest.mark.asyncio
    async def test_add_message_thread_not_found(self):
        """Test add_message raises ValueError for non-existent thread."""
        store = MemoryStore(user_id="user123")

        with pytest.raises(ValueError, match="Thread .* not found"):
            await store.add_message("thread_nonexistent", "user", "Test message")

    @pytest.mark.asyncio
    async def test_add_message_invalid_role(self):
        """Test add_message raises ValueError for invalid role."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id)

        with pytest.raises(ValueError, match="Invalid role"):
            await store.add_message(thread_id, "invalid_role", "Test message")

    @pytest.mark.asyncio
    async def test_get_messages_success(self):
        """Test successful message retrieval."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id)
        await store.add_message(thread_id, "user", "User message")
        await store.add_message(thread_id, "assistant", "Assistant message")

        result = await store.get_messages(thread_id)

        assert len(result) == 2
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "User message"
        assert result[1]["role"] == "assistant"
        assert result[1]["content"] == "Assistant message"

    @pytest.mark.asyncio
    async def test_get_messages_empty_thread(self):
        """Test get_messages returns empty list for thread with no messages."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id)
        result = await store.get_messages(thread_id)

        assert result == []

    @pytest.mark.asyncio
    async def test_get_messages_nonexistent_thread(self):
        """Test get_messages returns empty list for non-existent thread."""
        store = MemoryStore(user_id="user123")

        result = await store.get_messages("thread_nonexistent")

        assert result == []

    @pytest.mark.asyncio
    async def test_message_ordering(self):
        """Test messages are returned in creation order."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        await store.create_thread(thread_id)
        await store.add_message(thread_id, "user", "First message")
        await store.add_message(thread_id, "assistant", "Second message")
        await store.add_message(thread_id, "user", "Third message")

        result = await store.get_messages(thread_id)

        assert len(result) == 3
        assert result[0]["content"] == "First message"
        assert result[1]["content"] == "Second message"
        assert result[2]["content"] == "Third message"

    @pytest.mark.asyncio
    async def test_thread_updated_at_changes(self):
        """Test thread updated_at changes when messages are added."""
        store = MemoryStore(user_id="user123")
        thread_id = "thread_abc123"

        thread = await store.create_thread(thread_id)
        original_updated_at = thread["updated_at"]

        # Add message (should update thread's updated_at)
        await store.add_message(thread_id, "user", "Test message")

        updated_thread = await store.get_thread(thread_id)
        assert updated_thread["updated_at"] != original_updated_at
