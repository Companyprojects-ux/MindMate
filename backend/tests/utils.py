"""
Utility functions for API testing.
"""
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

logger = logging.getLogger("api_tests")

def assert_status_code(response, expected_status_code: int):
    """Assert that the response has the expected status code."""
    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, got {response.status_code}. Response: {response.text}"

def assert_json_response(response, expected_keys: List[str]):
    """Assert that the response is JSON and contains the expected keys."""
    try:
        data = response.json()
        assert isinstance(data, dict), f"Expected JSON object, got {type(data)}"
        for key in expected_keys:
            assert key in data, f"Expected key '{key}' not found in response: {data}"
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

def assert_error_response(response, expected_status_code: int, error_key: str = "detail"):
    """Assert that the response is an error with the expected status code."""
    assert_status_code(response, expected_status_code)
    try:
        data = response.json()
        assert error_key in data, f"Expected error key '{error_key}' not found in response: {data}"
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

def assert_list_response(response, expected_status_code: int = 200):
    """Assert that the response is a JSON list."""
    assert_status_code(response, expected_status_code)
    try:
        data = response.json()
        assert isinstance(data, list), f"Expected JSON list, got {type(data)}"
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

def assert_empty_response(response, expected_status_code: int = 204):
    """Assert that the response is empty with the expected status code."""
    assert_status_code(response, expected_status_code)
    assert not response.content, f"Expected empty response, got: {response.content}"

def assert_validation_error(response, field: Optional[str] = None):
    """Assert that the response is a validation error."""
    assert_status_code(response, 422)
    try:
        data = response.json()
        assert "detail" in data, f"Expected 'detail' key in validation error response: {data}"
        if field:
            found = False
            for error in data["detail"]:
                if field in error.get("loc", []):
                    found = True
                    break
            assert found, f"Expected validation error for field '{field}' not found in response: {data}"
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

def assert_unauthorized(response):
    """Assert that the response is an unauthorized error."""
    assert_error_response(response, 401)

def assert_forbidden(response):
    """Assert that the response is a forbidden error."""
    assert_error_response(response, 403)

def assert_not_found(response):
    """Assert that the response is a not found error."""
    assert_error_response(response, 404)

def setup_mock_db_get_user(mock_db_functions, mock_user):
    """Set up the mock database function to return the mock user."""
    mock_db_functions["get_user_by_id"].return_value = mock_user

def setup_mock_db_get_user_by_email(mock_db_functions, mock_user):
    """Set up the mock database function to return the mock user by email."""
    mock_db_functions["get_user_by_email"].return_value = mock_user

def setup_mock_db_create_user(mock_db_functions, mock_user):
    """Set up the mock database function to return the mock user on creation."""
    mock_db_functions["create_user"].return_value = mock_user

def setup_mock_db_create_item(mock_db_functions, mock_item):
    """Set up the mock database function to return the mock item on creation."""
    mock_db_functions["create_item"].return_value = mock_item

def setup_mock_db_get_item(mock_db_functions, mock_item):
    """Set up the mock database function to return the mock item."""
    mock_db_functions["get_item"].return_value = mock_item

def setup_mock_db_update_item(mock_db_functions, mock_item):
    """Set up the mock database function to return the mock item on update."""
    mock_db_functions["update_item"].return_value = mock_item

def setup_mock_db_query_items(mock_db_functions, mock_items):
    """Set up the mock database function to return the mock items on query."""
    mock_db_functions["query_items"].return_value = mock_items

def setup_mock_ai_service(mock_ai_service, **kwargs):
    """Set up the mock AI service functions with the provided return values."""
    for func_name, return_value in kwargs.items():
        if func_name in mock_ai_service:
            if callable(return_value):
                mock_ai_service[func_name].side_effect = return_value
            else:
                mock_ai_service[func_name].return_value = return_value

def create_test_user(client: TestClient, user_data: Dict[str, Any], mock_db_functions, mock_user):
    """Create a test user and return the response."""
    setup_mock_db_get_user_by_email(mock_db_functions, None)  # User doesn't exist yet
    setup_mock_db_create_user(mock_db_functions, mock_user)
    response = client.post("/api/auth/register", json=user_data)
    logger.info(f"Created test user: {response.json() if response.status_code == 201 else response.text}")
    return response

def login_test_user(client: TestClient, user_data: Dict[str, Any], mock_db_functions, mock_user):
    """Login a test user and return the response."""
    setup_mock_db_get_user_by_email(mock_db_functions, mock_user)
    mock_user_with_password = mock_user.copy()
    mock_user_with_password["password_hash"] = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Hash for 'testpassword123'
    setup_mock_db_get_user_by_email(mock_db_functions, mock_user_with_password)
    response = client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    logger.info(f"Logged in test user: {response.json() if response.status_code == 200 else response.text}")
    return response

def log_response(response, message: str = "Response"):
    """Log a response for debugging."""
    try:
        response_json = response.json()
        logger.info(f"{message}: {json.dumps(response_json, indent=2)}")
    except:
        logger.info(f"{message}: {response.text}")
    return response
