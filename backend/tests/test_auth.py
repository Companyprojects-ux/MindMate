"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.tests.utils import (
    assert_status_code, assert_json_response, assert_error_response,
    assert_validation_error, assert_unauthorized,
    setup_mock_db_get_user, setup_mock_db_get_user_by_email,
    setup_mock_db_create_user, log_response
)
from backend.tests.report import TestReporter

# Test reporters
register_reporter = TestReporter("/api/auth/register", "POST")
login_reporter = TestReporter("/api/auth/login", "POST")
refresh_reporter = TestReporter("/api/auth/refresh", "POST")
me_get_reporter = TestReporter("/api/auth/me", "GET")
me_put_reporter = TestReporter("/api/auth/me", "PUT")
password_reporter = TestReporter("/api/auth/password", "PUT")

def test_register_success(client: TestClient, test_user_data, mock_db_functions, mock_user, response_capture):
    """Test successful user registration."""
    # Register test
    register_reporter.register_test(
        "test_register_success",
        "Verify that a user can be registered with valid data."
    )
    
    # Set up mocks
    setup_mock_db_get_user_by_email(mock_db_functions, None)  # User doesn't exist yet
    setup_mock_db_create_user(mock_db_functions, mock_user)
    
    # Make request
    response = client.post("/api/auth/register", json=test_user_data)
    response = response_capture.capture(response)
    
    # Register response
    register_reporter.register_response(
        "test_register_success",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 201)
    assert_json_response(response, ["user_id", "email", "name", "created_at", "updated_at"])
    assert response.json()["email"] == test_user_data["email"]
    assert response.json()["name"] == test_user_data["name"]

def test_register_existing_email(client: TestClient, test_user_data, mock_db_functions, mock_user, response_capture):
    """Test registration with an existing email."""
    # Register test
    register_reporter.register_test(
        "test_register_existing_email",
        "Verify that registration fails when the email is already in use."
    )
    
    # Set up mocks
    setup_mock_db_get_user_by_email(mock_db_functions, mock_user)  # User already exists
    
    # Make request
    response = client.post("/api/auth/register", json=test_user_data)
    response = response_capture.capture(response)
    
    # Register response
    register_reporter.register_response(
        "test_register_existing_email",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_error_response(response, 400)

def test_register_invalid_email(client: TestClient, mock_db_functions, response_capture):
    """Test registration with an invalid email."""
    # Register test
    register_reporter.register_test(
        "test_register_invalid_email",
        "Verify that registration fails when the email is invalid."
    )
    
    # Set up mocks
    setup_mock_db_get_user_by_email(mock_db_functions, None)
    
    # Make request
    invalid_user_data = {
        "email": "invalid-email",
        "password": "testpassword123",
        "name": "Test User"
    }
    response = client.post("/api/auth/register", json=invalid_user_data)
    response = response_capture.capture(response)
    
    # Register response
    register_reporter.register_response(
        "test_register_invalid_email",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_validation_error(response, "email")

def test_register_short_password(client: TestClient, mock_db_functions, response_capture):
    """Test registration with a short password."""
    # Register test
    register_reporter.register_test(
        "test_register_short_password",
        "Verify that registration fails when the password is too short."
    )
    
    # Set up mocks
    setup_mock_db_get_user_by_email(mock_db_functions, None)
    
    # Make request
    invalid_user_data = {
        "email": "test@example.com",
        "password": "short",
        "name": "Test User"
    }
    response = client.post("/api/auth/register", json=invalid_user_data)
    response = response_capture.capture(response)
    
    # Register response
    register_reporter.register_response(
        "test_register_short_password",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_validation_error(response, "password")

def test_login_success(client: TestClient, test_user_data, mock_db_functions, mock_user, response_capture):
    """Test successful user login."""
    # Register test
    login_reporter.register_test(
        "test_login_success",
        "Verify that a user can login with valid credentials."
    )
    
    # Set up mocks
    mock_user_with_password = mock_user.copy()
    mock_user_with_password["password_hash"] = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Hash for 'testpassword123'
    setup_mock_db_get_user_by_email(mock_db_functions, mock_user_with_password)
    
    # Make request
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    response = response_capture.capture(response)
    
    # Register response
    login_reporter.register_response(
        "test_login_success",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["access_token", "token_type"])
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_email(client: TestClient, test_user_data, mock_db_functions, response_capture):
    """Test login with an invalid email."""
    # Register test
    login_reporter.register_test(
        "test_login_invalid_email",
        "Verify that login fails when the email is invalid."
    )
    
    # Set up mocks
    setup_mock_db_get_user_by_email(mock_db_functions, None)  # User doesn't exist
    
    # Make request
    login_data = {
        "email": "nonexistent@example.com",
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    response = response_capture.capture(response)
    
    # Register response
    login_reporter.register_response(
        "test_login_invalid_email",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_error_response(response, 401)

def test_login_incorrect_password(client: TestClient, test_user_data, mock_db_functions, mock_user, response_capture):
    """Test login with an incorrect password."""
    # Register test
    login_reporter.register_test(
        "test_login_incorrect_password",
        "Verify that login fails when the password is incorrect."
    )
    
    # Set up mocks
    mock_user_with_password = mock_user.copy()
    mock_user_with_password["password_hash"] = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Hash for 'testpassword123'
    setup_mock_db_get_user_by_email(mock_db_functions, mock_user_with_password)
    
    # Make request
    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    response = response_capture.capture(response)
    
    # Register response
    login_reporter.register_response(
        "test_login_incorrect_password",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_error_response(response, 401)

def test_get_user_profile(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test getting the user profile."""
    # Register test
    me_get_reporter.register_test(
        "test_get_user_profile",
        "Verify that an authenticated user can get their profile."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    
    # Make request
    response = client.get("/api/auth/me", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    me_get_reporter.register_response(
        "test_get_user_profile",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["user_id", "email", "name", "created_at", "updated_at"])
    assert response.json()["user_id"] == mock_user["user_id"]

def test_get_user_profile_unauthenticated(client: TestClient, response_capture):
    """Test getting the user profile without authentication."""
    # Register test
    me_get_reporter.register_test(
        "test_get_user_profile_unauthenticated",
        "Verify that an unauthenticated user cannot get a profile."
    )
    
    # Make request
    response = client.get("/api/auth/me")
    response = response_capture.capture(response)
    
    # Register response
    me_get_reporter.register_response(
        "test_get_user_profile_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_update_user_profile(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test updating the user profile."""
    # Register test
    me_put_reporter.register_test(
        "test_update_user_profile",
        "Verify that an authenticated user can update their profile."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    updated_user = mock_user.copy()
    updated_user["name"] = "Updated Name"
    mock_db_functions["update_user"].return_value = updated_user
    
    # Make request
    update_data = {
        "name": "Updated Name"
    }
    response = client.put("/api/auth/me", json=update_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    me_put_reporter.register_response(
        "test_update_user_profile",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["user_id", "email", "name", "created_at", "updated_at"])
    assert response.json()["name"] == "Updated Name"

def test_update_user_profile_unauthenticated(client: TestClient, response_capture):
    """Test updating the user profile without authentication."""
    # Register test
    me_put_reporter.register_test(
        "test_update_user_profile_unauthenticated",
        "Verify that an unauthenticated user cannot update a profile."
    )
    
    # Make request
    update_data = {
        "name": "Updated Name"
    }
    response = client.put("/api/auth/me", json=update_data)
    response = response_capture.capture(response)
    
    # Register response
    me_put_reporter.register_response(
        "test_update_user_profile_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)
