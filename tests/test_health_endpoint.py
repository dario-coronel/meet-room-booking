import json
from datetime import datetime

import pytest

from src.controllers.health_controller import create_app


@pytest.fixture
def client():
    """Create test client for Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint_returns_200(client):
    """Test that /health returns status code 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """Test that /health returns valid JSON."""
    response = client.get("/health")
    assert response.content_type == "application/json"

    data = json.loads(response.data)
    assert isinstance(data, dict)


def test_health_endpoint_contains_required_fields(client):
    """Test that /health response contains status and timestamp."""
    response = client.get("/health")
    data = json.loads(response.data)

    assert "status" in data
    assert "timestamp" in data
    assert data["status"] == "ok"


def test_health_endpoint_timestamp_format(client):
    """Test that timestamp is in correct ISO format."""
    response = client.get("/health")
    data = json.loads(response.data)

    # Should be able to parse the timestamp
    timestamp_str = data["timestamp"]
    parsed_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    assert isinstance(parsed_time, datetime)


def test_health_endpoint_response_time(client):
    """Test that /health responds quickly (under 100ms)."""
    import time

    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000
    assert response_time_ms < 100
    assert response.status_code == 200
