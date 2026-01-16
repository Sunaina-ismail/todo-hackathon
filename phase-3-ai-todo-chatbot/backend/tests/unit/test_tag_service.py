"""Unit Tests for TagService

Tests for tag-related business logic including tag creation, assignment, and usage counts.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from src.services.tag_service import TagService
from src.models.task import Task
from src.models.tag import Tag
from src.models.task_tag import TaskTag
import uuid


@pytest.fixture(name="test_session")
def test_session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestGetOrCreateTag:
    """Test get_or_create_tag method."""

    def test_create_new_tag(self, test_session: Session):
        """Test creating a new tag returns Tag entity."""
        user_id = "test-user-123"
        tag_name = "urgent"

        tag = TagService.get_or_create_tag(test_session, user_id, tag_name)

        assert tag is not None
        assert tag.name == "urgent"
        assert tag.user_id == user_id
        assert tag.id is not None

    def test_get_existing_tag(self, test_session: Session):
        """Test getting existing tag returns same entity."""
        user_id = "test-user-123"
        tag_name = "work"

        # Create first time
        tag1 = TagService.get_or_create_tag(test_session, user_id, tag_name)
        tag1_id = tag1.id

        # Get second time (should return existing)
        tag2 = TagService.get_or_create_tag(test_session, user_id, tag_name)

        assert tag2.id == tag1_id
        assert tag2.name == tag_name
        assert tag2.user_id == user_id

    def test_tags_isolated_by_user(self, test_session: Session):
        """Test tags are isolated by user_id."""
        user1 = "user-111"
        user2 = "user-222"
        tag_name = "shared-name"

        # Create tag for user1
        tag1 = TagService.get_or_create_tag(test_session, user1, tag_name)

        # Create tag for user2 (should create separate entity)
        tag2 = TagService.get_or_create_tag(test_session, user2, tag_name)

        assert tag1.id != tag2.id
        assert tag1.name == tag2.name
        assert tag1.user_id == user1
        assert tag2.user_id == user2


class TestGetUserTagsWithUsage:
    """Test get_user_tags_with_usage method."""

    def test_empty_tags_for_new_user(self, test_session: Session):
        """Test returns empty list for user with no tags."""
        user_id = "new-user-999"

        tags = TagService.get_user_tags_with_usage(test_session, user_id)

        assert tags == []

    def test_returns_tags_with_usage_counts(self, test_session: Session):
        """Test returns tags with accurate usage counts."""
        user_id = "test-user-456"

        # Create tasks
        task1 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 1")
        task2 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 2")
        task3 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 3")
        test_session.add(task1)
        test_session.add(task2)
        test_session.add(task3)
        test_session.commit()

        # Create tags
        tag_urgent = TagService.get_or_create_tag(test_session, user_id, "urgent")
        tag_work = TagService.get_or_create_tag(test_session, user_id, "work")

        # Assign tags
        # urgent: used by task1, task2 (count = 2)
        # work: used by task1 only (count = 1)
        test_session.add(TaskTag(task_id=task1.id, tag_id=tag_urgent.id))
        test_session.add(TaskTag(task_id=task2.id, tag_id=tag_urgent.id))
        test_session.add(TaskTag(task_id=task1.id, tag_id=tag_work.id))
        test_session.commit()

        # Get tags with usage
        tags = TagService.get_user_tags_with_usage(test_session, user_id)

        assert len(tags) == 2

        # Find tags by name
        urgent_tag = next((t for t in tags if t.name == "urgent"), None)
        work_tag = next((t for t in tags if t.name == "work"), None)

        assert urgent_tag is not None
        assert urgent_tag.usage_count == 2

        assert work_tag is not None
        assert work_tag.usage_count == 1

    def test_tags_sorted_alphabetically(self, test_session: Session):
        """Test tags are sorted by name alphabetically."""
        user_id = "test-user-789"

        # Create task
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        # Create tags in random order
        tag_z = TagService.get_or_create_tag(test_session, user_id, "zebra")
        tag_a = TagService.get_or_create_tag(test_session, user_id, "alpha")
        tag_m = TagService.get_or_create_tag(test_session, user_id, "mike")

        # Assign all tags to task
        test_session.add(TaskTag(task_id=task.id, tag_id=tag_z.id))
        test_session.add(TaskTag(task_id=task.id, tag_id=tag_a.id))
        test_session.add(TaskTag(task_id=task.id, tag_id=tag_m.id))
        test_session.commit()

        # Get tags
        tags = TagService.get_user_tags_with_usage(test_session, user_id)
        tag_names = [t.name for t in tags]

        assert tag_names == ["alpha", "mike", "zebra"]

    def test_data_isolation_different_users(self, test_session: Session):
        """Test user A's tags are not returned for user B."""
        user_a = "user-aaa"
        user_b = "user-bbb"

        # Create task and tag for user A
        task_a = Task(id=uuid.uuid4(), user_id=user_a, title="Task A")
        test_session.add(task_a)
        test_session.commit()

        tag_a = TagService.get_or_create_tag(test_session, user_a, "user-a-tag")
        test_session.add(TaskTag(task_id=task_a.id, tag_id=tag_a.id))
        test_session.commit()

        # Get tags for user B
        tags_b = TagService.get_user_tags_with_usage(test_session, user_b)

        assert len(tags_b) == 0


class TestAssignTagsToTask:
    """Test assign_tags_to_task method."""

    def test_assign_single_tag(self, test_session: Session):
        """Test assigning single tag to task."""
        user_id = "test-user-111"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        TagService.assign_tags_to_task(test_session, task, ["urgent"])

        # Verify tag association
        tags = TagService.get_task_tags(test_session, task.id)
        assert len(tags) == 1
        assert "urgent" in tags

    def test_assign_multiple_tags(self, test_session: Session):
        """Test assigning multiple tags to task."""
        user_id = "test-user-222"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        TagService.assign_tags_to_task(test_session, task, ["urgent", "work", "important"])

        # Verify tag associations
        tags = TagService.get_task_tags(test_session, task.id)
        assert len(tags) == 3
        assert set(tags) == {"urgent", "work", "important"}

    def test_assign_duplicate_tags_deduplicates(self, test_session: Session):
        """Test assigning duplicate tags only creates one association."""
        user_id = "test-user-333"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        # Assign with duplicates
        TagService.assign_tags_to_task(test_session, task, ["urgent", "urgent", "urgent"])

        # Should only have one tag
        tags = TagService.get_task_tags(test_session, task.id)
        assert len(tags) == 1
        assert tags == ["urgent"]

    def test_reassign_tags_replaces_existing(self, test_session: Session):
        """Test reassigning tags replaces existing associations."""
        user_id = "test-user-444"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        # Initial assignment
        TagService.assign_tags_to_task(test_session, task, ["old-tag"])

        # Reassign with new tags
        TagService.assign_tags_to_task(test_session, task, ["new-tag-1", "new-tag-2"])

        # Should only have new tags
        tags = TagService.get_task_tags(test_session, task.id)
        assert len(tags) == 2
        assert set(tags) == {"new-tag-1", "new-tag-2"}
        assert "old-tag" not in tags

    def test_assign_empty_tag_list_removes_all_tags(self, test_session: Session):
        """Test assigning empty list removes all tag associations."""
        user_id = "test-user-555"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        # Initial assignment
        TagService.assign_tags_to_task(test_session, task, ["tag1", "tag2"])

        # Assign empty list
        TagService.assign_tags_to_task(test_session, task, [])

        # Should have no tags
        tags = TagService.get_task_tags(test_session, task.id)
        assert len(tags) == 0


class TestGetTaskTags:
    """Test get_task_tags method."""

    def test_get_tags_for_task_with_multiple_tags(self, test_session: Session):
        """Test retrieving tags for task returns all associated tags."""
        user_id = "test-user-666"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        # Assign tags
        TagService.assign_tags_to_task(test_session, task, ["a", "b", "c"])

        # Get tags
        tags = TagService.get_task_tags(test_session, task.id)

        assert len(tags) == 3
        assert set(tags) == {"a", "b", "c"}

    def test_get_tags_for_task_with_no_tags(self, test_session: Session):
        """Test retrieving tags for task with no tags returns empty list."""
        user_id = "test-user-777"
        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        tags = TagService.get_task_tags(test_session, task.id)

        assert tags == []
