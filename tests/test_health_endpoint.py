import json
import time
from datetime import datetime

import pytest

from src.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint_exists(client):
    """Test that the /health endpoint exists and returns 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """Test that the /health endpoint returns valid JSON."""
    response = client.get("/health")
    assert response.content_type == "application/json"

    # Verify it's valid JSON by parsing it
    data = json.loads(response.data)
    assert isinstance(data, dict)


def test_health_endpoint_status_ok(client):
    """Test that the /health endpoint returns status 'ok'."""
    response = client.get("/health")
    data = json.loads(response.data)

    # TP Requirement: Must have "status": "ok"
    assert "status" in data
    assert data["status"] == "ok"


def test_health_endpoint_has_timestamp(client):
    """Test that the /health endpoint includes a timestamp."""
    response = client.get("/health")
    data = json.loads(response.data)

    # TP Requirement: Should include timestamp
    assert "timestamp" in data
    assert data["timestamp"] is not None


def test_health_endpoint_timestamp_format(client):
    """Test that the timestamp is in ISO format."""
    response = client.get("/health")
    data = json.loads(response.data)

    # Verify timestamp is parseable ISO format
    timestamp = data["timestamp"]
    parsed_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    assert isinstance(parsed_time, datetime)


def test_health_endpoint_response_time(client):
    """Test that the /health endpoint responds in less than 100ms."""
    # TP Requirement: Must respond in < 100ms
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000
    assert response_time_ms < 100  # Less than 100ms
    assert response.status_code == 200


def test_health_endpoint_no_auth_required(client):
    """Test that the /health endpoint doesn't require authentication."""
    # TP Requirement: No authentication required
    response = client.get("/health")
    assert response.status_code == 200
    # Should not return 401 Unauthorized or 403 Forbidden
    assert response.status_code not in [401, 403]


def test_health_endpoint_no_headers_required(client):
    """Test that the /health endpoint works without special headers."""
    # TP Requirement: No special headers required
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_get_method_only(client):
    """Test that the /health endpoint only accepts GET requests."""
    # Should work with GET
    response = client.get("/health")
    assert response.status_code == 200

    # Should not work with other methods
    response = client.post("/health")
    assert response.status_code == 405  # Method Not Allowed

    response = client.put("/health")
    assert response.status_code == 405

    response = client.delete("/health")
    assert response.status_code == 405


def test_health_endpoint_consistent_response(client):
    """Test that the /health endpoint returns consistent responses."""
    # Make multiple requests
    responses = []
    for _ in range(3):
        response = client.get("/health")
        data = json.loads(response.data)
        responses.append(data)
        time.sleep(0.01)  # Small delay

    # All should have status 'ok'
    for response_data in responses:
        assert response_data["status"] == "ok"
        assert "timestamp" in response_data


def test_health_endpoint_json_structure(client):
    """Test the exact JSON structure matches TP requirements."""
    response = client.get("/health")
    data = json.loads(response.data)

    # TP specifies exact structure
    assert len(data) == 2  # Should have exactly 2 fields
    assert "status" in data
    assert "timestamp" in data
    assert data["status"] == "ok"

    # Timestamp should be string in ISO format
    assert isinstance(data["timestamp"], str)
    assert "T" in data["timestamp"]  # ISO format indicator


def test_health_endpoint_multiple_concurrent_requests(client):
    """Test that the /health endpoint handles multiple requests."""
    import threading

    results = []

    def make_request():
        response = client.get("/health")
        results.append(response.status_code)

    # Make multiple concurrent requests
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # All requests should return 200
    assert all(status == 200 for status in results)
    assert len(results) == 5
