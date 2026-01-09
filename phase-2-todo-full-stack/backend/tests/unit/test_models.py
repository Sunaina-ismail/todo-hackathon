"""Unit Tests for Database Models

Tests for Task, Tag, and TaskTag models with validation and constraints.
"""

import pytest
from datetime import datetime, date
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
import uuid
from src.models.task import Task, PriorityType
from src.models.tag import Tag
from src.models.task_tag import TaskTag


@pytest.fixture(name="test_session")
def test_session_fixture():
    """Create a test database session with in-memory SQLite."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestTaskModel:
    """Test Task model validation and constraints."""

    def test_task_model_creation_with_defaults(self, test_session: Session):
        """Test creating a task with default values."""
        task = Task(
            user_id="test-user-123",
            title="Test Task"
        )
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)

        assert task.id is not None
        assert isinstance(task.id, uuid.UUID)
        assert task.user_id == "test-user-123"
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False
        assert task.priority == PriorityType.Medium  # Default priority
        assert task.due_date is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_model_with_all_fields(self, test_session: Session):
        """Test creating a task with all fields populated."""
        task_id = uuid.uuid4()
        due_date = date(2025, 12, 31)

        task = Task(
            id=task_id,
            user_id="test-user-123",
            title="Complete Project",
            description="Finish the backend implementation",
            completed=False,
            priority=PriorityType.High,
            due_date=due_date
        )
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)

        assert task.id == task_id
        assert task.user_id == "test-user-123"
        assert task.title == "Complete Project"
        assert task.description == "Finish the backend implementation"
        assert task.completed is False
        assert task.priority == PriorityType.High
        assert task.due_date == due_date

    def test_task_priority_enum_values(self, test_session: Session):
        """Test all priority enum values are valid."""
        # Test High priority
        task_high = Task(
            user_id="test-user-123",
            title="High Priority Task",
            priority=PriorityType.High
        )
        test_session.add(task_high)
        test_session.commit()
        test_session.refresh(task_high)
        assert task_high.priority == PriorityType.High

        # Test Medium priority
        task_medium = Task(
            user_id="test-user-123",
            title="Medium Priority Task",
            priority=PriorityType.Medium
        )
        test_session.add(task_medium)
        test_session.commit()
        test_session.refresh(task_medium)
        assert task_medium.priority == PriorityType.Medium

        # Test Low priority
        task_low = Task(
            user_id="test-user-123",
            title="Low Priority Task",
            priority=PriorityType.Low
        )
        test_session.add(task_low)
        test_session.commit()
        test_session.refresh(task_low)
        assert task_low.priority == PriorityType.Low

    def test_task_title_max_length(self, test_session: Session):
        """Test task title length constraint (max 200 chars)."""
        # Valid: exactly 200 characters
        valid_title = "A" * 200
        task = Task(user_id="test-user-123", title=valid_title)
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)
        assert len(task.title) == 200

        # Note: SQLite doesn't enforce max_length, but Pydantic validation does
        # This is validated at the schema level in TaskCreate/TaskUpdate

    def test_task_description_max_length(self, test_session: Session):
        """Test task description length constraint (max 1000 chars)."""
        # Valid: exactly 1000 characters
        valid_description = "B" * 1000
        task = Task(
            user_id="test-user-123",
            title="Test Task",
            description=valid_description
        )
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)
        assert len(task.description) == 1000

    def test_task_completed_default_false(self, test_session: Session):
        """Test that completed defaults to False."""
        task = Task(user_id="test-user-123", title="Test Task")
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)
        assert task.completed is False

    def test_task_user_isolation(self, test_session: Session):
        """Test that tasks are properly isolated by user_id."""
        # Create tasks for different users
        task1 = Task(user_id="user-1", title="User 1 Task")
        task2 = Task(user_id="user-2", title="User 2 Task")

        test_session.add(task1)
        test_session.add(task2)
        test_session.commit()

        # Verify both tasks have different user_ids
        assert task1.user_id != task2.user_id
        assert task1.user_id == "user-1"
        assert task2.user_id == "user-2"


class TestTagModel:
    """Test Tag model validation and constraints."""

    def test_tag_model_creation(self, test_session: Session):
        """Test creating a tag with required fields."""
        tag = Tag(
            name="urgent",
            user_id="test-user-123"
        )
        test_session.add(tag)
        test_session.commit()
        test_session.refresh(tag)

        assert tag.id is not None
        assert isinstance(tag.id, uuid.UUID)
        assert tag.name == "urgent"
        assert tag.user_id == "test-user-123"
        assert isinstance(tag.created_at, datetime)

    def test_tag_name_max_length(self, test_session: Session):
        """Test tag name length constraint (max 50 chars)."""
        # Valid: exactly 50 characters
        valid_name = "A" * 50
        tag = Tag(name=valid_name, user_id="test-user-123")
        test_session.add(tag)
        test_session.commit()
        test_session.refresh(tag)
        assert len(tag.name) == 50

    def test_tag_unique_per_user(self, test_session: Session):
        """Test that tag names are unique per user (composite unique constraint)."""
        # Create first tag
        tag1 = Tag(name="urgent", user_id="test-user-123")
        test_session.add(tag1)
        test_session.commit()

        # Try to create duplicate tag for same user
        tag2 = Tag(name="urgent", user_id="test-user-123")
        test_session.add(tag2)

        with pytest.raises(Exception):  # IntegrityError or similar
            test_session.commit()

    def test_tag_same_name_different_users(self, test_session: Session):
        """Test that different users can have tags with the same name."""
        # Create tag for user 1
        tag1 = Tag(name="work", user_id="user-1")
        test_session.add(tag1)
        test_session.commit()

        # Create tag with same name for user 2 (should succeed)
        tag2 = Tag(name="work", user_id="user-2")
        test_session.add(tag2)
        test_session.commit()
        test_session.refresh(tag2)

        assert tag1.name == tag2.name == "work"
        assert tag1.user_id != tag2.user_id


class TestTaskTagModel:
    """Test TaskTag junction table model."""

    def test_task_tag_creation(self, test_session: Session):
        """Test creating a task-tag association."""
        # Create task and tag first
        task = Task(user_id="test-user-123", title="Test Task")
        tag = Tag(name="urgent", user_id="test-user-123")
        test_session.add(task)
        test_session.add(tag)
        test_session.commit()
        test_session.refresh(task)
        test_session.refresh(tag)

        # Create association
        task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
        test_session.add(task_tag)
        test_session.commit()

        assert task_tag.task_id == task.id
        assert task_tag.tag_id == tag.id

    def test_task_tag_composite_primary_key(self, test_session: Session):
        """Test that task_tag has composite primary key (task_id, tag_id)."""
        # Create task and tag
        task = Task(user_id="test-user-123", title="Test Task")
        tag = Tag(name="urgent", user_id="test-user-123")
        test_session.add(task)
        test_session.add(tag)
        test_session.commit()
        test_session.refresh(task)
        test_session.refresh(tag)

        # Create association
        task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
        test_session.add(task_tag)
        test_session.commit()

        # Try to create duplicate association (should fail)
        task_tag_duplicate = TaskTag(task_id=task.id, tag_id=tag.id)
        test_session.add(task_tag_duplicate)

        with pytest.raises(Exception):  # IntegrityError
            test_session.commit()

    def test_task_tag_multiple_tags_per_task(self, test_session: Session):
        """Test that a task can have multiple tags."""
        # Create task and multiple tags
        task = Task(user_id="test-user-123", title="Test Task")
        tag1 = Tag(name="urgent", user_id="test-user-123")
        tag2 = Tag(name="work", user_id="test-user-123")
        tag3 = Tag(name="important", user_id="test-user-123")

        test_session.add(task)
        test_session.add(tag1)
        test_session.add(tag2)
        test_session.add(tag3)
        test_session.commit()
        test_session.refresh(task)
        test_session.refresh(tag1)
        test_session.refresh(tag2)
        test_session.refresh(tag3)

        # Create associations
        task_tag1 = TaskTag(task_id=task.id, tag_id=tag1.id)
        task_tag2 = TaskTag(task_id=task.id, tag_id=tag2.id)
        task_tag3 = TaskTag(task_id=task.id, tag_id=tag3.id)

        test_session.add(task_tag1)
        test_session.add(task_tag2)
        test_session.add(task_tag3)
        test_session.commit()

        # All associations should exist
        assert task_tag1.task_id == task.id
        assert task_tag2.task_id == task.id
        assert task_tag3.task_id == task.id


class TestPriorityTypeEnum:
    """Test PriorityType enum."""

    def test_priority_enum_values(self):
        """Test that PriorityType has correct enum values."""
        assert PriorityType.High.value == "High"
        assert PriorityType.Medium.value == "Medium"
        assert PriorityType.Low.value == "Low"

    def test_priority_enum_string_representation(self):
        """Test priority enum string representation."""
        assert str(PriorityType.High) == "PriorityType.High"
        assert PriorityType.High.value == "High"

    def test_priority_enum_comparison(self):
        """Test priority enum comparison."""
        assert PriorityType.High == PriorityType.High
        assert PriorityType.Medium == PriorityType.Medium
        assert PriorityType.Low == PriorityType.Low
        assert PriorityType.High != PriorityType.Medium
        assert PriorityType.Medium != PriorityType.Low
