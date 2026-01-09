"""SQLModel Engine Configuration

Neon Serverless PostgreSQL engine with optimized connection pooling.
"""

import logging

from sqlmodel import SQLModel, create_engine

from src.config import settings

logger = logging.getLogger(__name__)

# Neon Serverless PostgreSQL connection string validation
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

if not settings.DATABASE_URL.startswith("postgresql://"):
    raise ValueError("DATABASE_URL must be a PostgreSQL connection string")

# Create engine with Neon-specific configuration for serverless
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,  # Optimal for serverless workloads
    max_overflow=settings.DB_MAX_OVERFLOW,  # Allow some overflow during traffic spikes
    pool_pre_ping=settings.DB_POOL_PRE_PING,  # Verify connections before use (critical for serverless)
    pool_recycle=settings.DB_POOL_RECYCLE,  # Recycle connections every 5 minutes to handle timeouts
    echo=False,  # Set to True for debugging only
    connect_args={
        "sslmode": "require",  # Required for Neon
        "application_name": "todo-app",  # Help with monitoring
        "connect_timeout": "10",  # Connection timeout (10 seconds)
        # NOTE: statement_timeout not supported with Neon pooled connections (-pooler)
        # Neon pooler handles timeouts automatically
    },
)

logger.info(
    f"Database engine initialized with pool_size={settings.DB_POOL_SIZE}, "
    f"max_overflow={settings.DB_MAX_OVERFLOW}"
)


def create_db_and_tables() -> None:
    """Create database tables on startup.

    Call this in the FastAPI startup event to ensure tables exist.
    """
    logger.info("Creating database tables if they don't exist...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")
