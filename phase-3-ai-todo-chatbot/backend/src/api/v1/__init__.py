"""API Version 1

REST API endpoints version 1 for task and tag management.
"""

from src.api.v1.tags import router as tags_router
from src.api.v1.tasks import router as tasks_router

__all__ = ["tasks_router", "tags_router"]
