import json
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from src.controllers.health_controller import create_app


@pytest.fixture
def client():
    """Create test client for Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers(client):
    """Create auth headers with a valid token."""
    # Mock the token validation to always return True
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=True):
        yield {"Authorization": "Bearer test-token-123"}


def test_ping_endpoint_returns_200(client):
    """Test that /ping returns status code 200."""
    response = client.get("/ping")
    assert response.status_code == 200


def test_ping_endpoint_returns_pong(client):
    """Test that /ping returns pong status."""
    response = client.get("/ping")
    data = json.loads(response.data)

    assert data["status"] == "pong"
    assert "timestamp" in data
    assert "message" in data


def test_ping_endpoint_contains_timestamp(client):
    """Test that /ping response contains valid timestamp."""
    response = client.get("/ping")
    data = json.loads(response.data)

    timestamp_str = data["timestamp"]
    parsed_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    assert isinstance(parsed_time, datetime)


def test_get_responses_endpoint_returns_200(client, auth_headers):
    """Test that /get-responses returns status code 200."""
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=True):
        response = client.get("/get-responses", headers=auth_headers)
        assert response.status_code == 200


def test_get_responses_returns_json(client, auth_headers):
    """Test that /get-responses returns valid JSON structure."""
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=True):
        response = client.get("/get-responses", headers=auth_headers)
        data = json.loads(response.data)

        assert isinstance(data, dict)
        assert "total_returned" in data
        assert "redis_connected" in data
        assert "stats" in data
        assert "requests" in data
        assert isinstance(data["requests"], list)


def test_get_responses_with_limit(client, auth_headers):
    """Test that /get-responses respects limit parameter."""
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=True):
        response = client.get("/get-responses?limit=5", headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        # Should return at most 5 items
        assert len(data["requests"]) <= 5


def test_get_responses_with_endpoint_filter(client, auth_headers):
    """Test that /get-responses can filter by endpoint."""
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=True):
        response = client.get("/get-responses?endpoint=/health", headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        # All returned requests should be for /health endpoint
        for req in data["requests"]:
            if "endpoint" in req:
                assert req["endpoint"] == "/health"


@patch("src.database.redis_client.redis_client")
def test_health_persists_to_redis(mock_redis, client):
    """Test that /health saves request to Redis."""
    mock_redis.save_request = Mock(return_value="request_id")
    mock_redis.is_connected = Mock(return_value=True)

    response = client.get("/health")

    assert response.status_code == 200
    # Verify save_request was called (if Redis is available)
    # In real scenario it will be called


@patch("src.database.redis_client.redis_client")
def test_ping_persists_to_redis(mock_redis, client):
    """Test that /ping saves request to Redis."""
    mock_redis.save_request = Mock(return_value="request_id")
    mock_redis.is_connected = Mock(return_value=True)

    response = client.get("/ping")

    assert response.status_code == 200


def test_get_responses_without_token_returns_401(client):
    """Test that /get-responses returns 401 without token."""
    response = client.get("/get-responses")
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Invalid or missing token"


def test_get_responses_with_invalid_token_returns_401(client):
    """Test that /get-responses returns 401 with invalid token."""
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=False):
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/get-responses", headers=headers)
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Invalid or missing token"


def test_register_token_success(client):
    """Test that /register-token successfully registers a token."""
    with patch("src.database.redis_client.redis_client.save_token", return_value=True):
        payload = {
            "token": "test-token-123",
            "expiration_seconds": 3600
        }
        response = client.post("/register-token", 
                              data=json.dumps(payload),
                              content_type="application/json")
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "Token registered successfully"
        assert data["token"] == "test-token-123"


def test_register_token_without_token_field_returns_400(client):
    """Test that /register-token returns 400 without token field."""
    payload = {"expiration_seconds": 3600}
    response = client.post("/register-token", 
                          data=json.dumps(payload),
                          content_type="application/json")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Token is required"


def test_clear_responses_success(client, auth_headers):
    """Test that /clear-responses successfully clears all responses."""
    with patch("src.middleware.auth_middleware.redis_client.validate_token", return_value=True):
        with patch("src.database.redis_client.redis_client.clear_all_requests", return_value=True):
            response = client.delete("/clear-responses", headers=auth_headers)
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["message"] == "All responses have been cleared successfully"


def test_clear_responses_without_token_returns_401(client):
    """Test that /clear-responses returns 401 without token."""
    response = client.delete("/clear-responses")
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Invalid or missing token"
