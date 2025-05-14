"""
Tests for medication endpoints.
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
create_medication_reporter = TestReporter("/api/medications", "POST")
list_medications_reporter = TestReporter("/api/medications", "GET")
get_medication_reporter = TestReporter("/api/medications/{medication_id}", "GET")
update_medication_reporter = TestReporter("/api/medications/{medication_id}", "PUT")
delete_medication_reporter = TestReporter("/api/medications/{medication_id}", "DELETE")
upload_image_reporter = TestReporter("/api/medications/{medication_id}/image", "POST")

def test_create_medication(client: TestClient, auth_headers, mock_db_functions, mock_user, test_medication_data, test_medication_id, response_capture):
    """Test creating a medication."""
    # Register test
    create_medication_reporter.register_test(
        "test_create_medication",
        "Verify that an authenticated user can create a medication."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medication = {
        "medication_id": test_medication_id,
        "user_id": mock_user["user_id"],
        "name": test_medication_data["name"],
        "dosage": test_medication_data["dosage"],
        "frequency": test_medication_data["frequency"],
        "time_of_day": test_medication_data["time_of_day"],
        "start_date": test_medication_data["start_date"],
        "notes": test_medication_data["notes"],
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_create_item(mock_db_functions, mock_medication)
    
    # Make request
    response = client.post("/api/medications", json=test_medication_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    create_medication_reporter.register_response(
        "test_create_medication",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 201)
    assert_json_response(response, ["medication_id", "user_id", "name", "dosage", "frequency", "created_at", "updated_at"])
    assert response.json()["name"] == test_medication_data["name"]
    assert response.json()["dosage"] == test_medication_data["dosage"]
    assert response.json()["frequency"] == test_medication_data["frequency"]

def test_create_medication_unauthenticated(client: TestClient, test_medication_data, response_capture):
    """Test creating a medication without authentication."""
    # Register test
    create_medication_reporter.register_test(
        "test_create_medication_unauthenticated",
        "Verify that an unauthenticated user cannot create a medication."
    )
    
    # Make request
    response = client.post("/api/medications", json=test_medication_data)
    response = response_capture.capture(response)
    
    # Register response
    create_medication_reporter.register_response(
        "test_create_medication_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_list_medications(client: TestClient, auth_headers, mock_db_functions, mock_user, test_medication_id, response_capture):
    """Test listing medications."""
    # Register test
    list_medications_reporter.register_test(
        "test_list_medications",
        "Verify that an authenticated user can list their medications."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medications = [
        {
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
        },
        {
            "medication_id": "another-test-medication-id",
            "user_id": mock_user["user_id"],
            "name": "Another Test Medication",
            "dosage": "5mg",
            "frequency": "twice daily",
            "time_of_day": "morning and evening",
            "start_date": "2023-05-02",
            "notes": "Take after meals",
            "created_at": 1620086400,
            "updated_at": 1620086400
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_medications)
    
    # Make request
    response = client.get("/api/medications", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    list_medications_reporter.register_response(
        "test_list_medications",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 2
    assert response.json()[0]["medication_id"] == test_medication_id
    assert response.json()[1]["medication_id"] == "another-test-medication-id"

def test_list_medications_unauthenticated(client: TestClient, response_capture):
    """Test listing medications without authentication."""
    # Register test
    list_medications_reporter.register_test(
        "test_list_medications_unauthenticated",
        "Verify that an unauthenticated user cannot list medications."
    )
    
    # Make request
    response = client.get("/api/medications")
    response = response_capture.capture(response)
    
    # Register response
    list_medications_reporter.register_response(
        "test_list_medications_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_search_medications(client: TestClient, auth_headers, mock_db_functions, mock_user, test_medication_id, response_capture):
    """Test searching medications."""
    # Register test
    list_medications_reporter.register_test(
        "test_search_medications",
        "Verify that an authenticated user can search their medications."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_medications = [
        {
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
    ]
    setup_mock_db_query_items(mock_db_functions, mock_medications)
    
    # Make request
    response = client.get("/api/medications?query=test", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    list_medications_reporter.register_response(
        "test_search_medications",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 1
    assert response.json()[0]["medication_id"] == test_medication_id

def test_get_medication(client: TestClient, auth_headers, mock_db_functions, mock_user, test_medication_id, response_capture):
    """Test getting a medication by ID."""
    # Register test
    get_medication_reporter.register_test(
        "test_get_medication",
        "Verify that an authenticated user can get a medication by ID."
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
    
    # Make request
    response = client.get(f"/api/medications/{test_medication_id}", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_medication_reporter.register_response(
        "test_get_medication",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["medication_id", "user_id", "name", "dosage", "frequency", "created_at", "updated_at"])
    assert response.json()["medication_id"] == test_medication_id

def test_get_medication_not_found(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test getting a medication that doesn't exist."""
    # Register test
    get_medication_reporter.register_test(
        "test_get_medication_not_found",
        "Verify that getting a non-existent medication returns a 404 error."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_db_get_item(mock_db_functions, None)  # Medication doesn't exist
    
    # Make request
    response = client.get("/api/medications/nonexistent-id", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_medication_reporter.register_response(
        "test_get_medication_not_found",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_not_found(response)

def test_get_medication_unauthenticated(client: TestClient, test_medication_id, response_capture):
    """Test getting a medication without authentication."""
    # Register test
    get_medication_reporter.register_test(
        "test_get_medication_unauthenticated",
        "Verify that an unauthenticated user cannot get a medication."
    )
    
    # Make request
    response = client.get(f"/api/medications/{test_medication_id}")
    response = response_capture.capture(response)
    
    # Register response
    get_medication_reporter.register_response(
        "test_get_medication_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_update_medication(client: TestClient, auth_headers, mock_db_functions, mock_user, test_medication_id, response_capture):
    """Test updating a medication."""
    # Register test
    update_medication_reporter.register_test(
        "test_update_medication",
        "Verify that an authenticated user can update a medication."
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
    updated_medication = mock_medication.copy()
    updated_medication["dosage"] = "20mg"
    updated_medication["notes"] = "Updated notes"
    setup_mock_db_update_item(mock_db_functions, updated_medication)
    
    # Make request
    update_data = {
        "dosage": "20mg",
        "notes": "Updated notes"
    }
    response = client.put(f"/api/medications/{test_medication_id}", json=update_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    update_medication_reporter.register_response(
        "test_update_medication",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["medication_id", "user_id", "name", "dosage", "frequency", "created_at", "updated_at"])
    assert response.json()["dosage"] == "20mg"
    assert response.json()["notes"] == "Updated notes"

def test_delete_medication(client: TestClient, auth_headers, mock_db_functions, mock_user, test_medication_id, response_capture):
    """Test deleting a medication."""
    # Register test
    delete_medication_reporter.register_test(
        "test_delete_medication",
        "Verify that an authenticated user can delete a medication."
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
    
    # Make request
    response = client.delete(f"/api/medications/{test_medication_id}", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    delete_medication_reporter.register_response(
        "test_delete_medication",
        response.status_code,
        response.text
    )
    
    # Assert response
    assert_status_code(response, 204)
    assert response.content == b""  # Empty response for successful deletion
