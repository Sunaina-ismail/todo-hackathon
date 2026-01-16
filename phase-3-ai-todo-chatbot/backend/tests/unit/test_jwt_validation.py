"""Unit Tests for JWT Validation

Tests for JWT token validation using shared BETTER_AUTH_SECRET.
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt
from src.auth.jwt import verify_jwt_token, extract_user_id
from src.config import settings


class TestJWTValidation:
    """Test JWT token validation with shared secret."""

    def test_verify_valid_jwt_token(self):
        """Test verifying a valid JWT token."""
        user_id = "test-user-123"
        payload = {
            "sub": user_id,
            "email": "test@example.com",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        # Create valid token
        token = jwt.encode(
            payload,
            settings.BETTER_AUTH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        # Verify token
        decoded = verify_jwt_token(token)

        assert decoded["sub"] == user_id
        assert decoded["email"] == "test@example.com"
        assert "iat" in decoded
        assert "exp" in decoded

    def test_verify_jwt_with_invalid_signature(self):
        """Test that JWT validation fails with invalid signature."""
        user_id = "test-user-123"
        payload = {
            "sub": user_id,
            "email": "test@example.com",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        # Create token with wrong secret
        wrong_secret = "wrong-secret-key"
        token = jwt.encode(
            payload,
            wrong_secret,
            algorithm=settings.JWT_ALGORITHM
        )

        # Verification should fail
        with pytest.raises(ValueError, match="Could not validate credentials"):
            verify_jwt_token(token)

    def test_verify_jwt_with_missing_token(self):
        """Test that JWT validation fails with empty token."""
        with pytest.raises(ValueError):
            verify_jwt_token("")

    def test_verify_jwt_with_expired_token(self):
        """Test that JWT validation fails with expired token."""
        user_id = "test-user-123"
        payload = {
            "sub": user_id,
            "email": "test@example.com",
            "iat": datetime.utcnow() - timedelta(days=8),
            "exp": datetime.utcnow() - timedelta(days=1)  # Expired yesterday
        }

        # Create expired token
        token = jwt.encode(
            payload,
            settings.BETTER_AUTH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        # Verification should fail
        with pytest.raises(ValueError, match="Could not validate credentials"):
            verify_jwt_token(token)

    def test_verify_jwt_with_malformed_token(self):
        """Test that JWT validation fails with malformed token."""
        malformed_token = "not-a-valid-jwt-token"

        with pytest.raises(ValueError, match="Could not validate credentials"):
            verify_jwt_token(malformed_token)

    def test_extract_user_id_from_valid_payload(self):
        """Test extracting user_id from valid JWT payload."""
        user_id = "test-user-123"
        payload = {
            "sub": user_id,
            "email": "test@example.com"
        }

        extracted_id = extract_user_id(payload)
        assert extracted_id == user_id

    def test_extract_user_id_from_payload_missing_sub(self):
        """Test that extract_user_id fails when 'sub' claim is missing."""
        payload = {
            "email": "test@example.com"
            # Missing 'sub' claim
        }

        with pytest.raises(ValueError, match="missing 'sub' claim"):
            extract_user_id(payload)

    def test_extract_user_id_from_empty_payload(self):
        """Test that extract_user_id fails with empty payload."""
        payload = {}

        with pytest.raises(ValueError, match="missing 'sub' claim"):
            extract_user_id(payload)

    def test_jwt_algorithm_is_hs256(self):
        """Test that JWT algorithm is HS256 (shared secret)."""
        assert settings.JWT_ALGORITHM == "HS256"

    def test_verify_jwt_preserves_all_claims(self):
        """Test that JWT verification preserves all custom claims."""
        user_id = "test-user-123"
        payload = {
            "sub": user_id,
            "email": "test@example.com",
            "name": "Test User",
            "custom_field": "custom_value",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        # Create token
        token = jwt.encode(
            payload,
            settings.BETTER_AUTH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        # Verify and check all claims are preserved
        decoded = verify_jwt_token(token)

        assert decoded["sub"] == user_id
        assert decoded["email"] == "test@example.com"
        assert decoded["name"] == "Test User"
        assert decoded["custom_field"] == "custom_value"


class TestJWTIntegration:
    """Integration tests for JWT validation flow."""

    def test_full_jwt_validation_flow(self):
        """Test complete JWT validation workflow."""
        # Step 1: Create JWT token (simulating Better Auth)
        user_id = "integration-user-456"
        payload = {
            "sub": user_id,
            "email": "integration@example.com",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        token = jwt.encode(
            payload,
            settings.BETTER_AUTH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        # Step 2: Verify token (simulating FastAPI endpoint)
        decoded = verify_jwt_token(token)
        assert decoded is not None

        # Step 3: Extract user_id (simulating dependency injection)
        extracted_user_id = extract_user_id(decoded)
        assert extracted_user_id == user_id

    def test_jwt_roundtrip_with_minimal_payload(self):
        """Test JWT roundtrip with minimal required payload."""
        user_id = "minimal-user-789"
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        # Encode
        token = jwt.encode(
            payload,
            settings.BETTER_AUTH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        # Decode
        decoded = verify_jwt_token(token)

        # Extract
        extracted_user_id = extract_user_id(decoded)

        assert extracted_user_id == user_id
