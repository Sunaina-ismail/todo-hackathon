"""Pytest Configuration and Fixtures

Shared test fixtures and configuration for the test suite.
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from src.main import app
from src.db.session import get_session
from src.auth.dependencies import get_current_user_id
from jose import jwt
from src.config import settings


# Create in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """Create a test database session.

    Uses in-memory SQLite database for fast, isolated testing.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database session override."""

    def get_session_override() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_id() -> str:
    """Test user ID for authentication."""
    return "test-user-123"


@pytest.fixture
def test_jwt_token(test_user_id: str) -> str:
    """Create a test JWT token for authentication.

    Args:
        test_user_id: User ID to encode in token

    Returns:
        JWT token string
    """
    payload = {"sub": test_user_id, "email": "test@example.com"}
    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


@pytest.fixture
def auth_headers(test_jwt_token: str) -> dict[str, str]:
    """Create authentication headers with JWT token.

    Args:
        test_jwt_token: JWT token for authentication

    Returns:
        Headers dictionary with Authorization header
    """
    return {"Authorization": f"Bearer {test_jwt_token}"}


@pytest.fixture
def authenticated_client(
    client: TestClient, test_user_id: str
) -> Generator[TestClient, None, None]:
    """Create a test client with authentication bypass.

    Args:
        client: Test client
        test_user_id: User ID for authentication

    Yields:
        Test client with authentication override
    """

    def get_current_user_id_override() -> str:
        return test_user_id

    app.dependency_overrides[get_current_user_id] = get_current_user_id_override
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def generate_test_jwt():
    """Generate a JWT token for a given user_id.

    Returns:
        Callable that takes user_id and returns JWT token
    """

    def _generate(user_id: str) -> str:
        payload = {"sub": user_id, "email": f"{user_id}@example.com"}
        token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token

    return _generate
