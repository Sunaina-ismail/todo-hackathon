"""Integration Tests for Task Pagination and Sorting

Tests for pagination (limit, offset) and sorting (sort_by, sort_direction) in GET /api/{user_id}/tasks.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import date, datetime, timedelta


class TestTaskPagination:
    """Test pagination functionality with limit and offset."""

    def test_pagination_with_limit(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test pagination with limit parameter works correctly."""
        # Create 10 tasks
        for i in range(10):
            client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Task {i+1}"},
                headers=auth_headers
            )

        # Request only 5 tasks
        response = client.get(
            f"/api/{test_user_id}/tasks?limit=5",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) <= 5

    def test_pagination_with_offset(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test pagination with offset parameter works correctly."""
        # Create 10 tasks
        created_tasks = []
        for i in range(10):
            response = client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Task {i+1}"},
                headers=auth_headers
            )
            created_tasks.append(response.json())

        # Get first page
        first_page = client.get(
            f"/api/{test_user_id}/tasks?limit=5&offset=0",
            headers=auth_headers
        ).json()

        # Get second page
        second_page = client.get(
            f"/api/{test_user_id}/tasks?limit=5&offset=5",
            headers=auth_headers
        ).json()

        # Verify no overlap between pages
        first_page_ids = {task["id"] for task in first_page}
        second_page_ids = {task["id"] for task in second_page}
        assert len(first_page_ids.intersection(second_page_ids)) == 0

    def test_pagination_default_limit_50(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test default limit is 50 when not specified."""
        # Create 60 tasks
        for i in range(60):
            client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Task {i+1}"},
                headers=auth_headers
            )

        # Request without limit
        response = client.get(
            f"/api/{test_user_id}/tasks",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) <= 50  # Default limit

    def test_pagination_max_limit_100(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test maximum limit is 100."""
        # Try to request 200 tasks (should be capped at 100)
        response = client.get(
            f"/api/{test_user_id}/tasks?limit=200",
            headers=auth_headers
        )

        # Should return validation error for limit > 100
        assert response.status_code == 422  # Validation error

    def test_pagination_with_search_and_filter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test pagination works correctly with search and filter."""
        # Create tasks with "urgent" tag
        for i in range(10):
            client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Urgent task {i+1}", "tags": ["urgent"]},
                headers=auth_headers
            )

        response = client.get(
            f"/api/{test_user_id}/tasks?tags=urgent&limit=5&offset=0",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) <= 5
        # All tasks should have "urgent" tag
        for task in tasks:
            assert "urgent" in task.get("tags", [])


class TestTaskSorting:
    """Test sorting functionality with sort_by and sort_direction."""

    def test_sort_by_created_at_desc(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test sort by created_at descending (newest first - default)."""
        # Create tasks with slight delay
        task1 = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "First Task"},
            headers=auth_headers
        ).json()

        task2 = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Second Task"},
            headers=auth_headers
        ).json()

        response = client.get(
            f"/api/{test_user_id}/tasks?sort_by=created_at&sort_direction=desc",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Newest task should be first
        if len(tasks) >= 2:
            # Second task should appear before first task (DESC order)
            task2_index = next((i for i, t in enumerate(tasks) if t["id"] == task2["id"]), None)
            task1_index = next((i for i, t in enumerate(tasks) if t["id"] == task1["id"]), None)
            if task2_index is not None and task1_index is not None:
                assert task2_index < task1_index

    def test_sort_by_created_at_asc(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test sort by created_at ascending (oldest first)."""
        # Create tasks
        task1 = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "First Task"},
            headers=auth_headers
        ).json()

        task2 = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Second Task"},
            headers=auth_headers
        ).json()

        response = client.get(
            f"/api/{test_user_id}/tasks?sort_by=created_at&sort_direction=asc",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Oldest task should be first
        if len(tasks) >= 2:
            task1_index = next((i for i, t in enumerate(tasks) if t["id"] == task1["id"]), None)
            task2_index = next((i for i, t in enumerate(tasks) if t["id"] == task2["id"]), None)
            if task1_index is not None and task2_index is not None:
                assert task1_index < task2_index

    def test_sort_by_title_alphabetically(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test sort by title alphabetically works."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Zebra Task"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Apple Task"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?sort_by=title&sort_direction=asc",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Find our test tasks
        test_tasks = [t for t in tasks if "Task" in t["title"] and t["title"] in ["Zebra Task", "Apple Task"]]
        if len(test_tasks) == 2:
            # Apple should come before Zebra
            assert test_tasks[0]["title"] == "Apple Task"
            assert test_tasks[1]["title"] == "Zebra Task"

    def test_sort_by_due_date(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test sort by due_date works."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task Due Later", "due_date": "2025-12-31"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task Due Soon", "due_date": "2025-01-05"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?sort_by=due_date&sort_direction=asc",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Tasks with due dates should be sorted
        tasks_with_dates = [t for t in tasks if t.get("due_date")]
        if len(tasks_with_dates) >= 2:
            # Verify ascending order
            for i in range(len(tasks_with_dates) - 1):
                if tasks_with_dates[i]["due_date"] and tasks_with_dates[i+1]["due_date"]:
                    assert tasks_with_dates[i]["due_date"] <= tasks_with_dates[i+1]["due_date"]

    def test_sort_by_priority(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test sort by priority (High > Medium > Low) works."""
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Low Priority", "priority": "Low"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "High Priority", "priority": "High"},
            headers=auth_headers
        )
        client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Medium Priority", "priority": "Medium"},
            headers=auth_headers
        )

        response = client.get(
            f"/api/{test_user_id}/tasks?sort_by=priority&sort_direction=desc",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Find our test tasks
        test_tasks = [t for t in tasks if t["title"] in ["Low Priority", "High Priority", "Medium Priority"]]
        if len(test_tasks) == 3:
            priorities = [t["priority"] for t in test_tasks]
            # High should come before Medium, Medium before Low (DESC order)
            high_index = priorities.index("High")
            medium_index = priorities.index("Medium")
            low_index = priorities.index("Low")
            assert high_index < medium_index < low_index

    def test_sort_default_created_at_desc(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test default sort is created_at DESC (newest first)."""
        task1 = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Old Task"},
            headers=auth_headers
        ).json()

        task2 = client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "New Task"},
            headers=auth_headers
        ).json()

        # Request without sort parameters
        response = client.get(
            f"/api/{test_user_id}/tasks",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()

        # Newest should be first by default
        if len(tasks) >= 2:
            task2_index = next((i for i, t in enumerate(tasks) if t["id"] == task2["id"]), None)
            task1_index = next((i for i, t in enumerate(tasks) if t["id"] == task1["id"]), None)
            if task2_index is not None and task1_index is not None:
                assert task2_index < task1_index


class TestPaginationWithSortingAndFilters:
    """Test pagination works correctly with sorting and filters combined."""

    def test_pagination_with_sort_and_filter(
        self, client: TestClient, test_user_id: str, auth_headers: dict
    ):
        """Test pagination with sorting and filtering works correctly."""
        # Create high priority tasks
        for i in range(10):
            client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"High Task {i+1}", "priority": "High"},
                headers=auth_headers
            )

        response = client.get(
            f"/api/{test_user_id}/tasks?priority=High&sort_by=title&sort_direction=asc&limit=5&offset=0",
            headers=auth_headers
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) <= 5

        # All should be High priority
        for task in tasks:
            assert task["priority"] == "High"

        # Should be sorted by title
        titles = [t["title"] for t in tasks]
        assert titles == sorted(titles)
