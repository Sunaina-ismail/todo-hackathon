"""Custom HTTP Exceptions

Application-specific exception classes for consistent error handling.
"""

from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    """Exception raised when a task is not found."""

    def __init__(self, task_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )


class UnauthorizedAccessException(HTTPException):
    """Exception raised when user tries to access another user's resource."""

    def __init__(self, message: str = "Not authorized to access this resource") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class ValidationException(HTTPException):
    """Exception raised for validation errors."""

    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
