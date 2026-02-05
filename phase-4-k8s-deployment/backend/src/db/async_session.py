"""Async Database Session Management

Async session factory for ChatKit server and agent operations.
Provides async database sessions for non-blocking I/O operations.
"""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.config import settings


# Create async engine for PostgreSQL
# Convert postgresql:// to postgresql+asyncpg:// for async support
# Remove sslmode parameter from URL (asyncpg doesn't support it in URL)
async_database_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)
# Remove sslmode query parameter if present
if "?sslmode=" in async_database_url:
    async_database_url = async_database_url.split("?sslmode=")[0]
elif "&sslmode=" in async_database_url:
    async_database_url = async_database_url.split("&sslmode=")[0]

async_engine = create_async_engine(
    async_database_url,
    echo=settings.ENVIRONMENT == "development",
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_recycle=settings.DB_POOL_RECYCLE,
    connect_args={
        "ssl": "require",  # asyncpg SSL configuration
        "server_settings": {
            "application_name": "todo-app",
        },
    },
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Async database session dependency for ChatKit server and agent operations.

    Usage:
        async with get_async_session() as session:
            # Use async session here
            result = await session.execute(select(Conversation))

    Yields:
        AsyncSession: SQLAlchemy async database session

    Note:
        Session is automatically closed after the context manager exits.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_async_db() -> None:
    """Initialize async database tables.

    Creates all tables defined in SQLModel metadata.
    Should only be called during application startup or testing.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
