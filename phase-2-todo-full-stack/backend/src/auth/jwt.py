"""JWT Validation

Validates JWT tokens using shared BETTER_AUTH_SECRET from Better Auth.
"""

import logging
from typing import Any

from jose import JWTError, jwt

from src.config import settings

logger = logging.getLogger(__name__)

# Validate required environment variables
if not settings.BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")


def verify_jwt_token(token: str) -> dict[str, Any]:
    """Verify JWT token using shared secret from Better Auth.

    Args:
        token: JWT token string from Authorization header

    Returns:
        Dict containing decoded JWT payload with user information

    Raises:
        ValueError: If token is invalid, expired, or missing required claims

    Example:
        >>> payload = verify_jwt_token("eyJhbGciOiJIUzI1NiIs...")
        >>> print(payload['sub'])  # User ID
    """
    try:
        # Decode JWT with Better Auth compatibility
        # Better Auth doesn't set iss/aud claims, so we disable their verification
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "verify_iss": False,  # Better Auth doesn't set issuer claim
                "verify_aud": False,  # Better Auth doesn't set audience claim
            },
        )
        logger.debug(f"JWT token verified successfully for user: {payload.get('sub')}")
        return payload

    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise ValueError(f"Could not validate credentials: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error during JWT validation: {str(e)}")
        raise ValueError(f"Token validation failed: {str(e)}")


def extract_user_id(payload: dict[str, Any]) -> str:
    """Extract user_id from JWT payload.

    Args:
        payload: Decoded JWT payload dictionary

    Returns:
        User ID from 'sub' claim

    Raises:
        ValueError: If 'sub' claim is missing or invalid

    Example:
        >>> payload = {"sub": "user123", "email": "user@example.com"}
        >>> user_id = extract_user_id(payload)
        >>> print(user_id)  # "user123"
    """
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Invalid token: missing 'sub' claim (user_id)")

    return user_id
