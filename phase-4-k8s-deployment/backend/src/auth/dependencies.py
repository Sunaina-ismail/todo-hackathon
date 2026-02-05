"""FastAPI Authentication Dependencies

JWT authentication dependencies for endpoint protection.
"""

import logging
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.jwt import extract_user_id, verify_jwt_token

logger = logging.getLogger(__name__)

# HTTPBearer security scheme for Authorization header
security = HTTPBearer(
    scheme_name="BearerAuth",
    description="JWT token from Better Auth (Next.js)",
    auto_error=True,  # Automatically raise 401 if Authorization header is missing
)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
    """FastAPI dependency to get current user from JWT token.

    Validates JWT token using shared BETTER_AUTH_SECRET from Better Auth (Next.js).
    Uses HS256 algorithm for symmetric signature verification.

    Args:
        credentials: HTTPAuthorizationCredentials from HTTPBearer security scheme

    Returns:
        Dict[str, Any]: Decoded JWT payload containing user information

    Raises:
        HTTPException 401: If token is missing, invalid, or expired

    Example usage in endpoint:
        @app.get("/api/{user_id}/tasks")
        async def list_tasks(
            current_user: Dict[str, Any] = Depends(get_current_user)
        ):
            user_id = current_user["sub"]
            # ... endpoint logic
    """
    try:
        # Extract token from credentials
        token = credentials.credentials

        # Verify JWT signature using shared secret and decode payload
        payload = verify_jwt_token(token)

        logger.info(f"Successfully authenticated user: {payload.get('sub')}")
        return payload

    except ValueError as e:
        # Token validation failed (invalid, expired, missing claims)
        logger.error(f"Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Unexpected error during token validation
        logger.error(f"Unexpected auth error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(current_user: dict[str, Any] = Depends(get_current_user)) -> str:
    """Extract user_id from current user JWT claims.

    CRITICAL: All endpoints MUST validate that this user_id matches the user_id
    in the URL path to ensure proper user data isolation.

    Args:
        current_user: Decoded JWT payload from get_current_user dependency

    Returns:
        str: User ID from 'sub' claim

    Raises:
        HTTPException 401: If 'sub' claim is missing or invalid

    Example usage in endpoint:
        @app.get("/api/{user_id}/tasks")
        async def list_tasks(
            user_id: str,
            current_user_id: str = Depends(get_current_user_id)
        ):
            # CRITICAL: Validate user_id matches token
            if user_id != current_user_id:
                raise HTTPException(403, "Not authorized")
            # ... endpoint logic
    """
    try:
        user_id = extract_user_id(current_user)
        return user_id

    except ValueError as e:
        # Missing or invalid user_id in token
        logger.error(f"Failed to extract user_id: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
