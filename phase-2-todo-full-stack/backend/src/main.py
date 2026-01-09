"""FastAPI Main Application

Todo API with JWT authentication and Neon PostgreSQL.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import tags_router, tasks_router
from src.config import settings
from src.db import create_db_and_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Todo API - Phase 2",
    description="FastAPI backend for Todo application with JWT authentication from Next.js",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS to allow requests from Next.js frontend
# CRITICAL: Allow Authorization header for JWT tokens from Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured for origins: {settings.allowed_origins_list}")

# Include API routers
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(tags_router, prefix="/api", tags=["tags"])


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup."""
    logger.info("Starting up application...")
    create_db_and_tables()
    logger.info("Application startup complete")


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning API information."""
    return {"message": "Todo API - Phase 2 Backend", "status": "ready", "version": "0.1.0"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint (no authentication required).

    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "todo-api"}
