"""
Tests for reminder endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.tests.utils import (
    assert_status_code, assert_json_response, assert_error_response,
    assert_validation_error, assert_unauthorized, assert_not_found,
    assert_list_response, assert_empty_response,
    setup_mock_db_get_user, setup_mock_db_create_item,
    setup_mock_db_get_item, setup_mock_db_update_item,
    setup_mock_db_query_items, log_response
)
from backend.tests.report import TestReporter

# Test reporters
create_reminder_reporter = TestReporter("/api/reminders", "POST")
list_reminders_reporter = TestReporter("/api/reminders", "GET")
today_reminders_reporter = TestReporter("/api/reminders/today", "GET")
upcoming_reminders_reporter = TestReporter("/api/reminders/upcoming", "GET")
get_reminder_reporter = TestReporter("/api/reminders/{reminder_id}", "GET")
update_reminder_reporter = TestReporter("/api/reminders/{reminder_id}", "PUT")
update_status_reporter = TestReporter("/api/reminders/{reminder_id}/status", "PUT")
delete_reminder_reporter = TestReporter("/api/reminders/{reminder_id}", "DELETE")

def test_create_reminder(client: TestClient, auth_headers, mock_db_functions, mock_user, test_reminder_data, test_reminder_id, test_medication_id, response_capture):
    """Test creating a reminder."""
    # Register test
    create_reminder_reporter.register_test(
        "test_create_reminder",
        "Verify that an authenticated user can create a reminder."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medication = {
        "medication_id": test_medication_id,
        "user_id": mock_user["user_id"],
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "daily",
        "time_of_day": "morning",
        "start_date": "2023-05-01",
        "notes": "Take with food",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_get_item(mock_db_functions, mock_medication)
    mock_reminder = {
        "reminder_id": test_reminder_id,
        "user_id": mock_user["user_id"],
        "medication_id": test_medication_id,
        "scheduled_time": test_reminder_data["scheduled_time"],
        "status": "pending",
        "notes": test_reminder_data["notes"],
        "created_at": 1620000000,
        "updated_at": 1620000000,
        "medication": mock_medication
    }
    setup_mock_db_create_item(mock_db_functions, mock_reminder)
    
    # Make request
    response = client.post("/api/reminders", json=test_reminder_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    create_reminder_reporter.register_response(
        "test_create_reminder",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 201)
    assert_json_response(response, ["reminder_id", "user_id", "medication_id", "scheduled_time", "status", "notes", "created_at", "updated_at", "medication"])
    assert response.json()["medication_id"] == test_medication_id
    assert response.json()["scheduled_time"] == test_reminder_data["scheduled_time"]
    assert response.json()["notes"] == test_reminder_data["notes"]
    assert response.json()["medication"]["medication_id"] == test_medication_id

def test_create_reminder_unauthenticated(client: TestClient, test_reminder_data, response_capture):
    """Test creating a reminder without authentication."""
    # Register test
    create_reminder_reporter.register_test(
        "test_create_reminder_unauthenticated",
        "Verify that an unauthenticated user cannot create a reminder."
    )
    
    # Make request
    response = client.post("/api/reminders", json=test_reminder_data)
    response = response_capture.capture(response)
    
    # Register response
    create_reminder_reporter.register_response(
        "test_create_reminder_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_create_reminder_medication_not_found(client: TestClient, auth_headers, mock_db_functions, mock_user, test_reminder_data, response_capture):
    """Test creating a reminder for a medication that doesn't exist."""
    # Register test
    create_reminder_reporter.register_test(
        "test_create_reminder_medication_not_found",
        "Verify that creating a reminder for a non-existent medication returns a 404 error."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_db_get_item(mock_db_functions, None)  # Medication doesn't exist
    
    # Make request
    response = client.post("/api/reminders", json=test_reminder_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    create_reminder_reporter.register_response(
        "test_create_reminder_medication_not_found",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_not_found(response)

def test_list_reminders(client: TestClient, auth_headers, mock_db_functions, mock_user, test_reminder_id, test_medication_id, response_capture):
    """Test listing reminders."""
    # Register test
    list_reminders_reporter.register_test(
        "test_list_reminders",
        "Verify that an authenticated user can list their reminders."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medication = {
        "medication_id": test_medication_id,
        "user_id": mock_user["user_id"],
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "daily",
        "time_of_day": "morning",
        "start_date": "2023-05-01",
        "notes": "Take with food",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    mock_reminders = [
        {
            "reminder_id": test_reminder_id,
            "user_id": mock_user["user_id"],
            "medication_id": test_medication_id,
            "scheduled_time": "2023-05-01T08:00:00",
            "status": "pending",
            "notes": "Take with breakfast",
            "created_at": 1620000000,
            "updated_at": 1620000000,
            "medication": mock_medication
        },
        {
            "reminder_id": "another-test-reminder-id",
            "user_id": mock_user["user_id"],
            "medication_id": test_medication_id,
            "scheduled_time": "2023-05-01T20:00:00",
            "status": "pending",
            "notes": "Take with dinner",
            "created_at": 1620000000,
            "updated_at": 1620000000,
            "medication": mock_medication
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_reminders)
    
    # Make request
    response = client.get("/api/reminders", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    list_reminders_reporter.register_response(
        "test_list_reminders",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 2
    assert response.json()[0]["reminder_id"] == test_reminder_id
    assert response.json()[1]["reminder_id"] == "another-test-reminder-id"

def test_list_reminders_unauthenticated(client: TestClient, response_capture):
    """Test listing reminders without authentication."""
    # Register test
    list_reminders_reporter.register_test(
        "test_list_reminders_unauthenticated",
        "Verify that an unauthenticated user cannot list reminders."
    )
    
    # Make request
    response = client.get("/api/reminders")
    response = response_capture.capture(response)
    
    # Register response
    list_reminders_reporter.register_response(
        "test_list_reminders_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_today_reminders(client: TestClient, auth_headers, mock_db_functions, mock_user, test_reminder_id, test_medication_id, response_capture):
    """Test getting today's reminders."""
    # Register test
    today_reminders_reporter.register_test(
        "test_get_today_reminders",
        "Verify that an authenticated user can get today's reminders."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medication = {
        "medication_id": test_medication_id,
        "user_id": mock_user["user_id"],
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "daily",
        "time_of_day": "morning",
        "start_date": "2023-05-01",
        "notes": "Take with food",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    mock_reminders = [
        {
            "reminder_id": test_reminder_id,
            "user_id": mock_user["user_id"],
            "medication_id": test_medication_id,
            "scheduled_time": "2023-05-01T08:00:00",
            "status": "pending",
            "notes": "Take with breakfast",
            "created_at": 1620000000,
            "updated_at": 1620000000,
            "medication": mock_medication
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_reminders)
    
    # Make request
    response = client.get("/api/reminders/today", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    today_reminders_reporter.register_response(
        "test_get_today_reminders",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 1
    assert response.json()[0]["reminder_id"] == test_reminder_id

def test_get_upcoming_reminders(client: TestClient, auth_headers, mock_db_functions, mock_user, test_reminder_id, test_medication_id, response_capture):
    """Test getting upcoming reminders."""
    # Register test
    upcoming_reminders_reporter.register_test(
        "test_get_upcoming_reminders",
        "Verify that an authenticated user can get upcoming reminders."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medication = {
        "medication_id": test_medication_id,
        "user_id": mock_user["user_id"],
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "daily",
        "time_of_day": "morning",
        "start_date": "2023-05-01",
        "notes": "Take with food",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    mock_reminders = [
        {
            "reminder_id": test_reminder_id,
            "user_id": mock_user["user_id"],
            "medication_id": test_medication_id,
            "scheduled_time": "2023-05-01T08:00:00",
            "status": "pending",
            "notes": "Take with breakfast",
            "created_at": 1620000000,
            "updated_at": 1620000000,
            "medication": mock_medication
        },
        {
            "reminder_id": "another-test-reminder-id",
            "user_id": mock_user["user_id"],
            "medication_id": test_medication_id,
            "scheduled_time": "2023-05-02T08:00:00",
            "status": "pending",
            "notes": "Take with breakfast",
            "created_at": 1620000000,
            "updated_at": 1620000000,
            "medication": mock_medication
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_reminders)
    
    # Make request
    response = client.get("/api/reminders/upcoming?days=7", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    upcoming_reminders_reporter.register_response(
        "test_get_upcoming_reminders",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 2
    assert response.json()[0]["reminder_id"] == test_reminder_id
    assert response.json()[1]["reminder_id"] == "another-test-reminder-id"

def test_get_reminder(client: TestClient, auth_headers, mock_db_functions, mock_user, test_reminder_id, test_medication_id, response_capture):
    """Test getting a reminder by ID."""
    # Register test
    get_reminder_reporter.register_test(
        "test_get_reminder",
        "Verify that an authenticated user can get a reminder by ID."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medication = {
        "medication_id": test_medication_id,
        "user_id": mock_user["user_id"],
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "daily",
        "time_of_day": "morning",
        "start_date": "2023-05-01",
        "notes": "Take with food",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    mock_reminder = {
        "reminder_id": test_reminder_id,
        "user_id": mock_user["user_id"],
        "medication_id": test_medication_id,
        "scheduled_time": "2023-05-01T08:00:00",
        "status": "pending",
        "notes": "Take with breakfast",
        "created_at": 1620000000,
        "updated_at": 1620000000,
        "medication": mock_medication
    }
    setup_mock_db_get_item(mock_db_functions, mock_reminder)
    
    # Make request
    response = client.get(f"/api/reminders/{test_reminder_id}", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_reminder_reporter.register_response(
        "test_get_reminder",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["reminder_id", "user_id", "medication_id", "scheduled_time", "status", "notes", "created_at", "updated_at", "medication"])
    assert response.json()["reminder_id"] == test_reminder_id
