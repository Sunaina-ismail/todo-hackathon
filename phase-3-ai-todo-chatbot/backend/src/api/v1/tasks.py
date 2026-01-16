"""Task API Endpoints

REST API endpoints for task CRUD operations with JWT authentication and user validation.
"""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user_id
from src.db.session import get_session
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskListResponse
from src.schemas.common import ApiResponse
from src.services.tag_service import TagService
from src.services.task_service import TaskService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Create a new task for the authenticated user.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.

    Args:
        user_id: User ID from URL path
        task_create: Task creation data
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Created task with all fields

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
        HTTPException 400: If validation fails
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized create attempt: user {current_user_id} tried to create task for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user",
        )

    task = TaskService.create_task(session=session, user_id=user_id, task_create=task_create)

    # Get tags for the task
    tags = TagService.get_task_tags(session, task.id)

    # Create response with tags
    response = TaskResponse.model_validate(task)
    response.tags = tags
    return response


@router.get("/{user_id}/tasks", response_model=ApiResponse[TaskListResponse])
async def list_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    completed: bool | None = Query(None, description="Filter by completion status"),
    search: str | None = Query(None, description="Search in title/description"),
    priority: str | None = Query(None, description="Filter by priority (all/High/Medium/Low)"),
    tags: list[str] | None = Query(None, description="Filter by tags (tasks with ANY of these tags)"),
    sort_by: str = Query("created_at", description="Sort by field (created_at/updated_at/title/due_date/priority)"),
    sort_direction: str = Query("desc", description="Sort direction (asc/desc)"),
    limit: int = Query(50, ge=1, le=100, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: Session = Depends(get_session),
) -> ApiResponse[TaskListResponse]:
    """List all tasks for the authenticated user with advanced filtering, search, and sorting.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.
    Users can ONLY see their own tasks.

    Args:
        user_id: User ID from URL path
        current_user_id: User ID from JWT token
        completed: Optional filter by completion status
        search: Case-insensitive search in title/description
        priority: Filter by priority (all/High/Medium/Low)
        tags: Filter by tag names (tasks with ANY of these tags)
        sort_by: Sort field (created_at/updated_at/title/due_date/priority)
        sort_direction: Sort direction (asc/desc)
        limit: Maximum number of tasks to return (default 50, max 100)
        offset: Pagination offset (default 0)
        session: Database session

    Returns:
        Wrapped response with task list and pagination info

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized access attempt: user {current_user_id} tried to access tasks for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    logger.info(
        f"User {current_user_id} requesting tasks "
        f"(completed={completed}, search={search}, priority={priority}, "
        f"tags={tags}, sort={sort_by}:{sort_direction}, limit={limit}, offset={offset})"
    )

    tasks = TaskService.get_tasks_by_user(
        session=session,
        user_id=current_user_id,
        completed=completed,
        search_text=search,
        priority_filter=priority,
        tags_filter=tags,
        sort_by=sort_by,
        sort_direction=sort_direction,
        limit=limit,
        offset=offset
    )

    # Get tags for each task
    task_responses = []
    for task in tasks:
        task_tags = TagService.get_task_tags(session, task.id)
        response = TaskResponse.model_validate(task)
        response.tags = task_tags
        task_responses.append(response)

    # Get total count (for now, return length of results - ideally should query total from DB)
    total = len(task_responses)

    logger.info(f"Returning {len(task_responses)} tasks for user {current_user_id}")

    # Return wrapped response
    return ApiResponse(
        data=TaskListResponse(
            tasks=task_responses,
            total=total,
            limit=limit,
            offset=offset
        )
    )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: uuid.UUID,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Get a specific task for the authenticated user.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.

    Args:
        user_id: User ID from URL path
        task_id: Task UUID to retrieve
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Task data with tags

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
        HTTPException 404: If task not found
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized access attempt: user {current_user_id} tried to access task {task_id} for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task"
        )

    task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Get tags for the task
    tags = TagService.get_task_tags(session, task.id)

    # Create response with tags
    response = TaskResponse.model_validate(task)
    response.tags = tags
    return response


@router.patch("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Update a specific task for the authenticated user.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.
    Supports partial updates (only provided fields are updated, including tags).

    Args:
        user_id: User ID from URL path
        task_id: Task UUID to update
        task_update: Task update data (partial updates supported, includes tags)
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Updated task data with tags

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
        HTTPException 404: If task not found
        HTTPException 400: If validation fails
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized update attempt: user {current_user_id} tried to update task {task_id} for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this task"
        )

    task = TaskService.update_task(
        session=session, task_id=task_id, user_id=user_id, task_update=task_update
    )

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Get tags for the task
    tags = TagService.get_task_tags(session, task.id)

    # Create response with tags
    response = TaskResponse.model_validate(task)
    response.tags = tags
    return response


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: uuid.UUID,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    session: Session = Depends(get_session),
) -> None:
    """Delete a specific task for the authenticated user.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.

    Args:
        user_id: User ID from URL path
        task_id: Task UUID to delete
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        None (204 No Content on success)

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
        HTTPException 404: If task not found
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized delete attempt: user {current_user_id} tried to delete task {task_id} for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this task"
        )

    success = TaskService.delete_task(session=session, task_id=task_id, user_id=user_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: uuid.UUID,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Toggle the completion status of a task.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.

    Args:
        user_id: User ID from URL path
        task_id: Task UUID to toggle
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Updated task with toggled completion status and tags

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
        HTTPException 404: If task not found
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized toggle attempt: user {current_user_id} tried to toggle task {task_id} for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this task"
        )

    task = TaskService.toggle_task_completion(session=session, task_id=task_id, user_id=user_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Get tags for the task
    tags = TagService.get_task_tags(session, task.id)

    # Create response with tags
    response = TaskResponse.model_validate(task)
    response.tags = tags
    return response
