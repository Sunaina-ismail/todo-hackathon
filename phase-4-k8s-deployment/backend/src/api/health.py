"""
Health check endpoints for Kubernetes liveness and readiness probes.
"""
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, Response, status
from sqlalchemy import text
import os

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Liveness probe endpoint.

    Returns 200 OK if the process is running and responsive.
    Used by Kubernetes to detect crashed containers and trigger automatic restarts.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "backend"
    }


@router.get("/ready")
async def readiness_check(response: Response) -> Dict[str, Any]:
    """
    Readiness probe endpoint.

    Returns 200 OK only if the service is ready to handle requests.
    Tests database connectivity and validates environment variables.
    Used by Kubernetes to control traffic routing.
    """
    errors: List[str] = []
    checks = {
        "environment": "ok",
        "database": "ok"
    }

    # Validate required environment variables
    required_env_vars = [
        "DATABASE_URL",
        "BETTER_AUTH_SECRET"
    ]

    # At least one LLM provider API key must be set
    llm_keys = [
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
        "GROQ_API_KEY",
        "GEMINI_API_KEY"
    ]

    for env_var in required_env_vars:
        if not os.getenv(env_var):
            checks["environment"] = "failed"
            errors.append(f"Missing required environment variable: {env_var}")

    # Check if at least one LLM API key is set
    if not any(os.getenv(key) for key in llm_keys):
        checks["environment"] = "failed"
        errors.append("At least one LLM API key must be set (OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, or GEMINI_API_KEY)")

    # Test database connectivity
    try:
        from src.db.async_session import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            result.scalar()
    except Exception as e:
        checks["database"] = "failed"
        errors.append(f"Database connection failed: {str(e)}")

    # If any checks failed, return 503
    if errors:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "backend",
            "checks": checks,
            "errors": errors
        }

    # All checks passed
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "backend",
        "checks": checks
    }
