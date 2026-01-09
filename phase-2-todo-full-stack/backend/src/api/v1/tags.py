"""Tag API Endpoints

REST API endpoints for tag operations with JWT authentication and user validation.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user_id
from src.db.session import get_session
from src.schemas.tag import TagWithUsage
from src.services.tag_service import TagService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{user_id}/tags", response_model=list[TagWithUsage])
async def get_tags(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),  # JWT user_id
    session: Session = Depends(get_session),
) -> list[TagWithUsage]:
    """Get all unique tags with usage counts for the authenticated user.

    **CRITICAL**: Validates that URL user_id matches JWT user_id.
    Users can ONLY see their own tags.

    Args:
        user_id: User ID from URL path
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        List of tags with usage counts, sorted alphabetically by name

    Raises:
        HTTPException 401: If JWT token is invalid
        HTTPException 403: If URL user_id does not match JWT user_id
    """
    if user_id != current_user_id:
        logger.warning(
            f"Unauthorized access attempt: user {current_user_id} tried to access tags for {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    logger.info(f"User {current_user_id} requesting tags with usage counts")

    tags = TagService.get_user_tags_with_usage(session=session, user_id=user_id)

    logger.info(f"Returning {len(tags)} tags for user {current_user_id}")
    return tags
