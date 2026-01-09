"""Task Service

Business logic for task CRUD operations with user validation and security.
"""

import logging
import uuid
from datetime import datetime

from sqlmodel import Session, col, or_, select

from src.models.tag import Tag
from src.models.task import PriorityType, Task
from src.models.task_tag import TaskTag
from src.schemas.task import TaskCreate, TaskUpdate
from src.services.tag_service import TagService

logger = logging.getLogger(__name__)


class TaskService:
    """Task business logic with user validation and Neon-optimized queries."""

    @staticmethod
    def create_task(session: Session, user_id: str, task_create: TaskCreate) -> Task:
        """Create a new task for a user with Neon-optimized operations.

        Args:
            session: Database session
            user_id: User ID from authenticated context (JWT)
            task_create: Task creation data (includes tags)

        Returns:
            Created Task entity

        Raises:
            HTTPException 500: If database operation fails

        Example:
            >>> task_data = TaskCreate(
            ...     title="Buy milk",
            ...     description="Get 2 gallons",
            ...     priority=PriorityType.High,
            ...     tags=["shopping", "urgent"]
            ... )
            >>> task = TaskService.create_task(session, "user123", task_data)
        """
        try:
            # Extract tags before creating task
            tags = task_create.tags
            task_data = task_create.model_dump(exclude={"tags"})

            # Create task
            task = Task(
                **task_data,
                user_id=user_id,  # Set user_id from authenticated context, never from request
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            # Assign tags if provided
            if tags:
                TagService.assign_tags_to_task(session, task, tags)

            logger.info(f"Created task {task.id} for user {user_id} with {len(tags)} tags")
            return task
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating task for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def get_task_by_id(session: Session, task_id: uuid.UUID, user_id: str) -> Task | None:
        """Get a specific task by ID for a user - optimized for Neon Serverless.

        Args:
            session: Database session
            task_id: Task UUID to retrieve
            user_id: User ID for ownership validation

        Returns:
            Task entity if found and owned by user, None otherwise

        Example:
            >>> task_uuid = uuid.UUID("...")
            >>> task = TaskService.get_task_by_id(session, task_uuid, "user123")
            >>> if task:
            >>>     print(task.title)
        """
        try:
            statement = select(Task).where(
                (Task.id == task_id) & (Task.user_id == user_id)  # CRITICAL: Verify ownership
            )
            task = session.exec(statement).first()
            if task:
                logger.info(f"Retrieved task {task_id} for user {user_id}")
            else:
                logger.info(f"Task {task_id} not found for user {user_id}")
            return task
        except Exception as e:
            logger.error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        completed: bool | None = None,
        search_text: str | None = None,
        priority_filter: str | None = None,
        tags_filter: list[str] | None = None,
        sort_by: str = "created_at",
        sort_direction: str = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> list[Task]:
        """Get all tasks for a user with advanced filtering, search, and sorting.

        Args:
            session: Database session
            user_id: User ID for data isolation
            completed: Optional filter by completion status
            search_text: Case-insensitive search in title/description
            priority_filter: Filter by priority (all/High/Medium/Low)
            tags_filter: Filter by tag names (tasks with ANY of these tags)
            sort_by: Sort field (created_at/updated_at/title/due_date/priority)
            sort_direction: Sort direction (asc/desc)
            limit: Maximum number of tasks to return (default 50, max 100)
            offset: Pagination offset (default 0)

        Returns:
            List of Task entities matching criteria

        Example:
            >>> tasks = TaskService.get_tasks_by_user(
            ...     session,
            ...     user_id="user123",
            ...     search_text="groceries",
            ...     priority_filter="High",
            ...     tags_filter=["urgent", "shopping"],
            ...     sort_by="due_date",
            ...     sort_direction="asc",
            ...     limit=10
            ... )
        """
        try:
            # Base query with user isolation
            statement = select(Task).where(Task.user_id == user_id)

            # Apply completion status filter
            if completed is not None:
                statement = statement.where(Task.completed == completed)

            # Apply search filter (case-insensitive on title OR description)
            if search_text:
                search_pattern = f"%{search_text}%"
                statement = statement.where(
                    or_(
                        col(Task.title).ilike(search_pattern),
                        col(Task.description).ilike(search_pattern)
                    )
                )

            # Apply priority filter
            if priority_filter and priority_filter != "all":
                try:
                    priority_enum = PriorityType(priority_filter)
                    statement = statement.where(Task.priority == priority_enum)
                except ValueError:
                    logger.warning(f"Invalid priority filter: {priority_filter}")

            # Apply tags filter (tasks with ANY of the specified tags)
            if tags_filter and len(tags_filter) > 0:
                # Join with task_tags and tags tables
                statement = (
                    statement
                    .join(TaskTag, Task.id == TaskTag.task_id)
                    .join(Tag, TaskTag.tag_id == Tag.id)
                    .where(Tag.name.in_(tags_filter))
                    .distinct()
                )

            # Apply sorting
            sort_column = Task.created_at  # default
            if sort_by == "updated_at":
                sort_column = Task.updated_at
            elif sort_by == "title":
                sort_column = Task.title
            elif sort_by == "due_date":
                sort_column = Task.due_date
            elif sort_by == "priority":
                # Custom priority sorting (High=1, Medium=2, Low=3)
                # For ascending: High comes first
                # For descending: Low comes first
                sort_column = Task.priority

            if sort_direction == "asc":
                statement = statement.order_by(sort_column.asc())
            else:
                statement = statement.order_by(sort_column.desc())

            # Apply pagination
            statement = statement.offset(offset).limit(limit)

            tasks = session.exec(statement).all()
            logger.info(
                f"Retrieved {len(tasks)} tasks for user {user_id} "
                f"(search={search_text}, priority={priority_filter}, "
                f"tags={tags_filter}, sort={sort_by}:{sort_direction})"
            )
            return list(tasks)
        except Exception as e:
            logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def update_task(
        session: Session, task_id: uuid.UUID, user_id: str, task_update: TaskUpdate
    ) -> Task | None:
        """Update an existing task with Neon-optimized operations.

        Args:
            session: Database session
            task_id: Task UUID to update
            user_id: User ID for ownership validation
            task_update: Task update data (partial updates supported, includes tags)

        Returns:
            Updated Task entity if found and owned by user, None otherwise

        Example:
            >>> update_data = TaskUpdate(
            ...     title="Updated title",
            ...     completed=True,
            ...     priority=PriorityType.High,
            ...     tags=["urgent", "important"]
            ... )
            >>> task = TaskService.update_task(session, task_uuid, "user123", update_data)
        """
        try:
            task = TaskService.get_task_by_id(session, task_id, user_id)
            if not task:
                logger.warning(f"Update requested for non-existent task {task_id} by user {user_id}")
                return None

            # Extract tags before updating task fields
            update_data = task_update.model_dump(exclude_unset=True)
            tags = update_data.pop("tags", None)

            # Update task fields
            for field, value in update_data.items():
                setattr(task, field, value)

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            # Update tags if provided
            if tags is not None:
                TagService.assign_tags_to_task(session, task, tags)

            logger.info(f"Updated task {task_id} for user {user_id}")
            return task
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID, user_id: str) -> bool:
        """Delete a task by ID for a user - Neon-optimized deletion.

        Args:
            session: Database session
            task_id: Task UUID to delete
            user_id: User ID for ownership validation

        Returns:
            True if task was deleted, False if not found or not owned by user

        Example:
            >>> success = TaskService.delete_task(session, task_uuid, "user123")
            >>> if success:
            >>>     print("Task deleted")
        """
        try:
            task = TaskService.get_task_by_id(session, task_id, user_id)
            if not task:
                logger.warning(f"Delete requested for non-existent task {task_id} by user {user_id}")
                return False

            session.delete(task)
            session.commit()
            logger.info(f"Deleted task {task_id} for user {user_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def toggle_task_completion(session: Session, task_id: uuid.UUID, user_id: str) -> Task | None:
        """Toggle the completion status of a task - optimized for Neon.

        Args:
            session: Database session
            task_id: Task UUID to toggle
            user_id: User ID for ownership validation

        Returns:
            Updated Task entity if found and owned by user, None otherwise

        Example:
            >>> task = TaskService.toggle_task_completion(session, task_uuid, "user123")
            >>> print(task.completed)  # True if was False, False if was True
        """
        try:
            task = TaskService.get_task_by_id(session, task_id, user_id)
            if not task:
                logger.warning(
                    f"Toggle completion requested for non-existent task {task_id} by user {user_id}"
                )
                return None

            task.completed = not task.completed
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            logger.info(f"Toggled completion for task {task_id} for user {user_id}")
            return task
        except Exception as e:
            session.rollback()
            logger.error(f"Error toggling completion for task {task_id} for user {user_id}: {str(e)}")
            raise
