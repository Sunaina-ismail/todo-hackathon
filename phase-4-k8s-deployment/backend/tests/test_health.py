"""
Tests for health check endpoints.
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from sqlalchemy.exc import OperationalError


@pytest.mark.asyncio
async def test_health_endpoint_returns_200(client: AsyncClient):
    """Test that /api/health returns 200 OK."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "backend"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_readiness_endpoint_returns_200_with_valid_db(client: AsyncClient):
    """Test that /api/ready returns 200 when database is accessible."""
    with patch.dict("os.environ", {
        "DATABASE_URL": "postgresql://test:test@localhost/test",
        "BETTER_AUTH_SECRET": "test-secret-key-min-32-characters",
        "OPENAI_API_KEY": "sk-test-key"
    }):
        # Mock database connection
        with patch("src.api.health.async_session_maker") as mock_session:
            mock_session.return_value.__aenter__.return_value.execute = AsyncMock()

            response = await client.get("/api/ready")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"
            assert data["service"] == "backend"
            assert data["checks"]["environment"] == "ok"
            assert data["checks"]["database"] == "ok"
            assert "timestamp" in data


@pytest.mark.asyncio
async def test_readiness_endpoint_returns_503_without_db(client: AsyncClient):
    """Test that /api/ready returns 503 when database is not accessible."""
    with patch.dict("os.environ", {
        "DATABASE_URL": "postgresql://test:test@localhost/test",
        "BETTER_AUTH_SECRET": "test-secret-key-min-32-characters",
        "OPENAI_API_KEY": "sk-test-key"
    }):
        # Mock database connection failure
        with patch("src.api.health.async_session_maker") as mock_session:
            mock_session.return_value.__aenter__.side_effect = OperationalError(
                "connection failed", None, None
            )

            response = await client.get("/api/ready")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "not_ready"
            assert data["service"] == "backend"
            assert data["checks"]["environment"] == "ok"
            assert data["checks"]["database"] == "failed"
            assert len(data["errors"]) > 0
            assert "Database connection failed" in data["errors"][0]


@pytest.mark.asyncio
async def test_readiness_endpoint_returns_503_without_env_vars(client: AsyncClient):
    """Test that /api/ready returns 503 when required env vars are missing."""
    with patch.dict("os.environ", {}, clear=True):
        response = await client.get("/api/ready")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not_ready"
        assert data["checks"]["environment"] == "failed"
        assert len(data["errors"]) > 0


@pytest.mark.asyncio
async def test_readiness_endpoint_requires_llm_api_key(client: AsyncClient):
    """Test that /api/ready requires at least one LLM API key."""
    with patch.dict("os.environ", {
        "DATABASE_URL": "postgresql://test:test@localhost/test",
        "BETTER_AUTH_SECRET": "test-secret-key-min-32-characters"
    }):
        # Mock database connection
        with patch("src.api.health.async_session_maker") as mock_session:
            mock_session.return_value.__aenter__.return_value.execute = AsyncMock()

            response = await client.get("/api/ready")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "not_ready"
            assert data["checks"]["environment"] == "failed"
            assert any("LLM API key" in error for error in data["errors"])
