"""
Tests for AI recommendations endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

from backend.tests.utils import (
    assert_status_code, assert_json_response, assert_error_response,
    assert_unauthorized, setup_mock_db_get_user, log_response
)
from backend.tests.report import TestReporter

# Test reporters
recommendations_reporter = TestReporter("/api/ai/recommendations", "GET")

def test_get_ai_recommendations(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test getting AI recommendations."""
    # Register test
    recommendations_reporter.register_test(
        "test_get_ai_recommendations",
        "Verify that an authenticated user can get AI recommendations."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    
    # Mock mood and journal services
    mock_mood_data = [
        {"mood_rating": 7, "timestamp": "2023-05-01T12:00:00", "notes": "Feeling good"}
    ]
    mock_journal_data = [
        {"content": "Today was a good day.", "timestamp": "2023-05-01T20:00:00", "title": "Good Day"}
    ]
    
    # Mock recommendation service
    mock_recommendations = {
        "journal_prompts": [
            {"title": "Test Prompt", "prompt": "This is a test prompt."}
        ],
        "coping_strategies": [
            {"title": "Test Strategy", "description": "This is a test strategy."}
        ],
        "timestamp": "2023-05-02T10:00:00",
        "user_id": mock_user["user_id"]
    }
    
    with patch("backend.services.mood_service.list_mood_entries", AsyncMock(return_value=mock_mood_data)), \
         patch("backend.services.journal_service.list_journal_entries", AsyncMock(return_value=mock_journal_data)), \
         patch("backend.services.recommendation_service.generate_recommendations", AsyncMock(return_value=mock_recommendations)):
        
        # Make request
        response = client.get("/api/ai/recommendations", headers=auth_headers)
        response = response_capture.capture(response)
        
        # Register response
        recommendations_reporter.register_response(
            "test_get_ai_recommendations",
            response.status_code,
            response.json()
        )
        
        # Assert response
        assert_status_code(response, 200)
        assert_json_response(response, ["journal_prompts", "coping_strategies", "timestamp", "user_id"])
        assert response.json()["journal_prompts"][0]["title"] == "Test Prompt"
        assert response.json()["coping_strategies"][0]["title"] == "Test Strategy"
        assert response.json()["user_id"] == mock_user["user_id"]

def test_get_ai_recommendations_unauthenticated(client: TestClient, response_capture):
    """Test getting AI recommendations without authentication."""
    # Register test
    recommendations_reporter.register_test(
        "test_get_ai_recommendations_unauthenticated",
        "Verify that an unauthenticated user cannot get AI recommendations."
    )
    
    # Make request
    response = client.get("/api/ai/recommendations")
    response = response_capture.capture(response)
    
    # Register response
    recommendations_reporter.register_response(
        "test_get_ai_recommendations_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_ai_recommendations_error(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test getting AI recommendations with an error."""
    # Register test
    recommendations_reporter.register_test(
        "test_get_ai_recommendations_error",
        "Verify that an error in the recommendation service is handled properly."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    
    # Mock services with error
    with patch("backend.services.mood_service.list_mood_entries", AsyncMock(side_effect=Exception("Test error"))):
        
        # Make request
        response = client.get("/api/ai/recommendations", headers=auth_headers)
        response = response_capture.capture(response)
        
        # Register response
        recommendations_reporter.register_response(
            "test_get_ai_recommendations_error",
            response.status_code,
            response.json()
        )
        
        # Assert response
        assert_error_response(response, 500)
        assert "detail" in response.json()
        assert "Test error" in response.json()["detail"]
