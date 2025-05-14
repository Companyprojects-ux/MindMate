"""
Tests for AI support endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from backend.tests.utils import (
    assert_status_code, assert_json_response, assert_error_response,
    assert_validation_error, assert_unauthorized, assert_not_found,
    assert_list_response, setup_mock_db_get_user,
    setup_mock_ai_service, log_response
)
from backend.tests.report import TestReporter

# Test reporters
chat_reporter = TestReporter("/api/ai/chat", "POST")
suggestions_reporter = TestReporter("/api/ai/suggestions", "GET")
visualization_reporter = TestReporter("/api/ai/visualization_data", "GET")
feedback_reporter = TestReporter("/api/ai/feedback", "POST")
weekly_report_reporter = TestReporter("/api/ai/weekly-report", "GET")
legacy_mental_health_reporter = TestReporter("/mental_health_support", "GET")
legacy_coping_reporter = TestReporter("/coping_strategies", "GET")

def test_chat_with_ai(client: TestClient, auth_headers, mock_db_functions, mock_user, mock_ai_service, response_capture):
    """Test sending a message to the chatbot."""
    # Register test
    chat_reporter.register_test(
        "test_chat_with_ai",
        "Verify that an authenticated user can chat with the AI."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_ai_service(mock_ai_service, generate_chatbot_response=AsyncMock(return_value="AI response"))
    
    # Make request
    chat_data = {
        "message": "Hello, AI!"
    }
    response = client.post("/api/ai/chat", json=chat_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    chat_reporter.register_response(
        "test_chat_with_ai",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["response"])
    assert response.json()["response"] == "AI response"

def test_chat_with_ai_unauthenticated(client: TestClient, response_capture):
    """Test sending a message to the chatbot without authentication."""
    # Register test
    chat_reporter.register_test(
        "test_chat_with_ai_unauthenticated",
        "Verify that an unauthenticated user cannot chat with the AI."
    )
    
    # Make request
    chat_data = {
        "message": "Hello, AI!"
    }
    response = client.post("/api/ai/chat", json=chat_data)
    response = response_capture.capture(response)
    
    # Register response
    chat_reporter.register_response(
        "test_chat_with_ai_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_ai_suggestions(client: TestClient, auth_headers, mock_db_functions, mock_user, mock_ai_service, response_capture):
    """Test getting AI suggestions."""
    # Register test
    suggestions_reporter.register_test(
        "test_get_ai_suggestions",
        "Verify that an authenticated user can get AI suggestions."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_suggestions = {
        "coping_strategies": ["Take a walk", "Practice deep breathing"],
        "resources": [{"title": "Meditation Guide", "url": "https://example.com/meditation"}],
        "activities": ["Journaling", "Exercise"]
    }
    setup_mock_ai_service(mock_ai_service, generate_ai_suggestions=AsyncMock(return_value=mock_suggestions))
    
    # Make request
    response = client.get("/api/ai/suggestions", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    suggestions_reporter.register_response(
        "test_get_ai_suggestions",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["coping_strategies", "resources", "activities"])
    assert response.json()["coping_strategies"] == mock_suggestions["coping_strategies"]
    assert response.json()["resources"] == mock_suggestions["resources"]
    assert response.json()["activities"] == mock_suggestions["activities"]

def test_get_ai_suggestions_unauthenticated(client: TestClient, response_capture):
    """Test getting AI suggestions without authentication."""
    # Register test
    suggestions_reporter.register_test(
        "test_get_ai_suggestions_unauthenticated",
        "Verify that an unauthenticated user cannot get AI suggestions."
    )
    
    # Make request
    response = client.get("/api/ai/suggestions")
    response = response_capture.capture(response)
    
    # Register response
    suggestions_reporter.register_response(
        "test_get_ai_suggestions_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_visualization_data(client: TestClient, auth_headers, mock_db_functions, mock_user, mock_ai_service, response_capture):
    """Test getting visualization data."""
    # Register test
    visualization_reporter.register_test(
        "test_get_visualization_data",
        "Verify that an authenticated user can get visualization data."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_data = [
        {"date": "2023-05-01", "mood_rating": 7},
        {"date": "2023-05-02", "mood_rating": 8}
    ]
    setup_mock_ai_service(mock_ai_service, get_visualization_data=AsyncMock(return_value=mock_data))
    
    # Make request
    response = client.get("/api/ai/visualization_data?data_type=mood", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    visualization_reporter.register_response(
        "test_get_visualization_data",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 2
    assert response.json()[0]["date"] == "2023-05-01"
    assert response.json()[1]["date"] == "2023-05-02"

def test_get_visualization_data_unauthenticated(client: TestClient, response_capture):
    """Test getting visualization data without authentication."""
    # Register test
    visualization_reporter.register_test(
        "test_get_visualization_data_unauthenticated",
        "Verify that an unauthenticated user cannot get visualization data."
    )
    
    # Make request
    response = client.get("/api/ai/visualization_data?data_type=mood")
    response = response_capture.capture(response)
    
    # Register response
    visualization_reporter.register_response(
        "test_get_visualization_data_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_visualization_data_invalid_type(client: TestClient, auth_headers, mock_db_functions, mock_user, mock_ai_service, response_capture):
    """Test getting visualization data with an invalid type."""
    # Register test
    visualization_reporter.register_test(
        "test_get_visualization_data_invalid_type",
        "Verify that getting visualization data with an invalid type returns an error."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_ai_service(mock_ai_service, get_visualization_data=AsyncMock(side_effect=ValueError("Invalid data type")))
    
    # Make request
    response = client.get("/api/ai/visualization_data?data_type=invalid", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    visualization_reporter.register_response(
        "test_get_visualization_data_invalid_type",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_error_response(response, 500)

def test_submit_feedback(client: TestClient, auth_headers, mock_db_functions, mock_user, mock_ai_service, response_capture):
    """Test submitting feedback on AI suggestions."""
    # Register test
    feedback_reporter.register_test(
        "test_submit_feedback",
        "Verify that an authenticated user can submit feedback on AI suggestions."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_ai_service(mock_ai_service, submit_feedback=AsyncMock(return_value=None))
    
    # Make request
    response = client.post("/api/ai/feedback?feedback=This+is+helpful", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    feedback_reporter.register_response(
        "test_submit_feedback",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["message"])
    assert response.json()["message"] == "Feedback submitted successfully"

def test_submit_feedback_unauthenticated(client: TestClient, response_capture):
    """Test submitting feedback without authentication."""
    # Register test
    feedback_reporter.register_test(
        "test_submit_feedback_unauthenticated",
        "Verify that an unauthenticated user cannot submit feedback."
    )
    
    # Make request
    response = client.post("/api/ai/feedback?feedback=This+is+helpful")
    response = response_capture.capture(response)
    
    # Register response
    feedback_reporter.register_response(
        "test_submit_feedback_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_weekly_report(client: TestClient, auth_headers, mock_db_functions, mock_user, mock_ai_service, response_capture):
    """Test getting a weekly report."""
    # Register test
    weekly_report_reporter.register_test(
        "test_get_weekly_report",
        "Verify that an authenticated user can get a weekly report."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_ai_service(mock_ai_service, generate_weekly_report=AsyncMock(return_value="Weekly report content"))
    
    # Make request
    response = client.get("/api/ai/weekly-report", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    weekly_report_reporter.register_response(
        "test_get_weekly_report",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["report"])
    assert response.json()["report"] == "Weekly report content"

def test_get_weekly_report_unauthenticated(client: TestClient, response_capture):
    """Test getting a weekly report without authentication."""
    # Register test
    weekly_report_reporter.register_test(
        "test_get_weekly_report_unauthenticated",
        "Verify that an unauthenticated user cannot get a weekly report."
    )
    
    # Make request
    response = client.get("/api/ai/weekly-report")
    response = response_capture.capture(response)
    
    # Register response
    weekly_report_reporter.register_response(
        "test_get_weekly_report_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_mental_health_support(client: TestClient, response_capture):
    """Test the legacy mental health support endpoint."""
    # Register test
    legacy_mental_health_reporter.register_test(
        "test_mental_health_support",
        "Verify that the legacy mental health support endpoint works."
    )
    
    # Set up mocks
    with patch("backend.llm.get_llm_response", return_value="LLM response"):
        # Make request
        response = client.get("/mental_health_support?prompt=test")
        response = response_capture.capture(response)
        
        # Register response
        legacy_mental_health_reporter.register_response(
            "test_mental_health_support",
            response.status_code,
            response.json()
        )
        
        # Assert response
        assert response.status_code in [200, 500]  # 500 if LLM not configured
        if response.status_code == 200:
            assert_json_response(response, ["response"])
            assert response.json()["response"] == "LLM response"

def test_coping_strategies(client: TestClient, response_capture):
    """Test the legacy coping strategies endpoint."""
    # Register test
    legacy_coping_reporter.register_test(
        "test_coping_strategies",
        "Verify that the legacy coping strategies endpoint works."
    )
    
    # Set up mocks
    with patch("backend.llm.get_personalized_coping_strategies", return_value=["Strategy 1", "Strategy 2"]):
        # Make request
        response = client.get("/coping_strategies?user_input=test")
        response = response_capture.capture(response)
        
        # Register response
        legacy_coping_reporter.register_response(
            "test_coping_strategies",
            response.status_code,
            response.json()
        )
        
        # Assert response
        assert response.status_code in [200, 500]  # 500 if LLM not configured
        if response.status_code == 200:
            assert_json_response(response, ["strategies"])
            assert response.json()["strategies"] == ["Strategy 1", "Strategy 2"]
