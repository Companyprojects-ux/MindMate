"""
Tests for mood tracking endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

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
create_mood_reporter = TestReporter("/api/moods", "POST")
list_moods_reporter = TestReporter("/api/moods", "GET")
get_mood_reporter = TestReporter("/api/moods/{entry_id}", "GET")
update_mood_reporter = TestReporter("/api/moods/{entry_id}", "PUT")
delete_mood_reporter = TestReporter("/api/moods/{entry_id}", "DELETE")
stats_reporter = TestReporter("/api/moods/stats", "GET")

def test_create_mood_entry(client: TestClient, auth_headers, mock_db_functions, mock_user, test_mood_data, test_mood_id, response_capture):
    """Test creating a mood entry."""
    # Register test
    create_mood_reporter.register_test(
        "test_create_mood_entry",
        "Verify that an authenticated user can create a mood entry."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_mood = {
        "entry_id": test_mood_id,
        "user_id": mock_user["user_id"],
        "mood_rating": test_mood_data["mood_rating"],
        "tags": test_mood_data["tags"],
        "notes": test_mood_data["notes"],
        "timestamp": "2023-05-01T12:00:00",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_create_item(mock_db_functions, mock_mood)
    
    # Make request
    response = client.post("/api/moods", json=test_mood_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    create_mood_reporter.register_response(
        "test_create_mood_entry",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 201)
    assert_json_response(response, ["entry_id", "user_id", "mood_rating", "tags", "notes", "timestamp", "created_at", "updated_at"])
    assert response.json()["mood_rating"] == test_mood_data["mood_rating"]
    assert response.json()["tags"] == test_mood_data["tags"]
    assert response.json()["notes"] == test_mood_data["notes"]

def test_create_mood_entry_unauthenticated(client: TestClient, test_mood_data, response_capture):
    """Test creating a mood entry without authentication."""
    # Register test
    create_mood_reporter.register_test(
        "test_create_mood_entry_unauthenticated",
        "Verify that an unauthenticated user cannot create a mood entry."
    )
    
    # Make request
    response = client.post("/api/moods", json=test_mood_data)
    response = response_capture.capture(response)
    
    # Register response
    create_mood_reporter.register_response(
        "test_create_mood_entry_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_create_mood_entry_invalid_rating(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test creating a mood entry with an invalid rating."""
    # Register test
    create_mood_reporter.register_test(
        "test_create_mood_entry_invalid_rating",
        "Verify that creating a mood entry fails when the rating is invalid."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    
    # Make request
    invalid_mood_data = {
        "mood_rating": 11,  # Invalid: should be 1-10
        "tags": ["test"],
        "notes": "Test notes"
    }
    response = client.post("/api/moods", json=invalid_mood_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    create_mood_reporter.register_response(
        "test_create_mood_entry_invalid_rating",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_validation_error(response, "mood_rating")

def test_list_mood_entries(client: TestClient, auth_headers, mock_db_functions, mock_user, test_mood_id, response_capture):
    """Test listing mood entries."""
    # Register test
    list_moods_reporter.register_test(
        "test_list_mood_entries",
        "Verify that an authenticated user can list their mood entries."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_moods = [
        {
            "entry_id": test_mood_id,
            "user_id": mock_user["user_id"],
            "mood_rating": 7,
            "tags": ["happy", "productive"],
            "notes": "Had a great day!",
            "timestamp": "2023-05-01T12:00:00",
            "created_at": 1620000000,
            "updated_at": 1620000000
        },
        {
            "entry_id": "another-test-mood-id",
            "user_id": mock_user["user_id"],
            "mood_rating": 5,
            "tags": ["neutral"],
            "notes": "Average day",
            "timestamp": "2023-05-02T12:00:00",
            "created_at": 1620086400,
            "updated_at": 1620086400
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_moods)
    
    # Make request
    response = client.get("/api/moods", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    list_moods_reporter.register_response(
        "test_list_mood_entries",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 2
    assert response.json()[0]["entry_id"] == test_mood_id
    assert response.json()[1]["entry_id"] == "another-test-mood-id"

def test_list_mood_entries_unauthenticated(client: TestClient, response_capture):
    """Test listing mood entries without authentication."""
    # Register test
    list_moods_reporter.register_test(
        "test_list_mood_entries_unauthenticated",
        "Verify that an unauthenticated user cannot list mood entries."
    )
    
    # Make request
    response = client.get("/api/moods")
    response = response_capture.capture(response)
    
    # Register response
    list_moods_reporter.register_response(
        "test_list_mood_entries_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_mood_entry(client: TestClient, auth_headers, mock_db_functions, mock_user, test_mood_id, response_capture):
    """Test getting a mood entry by ID."""
    # Register test
    get_mood_reporter.register_test(
        "test_get_mood_entry",
        "Verify that an authenticated user can get a mood entry by ID."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_mood = {
        "entry_id": test_mood_id,
        "user_id": mock_user["user_id"],
        "mood_rating": 7,
        "tags": ["happy", "productive"],
        "notes": "Had a great day!",
        "timestamp": "2023-05-01T12:00:00",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_get_item(mock_db_functions, mock_mood)
    
    # Make request
    response = client.get(f"/api/moods/{test_mood_id}", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_mood_reporter.register_response(
        "test_get_mood_entry",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["entry_id", "user_id", "mood_rating", "tags", "notes", "timestamp", "created_at", "updated_at"])
    assert response.json()["entry_id"] == test_mood_id

def test_get_mood_entry_not_found(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test getting a mood entry that doesn't exist."""
    # Register test
    get_mood_reporter.register_test(
        "test_get_mood_entry_not_found",
        "Verify that getting a non-existent mood entry returns a 404 error."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_db_get_item(mock_db_functions, None)  # Entry doesn't exist
    
    # Make request
    response = client.get("/api/moods/nonexistent-id", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_mood_reporter.register_response(
        "test_get_mood_entry_not_found",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_not_found(response)

def test_get_mood_entry_unauthenticated(client: TestClient, test_mood_id, response_capture):
    """Test getting a mood entry without authentication."""
    # Register test
    get_mood_reporter.register_test(
        "test_get_mood_entry_unauthenticated",
        "Verify that an unauthenticated user cannot get a mood entry."
    )
    
    # Make request
    response = client.get(f"/api/moods/{test_mood_id}")
    response = response_capture.capture(response)
    
    # Register response
    get_mood_reporter.register_response(
        "test_get_mood_entry_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_update_mood_entry(client: TestClient, auth_headers, mock_db_functions, mock_user, test_mood_id, response_capture):
    """Test updating a mood entry."""
    # Register test
    update_mood_reporter.register_test(
        "test_update_mood_entry",
        "Verify that an authenticated user can update a mood entry."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_mood = {
        "entry_id": test_mood_id,
        "user_id": mock_user["user_id"],
        "mood_rating": 7,
        "tags": ["happy", "productive"],
        "notes": "Had a great day!",
        "timestamp": "2023-05-01T12:00:00",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_get_item(mock_db_functions, mock_mood)
    updated_mood = mock_mood.copy()
    updated_mood["mood_rating"] = 8
    updated_mood["notes"] = "Updated notes"
    setup_mock_db_update_item(mock_db_functions, updated_mood)
    
    # Make request
    update_data = {
        "mood_rating": 8,
        "notes": "Updated notes"
    }
    response = client.put(f"/api/moods/{test_mood_id}", json=update_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    update_mood_reporter.register_response(
        "test_update_mood_entry",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["entry_id", "user_id", "mood_rating", "tags", "notes", "timestamp", "created_at", "updated_at"])
    assert response.json()["mood_rating"] == 8
    assert response.json()["notes"] == "Updated notes"

def test_update_mood_entry_not_found(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test updating a mood entry that doesn't exist."""
    # Register test
    update_mood_reporter.register_test(
        "test_update_mood_entry_not_found",
        "Verify that updating a non-existent mood entry returns a 404 error."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_db_get_item(mock_db_functions, None)  # Entry doesn't exist
    
    # Make request
    update_data = {
        "mood_rating": 8,
        "notes": "Updated notes"
    }
    response = client.put("/api/moods/nonexistent-id", json=update_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    update_mood_reporter.register_response(
        "test_update_mood_entry_not_found",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_not_found(response)

def test_update_mood_entry_unauthenticated(client: TestClient, test_mood_id, response_capture):
    """Test updating a mood entry without authentication."""
    # Register test
    update_mood_reporter.register_test(
        "test_update_mood_entry_unauthenticated",
        "Verify that an unauthenticated user cannot update a mood entry."
    )
    
    # Make request
    update_data = {
        "mood_rating": 8,
        "notes": "Updated notes"
    }
    response = client.put(f"/api/moods/{test_mood_id}", json=update_data)
    response = response_capture.capture(response)
    
    # Register response
    update_mood_reporter.register_response(
        "test_update_mood_entry_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)
