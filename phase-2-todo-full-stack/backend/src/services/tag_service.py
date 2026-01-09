"""Tag Service

Business logic for tag operations with user validation and security.
"""

import logging
import uuid

from sqlmodel import Session, func, select

from src.models.tag import Tag
from src.models.task import Task as TaskModel
from src.models.task_tag import TaskTag
from src.schemas.tag import TagWithUsage

logger = logging.getLogger(__name__)


class TagService:
    """Tag business logic with user validation and Neon-optimized queries."""

    @staticmethod
    def get_or_create_tag(session: Session, user_id: str, tag_name: str) -> Tag:
        """Get an existing tag or create a new one for the user.

        Args:
            session: Database session
            user_id: User ID from authenticated context (JWT)
            tag_name: Name of the tag to get or create

        Returns:
            Tag entity

        Example:
            >>> tag = TagService.get_or_create_tag(session, "user123", "urgent")
        """
        try:
            # Try to find existing tag for this user
            statement = select(Tag).where(
                (Tag.user_id == user_id) & (Tag.name == tag_name)
            )
            tag = session.exec(statement).first()

            if tag:
                logger.info(f"Found existing tag '{tag_name}' for user {user_id}")
                return tag

            # Create new tag if it doesn't exist
            tag = Tag(user_id=user_id, name=tag_name)
            session.add(tag)
            session.commit()
            session.refresh(tag)
            logger.info(f"Created new tag '{tag_name}' for user {user_id}")
            return tag
        except Exception as e:
            session.rollback()
            logger.error(f"Error getting/creating tag '{tag_name}' for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def get_user_tags_with_usage(session: Session, user_id: str) -> list[TagWithUsage]:
        """Get all unique tags for a user with usage counts.

        Args:
            session: Database session
            user_id: User ID for data isolation

        Returns:
            List of TagWithUsage objects sorted alphabetically by name

        Example:
            >>> tags = TagService.get_user_tags_with_usage(session, "user123")
            >>> for tag in tags:
            >>>     print(f"{tag.name}: {tag.usage_count}")
        """
        try:
            # Query tags with usage count using JOIN
            statement = (
                select(
                    Tag.name,
                    func.count(TaskTag.task_id).label("usage_count")
                )
                .outerjoin(TaskTag, Tag.id == TaskTag.tag_id)
                .where(Tag.user_id == user_id)
                .group_by(Tag.name)
                .order_by(Tag.name)
            )

            results = session.exec(statement).all()

            tags_with_usage = [
                TagWithUsage(name=name, usage_count=count or 0)
                for name, count in results
            ]

            logger.info(f"Retrieved {len(tags_with_usage)} tags for user {user_id}")
            return tags_with_usage
        except Exception as e:
            logger.error(f"Error retrieving tags for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def assign_tags_to_task(session: Session, task: TaskModel, tag_names: list[str]) -> None:
        """Assign tags to a task (replaces existing tags).

        Args:
            session: Database session
            task: Task entity to assign tags to
            tag_names: List of tag names to assign (duplicates will be removed)

        Example:
            >>> TagService.assign_tags_to_task(session, task, ["urgent", "work"])
        """
        try:
            # Remove existing tag associations
            delete_statement = select(TaskTag).where(TaskTag.task_id == task.id)
            existing_associations = session.exec(delete_statement).all()
            for association in existing_associations:
                session.delete(association)

            # Deduplicate tag names to prevent UNIQUE constraint violations
            unique_tag_names = list(set(tag_names))

            # Create new tag associations
            for tag_name in unique_tag_names:
                # Get or create tag
                tag = TagService.get_or_create_tag(session, task.user_id, tag_name)

                # Create task-tag association
                task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                session.add(task_tag)

            session.commit()
            logger.info(f"Assigned {len(unique_tag_names)} tags to task {task.id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error assigning tags to task {task.id}: {str(e)}")
            raise

    @staticmethod
    def get_task_tags(session: Session, task_id: uuid.UUID) -> list[str]:
        """Get all tag names for a specific task.

        Args:
            session: Database session
            task_id: Task ID to get tags for

        Returns:
            List of tag names

        Example:
            >>> tags = TagService.get_task_tags(session, task_id)
            >>> print(tags)  # ["urgent", "work"]
        """
        try:
            statement = (
                select(Tag.name)
                .join(TaskTag, Tag.id == TaskTag.tag_id)
                .where(TaskTag.task_id == task_id)
                .order_by(Tag.name)
            )

            tag_names = session.exec(statement).all()
            return list(tag_names)
        except Exception as e:
            logger.error(f"Error retrieving tags for task {task_id}: {str(e)}")
            raise

    @staticmethod
    def remove_orphaned_tags(session: Session, user_id: str) -> int:
        """Remove tags that are not associated with any tasks.

        Args:
            session: Database session
            user_id: User ID for data isolation

        Returns:
            Number of orphaned tags removed

        Example:
            >>> count = TagService.remove_orphaned_tags(session, "user123")
            >>> print(f"Removed {count} orphaned tags")
        """
        try:
            # Find tags with no task associations
            statement = (
                select(Tag)
                .outerjoin(TaskTag, Tag.id == TaskTag.tag_id)
                .where(
                    (Tag.user_id == user_id) & (TaskTag.tag_id.is_(None))
                )
            )

            orphaned_tags = session.exec(statement).all()
            count = len(orphaned_tags)

            for tag in orphaned_tags:
                session.delete(tag)

            session.commit()
            logger.info(f"Removed {count} orphaned tags for user {user_id}")
            return count
        except Exception as e:
            session.rollback()
            logger.error(f"Error removing orphaned tags for user {user_id}: {str(e)}")
            raise
