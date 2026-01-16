"""Common Response Schemas

Reusable Pydantic schemas for API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic

# Generic type for data in API responses
T = TypeVar('T')


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    message: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Machine-readable error code")


class MessageResponse(BaseModel):
    """Standard message response schema."""

    message: str

    model_config = {"json_schema_extra": {"examples": [{"message": "Success message"}]}}


class ApiResponse(BaseModel, Generic[T]):
    """
    Standardized API response wrapper.

    All successful API responses use this format:
    {
        "data": <response_data>,
        "error": null
    }

    All error responses use this format:
    {
        "data": null,
        "error": {"message": "...", "code": "..."}
    }
    """
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None
