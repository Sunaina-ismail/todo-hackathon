"""Database Session Management

FastAPI dependency for database session injection.
"""

from collections.abc import Generator

from sqlmodel import Session

from src.db.engine import engine


def get_session() -> Generator[Session]:
    """Database session dependency for FastAPI endpoints.

    Usage:
        @app.get("/api/{user_id}/tasks")
        async def list_tasks(session: Session = Depends(get_session)):
            # Use session here

    Yields:
        Session: SQLModel database session

    Note:
        Session is automatically closed after the request completes.
    """
    with Session(engine) as session:
        yield session
