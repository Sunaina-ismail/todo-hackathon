"""Unit Tests for Task Search and Filter Logic

Tests for search query builder, priority filtering, tags filtering, and sorting logic.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from sqlmodel.pool import StaticPool
from src.services.task_service import TaskService
from src.services.tag_service import TagService
from src.models.task import Task, PriorityType
from datetime import date
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


class TestSearchQueryBuilder:
    """Test search query logic."""

    def test_search_matches_title(self, test_session: Session):
        """Test search query matches task title."""
        user_id = "test-user-search"

        # Create tasks
        task1 = Task(id=uuid.uuid4(), user_id=user_id, title="Buy groceries")
        task2 = Task(id=uuid.uuid4(), user_id=user_id, title="Call dentist")
        task3 = Task(id=uuid.uuid4(), user_id=user_id, title="Grocery shopping list")
        test_session.add_all([task1, task2, task3])
        test_session.commit()

        # Search for "grocery"
        results = TaskService.get_tasks_by_user(
            test_session, user_id, search_text="grocery"
        )

        assert len(results) == 2
        titles = {t.title for t in results}
        assert "Buy groceries" in titles
        assert "Grocery shopping list" in titles

    def test_search_matches_description(self, test_session: Session):
        """Test search query matches task description."""
        user_id = "test-user-desc"

        # Create tasks
        task1 = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Task 1",
            description="Important meeting notes",
        )
        task2 = Task(
            id=uuid.uuid4(), user_id=user_id, title="Task 2", description="Casual chat"
        )
        test_session.add_all([task1, task2])
        test_session.commit()

        # Search for "meeting"
        results = TaskService.get_tasks_by_user(
            test_session, user_id, search_text="meeting"
        )

        assert len(results) == 1
        assert results[0].description == "Important meeting notes"

    def test_search_case_insensitive(self, test_session: Session):
        """Test search is case-insensitive."""
        user_id = "test-user-case"

        task = Task(id=uuid.uuid4(), user_id=user_id, title="URGENT Task")
        test_session.add(task)
        test_session.commit()

        # Search with lowercase
        results = TaskService.get_tasks_by_user(
            test_session, user_id, search_text="urgent"
        )

        assert len(results) == 1
        assert results[0].title == "URGENT Task"

    def test_search_empty_returns_all(self, test_session: Session):
        """Test empty search returns all tasks."""
        user_id = "test-user-empty"

        task1 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 1")
        task2 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 2")
        test_session.add_all([task1, task2])
        test_session.commit()

        results = TaskService.get_tasks_by_user(test_session, user_id, search_text="")

        assert len(results) == 2


class TestPriorityFilter:
    """Test priority filter logic."""

    def test_filter_by_priority_high(self, test_session: Session):
        """Test filtering by High priority."""
        user_id = "test-user-pri"

        task_high = Task(
            id=uuid.uuid4(), user_id=user_id, title="High", priority=PriorityType.High
        )
        task_medium = Task(
            id=uuid.uuid4(), user_id=user_id, title="Medium", priority=PriorityType.Medium
        )
        test_session.add_all([task_high, task_medium])
        test_session.commit()

        results = TaskService.get_tasks_by_user(
            test_session, user_id, priority_filter="High"
        )

        assert len(results) == 1
        assert results[0].priority == PriorityType.High

    def test_filter_by_priority_all_returns_all(self, test_session: Session):
        """Test priority filter 'all' returns all priorities."""
        user_id = "test-user-all"

        task_high = Task(
            id=uuid.uuid4(), user_id=user_id, title="High", priority=PriorityType.High
        )
        task_low = Task(
            id=uuid.uuid4(), user_id=user_id, title="Low", priority=PriorityType.Low
        )
        test_session.add_all([task_high, task_low])
        test_session.commit()

        results = TaskService.get_tasks_by_user(
            test_session, user_id, priority_filter="all"
        )

        assert len(results) == 2

    def test_invalid_priority_ignored(self, test_session: Session):
        """Test invalid priority filter is ignored."""
        user_id = "test-user-invalid"

        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        # Invalid priority should not crash, just return all
        results = TaskService.get_tasks_by_user(
            test_session, user_id, priority_filter="InvalidPriority"
        )

        assert len(results) == 1


class TestTagsFilter:
    """Test tags filter logic with JOIN."""

    def test_filter_by_single_tag(self, test_session: Session):
        """Test filtering by single tag."""
        user_id = "test-user-tag"

        # Create tasks
        task1 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 1")
        task2 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 2")
        test_session.add_all([task1, task2])
        test_session.commit()

        # Assign tags
        TagService.assign_tags_to_task(test_session, task1, ["urgent"])
        TagService.assign_tags_to_task(test_session, task2, ["personal"])

        # Filter by "urgent"
        results = TaskService.get_tasks_by_user(
            test_session, user_id, tags_filter=["urgent"]
        )

        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_filter_by_multiple_tags_any_match(self, test_session: Session):
        """Test filtering by multiple tags returns tasks with ANY of the tags."""
        user_id = "test-user-multi"

        # Create tasks
        task1 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 1")
        task2 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 2")
        task3 = Task(id=uuid.uuid4(), user_id=user_id, title="Task 3")
        test_session.add_all([task1, task2, task3])
        test_session.commit()

        # Assign tags
        TagService.assign_tags_to_task(test_session, task1, ["work"])
        TagService.assign_tags_to_task(test_session, task2, ["urgent"])
        TagService.assign_tags_to_task(test_session, task3, ["personal"])

        # Filter by "work" OR "urgent"
        results = TaskService.get_tasks_by_user(
            test_session, user_id, tags_filter=["work", "urgent"]
        )

        assert len(results) == 2
        titles = {t.title for t in results}
        assert "Task 1" in titles  # has "work"
        assert "Task 2" in titles  # has "urgent"

    def test_filter_empty_tags_returns_all(self, test_session: Session):
        """Test empty tags filter returns all tasks."""
        user_id = "test-user-empty-tags"

        task = Task(id=uuid.uuid4(), user_id=user_id, title="Task")
        test_session.add(task)
        test_session.commit()

        results = TaskService.get_tasks_by_user(test_session, user_id, tags_filter=[])

        assert len(results) == 1


class TestSortingLogic:
    """Test sorting logic for all fields."""

    def test_sort_by_created_at_desc_default(self, test_session: Session):
        """Test default sort is created_at descending (newest first)."""
        user_id = "test-user-sort"

        # Create tasks in order
        task1 = Task(id=uuid.uuid4(), user_id=user_id, title="First")
        test_session.add(task1)
        test_session.commit()

        task2 = Task(id=uuid.uuid4(), user_id=user_id, title="Second")
        test_session.add(task2)
        test_session.commit()

        # Get with default sort
        results = TaskService.get_tasks_by_user(test_session, user_id)

        # Newest (task2) should be first
        assert results[0].title == "Second"
        assert results[1].title == "First"

    def test_sort_by_title_ascending(self, test_session: Session):
        """Test sorting by title alphabetically."""
        user_id = "test-user-title"

        task_z = Task(id=uuid.uuid4(), user_id=user_id, title="Zebra")
        task_a = Task(id=uuid.uuid4(), user_id=user_id, title="Apple")
        test_session.add_all([task_z, task_a])
        test_session.commit()

        results = TaskService.get_tasks_by_user(
            test_session, user_id, sort_by="title", sort_direction="asc"
        )

        assert results[0].title == "Apple"
        assert results[1].title == "Zebra"

    def test_sort_by_due_date(self, test_session: Session):
        """Test sorting by due_date."""
        user_id = "test-user-due"

        task_late = Task(
            id=uuid.uuid4(), user_id=user_id, title="Late", due_date=date(2025, 12, 31)
        )
        task_soon = Task(
            id=uuid.uuid4(), user_id=user_id, title="Soon", due_date=date(2025, 1, 5)
        )
        test_session.add_all([task_late, task_soon])
        test_session.commit()

        results = TaskService.get_tasks_by_user(
            test_session, user_id, sort_by="due_date", sort_direction="asc"
        )

        # Earliest due date first
        assert results[0].title == "Soon"
        assert results[1].title == "Late"

    def test_sort_by_priority(self, test_session: Session):
        """Test sorting by priority (High > Medium > Low)."""
        user_id = "test-user-priority-sort"

        task_low = Task(
            id=uuid.uuid4(), user_id=user_id, title="Low", priority=PriorityType.Low
        )
        task_high = Task(
            id=uuid.uuid4(), user_id=user_id, title="High", priority=PriorityType.High
        )
        task_medium = Task(
            id=uuid.uuid4(), user_id=user_id, title="Medium", priority=PriorityType.Medium
        )
        test_session.add_all([task_low, task_high, task_medium])
        test_session.commit()

        # Sort descending (High first)
        results = TaskService.get_tasks_by_user(
            test_session, user_id, sort_by="priority", sort_direction="desc"
        )

        # Order should be High, Medium, Low
        assert results[0].priority == PriorityType.High
        assert results[1].priority == PriorityType.Medium
        assert results[2].priority == PriorityType.Low


class TestCombinedFilters:
    """Test combining multiple filters."""

    def test_search_and_priority_combined(self, test_session: Session):
        """Test combining search and priority filter."""
        user_id = "test-user-combo"

        task1 = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Important meeting",
            priority=PriorityType.High,
        )
        task2 = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Casual meeting",
            priority=PriorityType.Low,
        )
        test_session.add_all([task1, task2])
        test_session.commit()

        results = TaskService.get_tasks_by_user(
            test_session, user_id, search_text="meeting", priority_filter="High"
        )

        assert len(results) == 1
        assert results[0].title == "Important meeting"

    def test_all_filters_combined(self, test_session: Session):
        """Test combining search, priority, tags, and sorting."""
        user_id = "test-user-all-filters"

        # Create tasks
        task1 = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Important work task",
            priority=PriorityType.High,
            completed=False,
        )
        task2 = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Important personal task",
            priority=PriorityType.Low,
            completed=True,
        )
        test_session.add_all([task1, task2])
        test_session.commit()

        # Assign tags
        TagService.assign_tags_to_task(test_session, task1, ["work", "urgent"])
        TagService.assign_tags_to_task(test_session, task2, ["personal"])

        # Apply all filters
        results = TaskService.get_tasks_by_user(
            test_session,
            user_id,
            search_text="important",
            completed=False,
            priority_filter="High",
            tags_filter=["work"],
        )

        assert len(results) == 1
        assert results[0].title == "Important work task"
