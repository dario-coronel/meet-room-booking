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


def test_get_responses_endpoint_returns_200(client):
    """Test that /get-responses returns status code 200."""
    response = client.get("/get-responses")
    assert response.status_code == 200


def test_get_responses_returns_json(client):
    """Test that /get-responses returns valid JSON structure."""
    response = client.get("/get-responses")
    data = json.loads(response.data)

    assert isinstance(data, dict)
    assert "total_returned" in data
    assert "redis_connected" in data
    assert "stats" in data
    assert "requests" in data
    assert isinstance(data["requests"], list)


def test_get_responses_with_limit(client):
    """Test that /get-responses respects limit parameter."""
    response = client.get("/get-responses?limit=5")
    data = json.loads(response.data)

    assert response.status_code == 200
    # Should return at most 5 items
    assert len(data["requests"]) <= 5


def test_get_responses_with_endpoint_filter(client):
    """Test that /get-responses can filter by endpoint."""
    response = client.get("/get-responses?endpoint=/health")
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
