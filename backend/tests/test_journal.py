"""
Tests for journal endpoints.
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
create_journal_reporter = TestReporter("/api/journal", "POST")
list_journal_reporter = TestReporter("/api/journal", "GET")
search_journal_reporter = TestReporter("/api/journal/search", "GET")
get_journal_reporter = TestReporter("/api/journal/{entry_id}", "GET")
update_journal_reporter = TestReporter("/api/journal/{entry_id}", "PUT")
delete_journal_reporter = TestReporter("/api/journal/{entry_id}", "DELETE")

def test_create_journal_entry(client: TestClient, auth_headers, mock_db_functions, mock_user, test_journal_data, test_journal_id, response_capture):
    """Test creating a journal entry."""
    # Register test
    create_journal_reporter.register_test(
        "test_create_journal_entry",
        "Verify that an authenticated user can create a journal entry."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_journal = {
        "entry_id": test_journal_id,
        "user_id": mock_user["user_id"],
        "title": test_journal_data["title"],
        "content": test_journal_data["content"],
        "tags": test_journal_data["tags"],
        "timestamp": "2023-05-01T12:00:00",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_create_item(mock_db_functions, mock_journal)
    
    # Make request
    response = client.post("/api/journal", json=test_journal_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    create_journal_reporter.register_response(
        "test_create_journal_entry",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 201)
    assert_json_response(response, ["entry_id", "user_id", "title", "content", "tags", "timestamp", "created_at", "updated_at"])
    assert response.json()["title"] == test_journal_data["title"]
    assert response.json()["content"] == test_journal_data["content"]
    assert response.json()["tags"] == test_journal_data["tags"]

def test_create_journal_entry_unauthenticated(client: TestClient, test_journal_data, response_capture):
    """Test creating a journal entry without authentication."""
    # Register test
    create_journal_reporter.register_test(
        "test_create_journal_entry_unauthenticated",
        "Verify that an unauthenticated user cannot create a journal entry."
    )
    
    # Make request
    response = client.post("/api/journal", json=test_journal_data)
    response = response_capture.capture(response)
    
    # Register response
    create_journal_reporter.register_response(
        "test_create_journal_entry_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_list_journal_entries(client: TestClient, auth_headers, mock_db_functions, mock_user, test_journal_id, response_capture):
    """Test listing journal entries."""
    # Register test
    list_journal_reporter.register_test(
        "test_list_journal_entries",
        "Verify that an authenticated user can list their journal entries."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_journals = [
        {
            "entry_id": test_journal_id,
            "user_id": mock_user["user_id"],
            "title": "Test Journal Entry",
            "content": "This is a test journal entry.",
            "tags": ["test", "journal"],
            "timestamp": "2023-05-01T12:00:00",
            "created_at": 1620000000,
            "updated_at": 1620000000
        },
        {
            "entry_id": "another-test-journal-id",
            "user_id": mock_user["user_id"],
            "title": "Another Test Journal Entry",
            "content": "This is another test journal entry.",
            "tags": ["test", "another"],
            "timestamp": "2023-05-02T12:00:00",
            "created_at": 1620086400,
            "updated_at": 1620086400
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_journals)
    
    # Make request
    response = client.get("/api/journal", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    list_journal_reporter.register_response(
        "test_list_journal_entries",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 2
    assert response.json()[0]["entry_id"] == test_journal_id
    assert response.json()[1]["entry_id"] == "another-test-journal-id"

def test_list_journal_entries_unauthenticated(client: TestClient, response_capture):
    """Test listing journal entries without authentication."""
    # Register test
    list_journal_reporter.register_test(
        "test_list_journal_entries_unauthenticated",
        "Verify that an unauthenticated user cannot list journal entries."
    )
    
    # Make request
    response = client.get("/api/journal")
    response = response_capture.capture(response)
    
    # Register response
    list_journal_reporter.register_response(
        "test_list_journal_entries_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_search_journal_entries(client: TestClient, auth_headers, mock_db_functions, mock_user, test_journal_id, response_capture):
    """Test searching journal entries."""
    # Register test
    search_journal_reporter.register_test(
        "test_search_journal_entries",
        "Verify that an authenticated user can search their journal entries."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_journals = [
        {
            "entry_id": test_journal_id,
            "user_id": mock_user["user_id"],
            "title": "Test Journal Entry",
            "content": "This is a test journal entry.",
            "tags": ["test", "journal"],
            "timestamp": "2023-05-01T12:00:00",
            "created_at": 1620000000,
            "updated_at": 1620000000
        }
    ]
    setup_mock_db_query_items(mock_db_functions, mock_journals)
    
    # Make request
    response = client.get("/api/journal/search?query=test", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    search_journal_reporter.register_response(
        "test_search_journal_entries",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_list_response(response)
    assert len(response.json()) == 1
    assert response.json()[0]["entry_id"] == test_journal_id

def test_search_journal_entries_unauthenticated(client: TestClient, response_capture):
    """Test searching journal entries without authentication."""
    # Register test
    search_journal_reporter.register_test(
        "test_search_journal_entries_unauthenticated",
        "Verify that an unauthenticated user cannot search journal entries."
    )
    
    # Make request
    response = client.get("/api/journal/search?query=test")
    response = response_capture.capture(response)
    
    # Register response
    search_journal_reporter.register_response(
        "test_search_journal_entries_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_get_journal_entry(client: TestClient, auth_headers, mock_db_functions, mock_user, test_journal_id, response_capture):
    """Test getting a journal entry by ID."""
    # Register test
    get_journal_reporter.register_test(
        "test_get_journal_entry",
        "Verify that an authenticated user can get a journal entry by ID."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_journal = {
        "entry_id": test_journal_id,
        "user_id": mock_user["user_id"],
        "title": "Test Journal Entry",
        "content": "This is a test journal entry.",
        "tags": ["test", "journal"],
        "timestamp": "2023-05-01T12:00:00",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_get_item(mock_db_functions, mock_journal)
    
    # Make request
    response = client.get(f"/api/journal/{test_journal_id}", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_journal_reporter.register_response(
        "test_get_journal_entry",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["entry_id", "user_id", "title", "content", "tags", "timestamp", "created_at", "updated_at"])
    assert response.json()["entry_id"] == test_journal_id

def test_get_journal_entry_not_found(client: TestClient, auth_headers, mock_db_functions, mock_user, response_capture):
    """Test getting a journal entry that doesn't exist."""
    # Register test
    get_journal_reporter.register_test(
        "test_get_journal_entry_not_found",
        "Verify that getting a non-existent journal entry returns a 404 error."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    setup_mock_db_get_item(mock_db_functions, None)  # Entry doesn't exist
    
    # Make request
    response = client.get("/api/journal/nonexistent-id", headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    get_journal_reporter.register_response(
        "test_get_journal_entry_not_found",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_not_found(response)

def test_get_journal_entry_unauthenticated(client: TestClient, test_journal_id, response_capture):
    """Test getting a journal entry without authentication."""
    # Register test
    get_journal_reporter.register_test(
        "test_get_journal_entry_unauthenticated",
        "Verify that an unauthenticated user cannot get a journal entry."
    )
    
    # Make request
    response = client.get(f"/api/journal/{test_journal_id}")
    response = response_capture.capture(response)
    
    # Register response
    get_journal_reporter.register_response(
        "test_get_journal_entry_unauthenticated",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_unauthorized(response)

def test_update_journal_entry(client: TestClient, auth_headers, mock_db_functions, mock_user, test_journal_id, response_capture):
    """Test updating a journal entry."""
    # Register test
    update_journal_reporter.register_test(
        "test_update_journal_entry",
        "Verify that an authenticated user can update a journal entry."
    )
    
    # Set up mocks
    setup_mock_db_get_user(mock_db_functions, mock_user)
    mock_journal = {
        "entry_id": test_journal_id,
        "user_id": mock_user["user_id"],
        "title": "Test Journal Entry",
        "content": "This is a test journal entry.",
        "tags": ["test", "journal"],
        "timestamp": "2023-05-01T12:00:00",
        "created_at": 1620000000,
        "updated_at": 1620000000
    }
    setup_mock_db_get_item(mock_db_functions, mock_journal)
    updated_journal = mock_journal.copy()
    updated_journal["title"] = "Updated Title"
    updated_journal["content"] = "Updated content"
    setup_mock_db_update_item(mock_db_functions, updated_journal)
    
    # Make request
    update_data = {
        "title": "Updated Title",
        "content": "Updated content"
    }
    response = client.put(f"/api/journal/{test_journal_id}", json=update_data, headers=auth_headers)
    response = response_capture.capture(response)
    
    # Register response
    update_journal_reporter.register_response(
        "test_update_journal_entry",
        response.status_code,
        response.json()
    )
    
    # Assert response
    assert_status_code(response, 200)
    assert_json_response(response, ["entry_id", "user_id", "title", "content", "tags", "timestamp", "created_at", "updated_at"])
    assert response.json()["title"] == "Updated Title"
    assert response.json()["content"] == "Updated content"
