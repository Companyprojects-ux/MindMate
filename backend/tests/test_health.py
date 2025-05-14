"""
Tests for the health check endpoint.
"""
import pytest
from fastapi.testclient import TestClient

from backend.tests.utils import assert_status_code
from backend.tests.report import TestReporter

# Test reporter
health_reporter = TestReporter("/api/health", "GET")

def test_health_check(client: TestClient, response_capture):
    """Test the health check endpoint."""
    # Register test
    health_reporter.register_test(
        "test_health_check",
        "Verify that the health check endpoint returns a 200 status code and the expected response."
    )
    
    # Make request
    response = client.get("/api/health")
    response = response_capture.capture(response)
    
    # Register response
    health_reporter.register_response(
        "test_health_check",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert response.json() == {"status": "healthy"}
