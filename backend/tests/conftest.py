"""
Test fixtures and utilities for API testing.
"""
import pytest
import json
import logging
from typing import Dict, Any, Generator, List
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.core.security import create_access_token
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_log.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api_tests")

# Test client
@pytest.fixture
def client() -> TestClient:
    """Create a test client for the API."""
    return TestClient(app)

# Test user data
@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """Return test user data."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

@pytest.fixture
def test_user_2_data() -> Dict[str, Any]:
    """Return test user data for a second user."""
    return {
        "email": "test2@example.com",
        "password": "testpassword123",
        "name": "Test User 2"
    }

# Mock user for authentication
@pytest.fixture
def mock_user() -> Dict[str, Any]:
    """Return a mock user for authentication."""
    return {
        "user_id": "test-user-id",
        "email": "test@example.com",
        "name": "Test User",
        "created_at": 1620000000,
        "updated_at": 1620000000,
        "preferences": {},
        "notification_settings": {}
    }

@pytest.fixture
def mock_user_2() -> Dict[str, Any]:
    """Return a mock user for authentication."""
    return {
        "user_id": "test-user-id-2",
        "email": "test2@example.com",
        "name": "Test User 2",
        "created_at": 1620000000,
        "updated_at": 1620000000,
        "preferences": {},
        "notification_settings": {}
    }

# Authentication token
@pytest.fixture
def auth_token(mock_user) -> str:
    """Create an authentication token for the test user."""
    return create_access_token(data={"sub": mock_user["user_id"]})

@pytest.fixture
def auth_token_2(mock_user_2) -> str:
    """Create an authentication token for the second test user."""
    return create_access_token(data={"sub": mock_user_2["user_id"]})

@pytest.fixture
def auth_headers(auth_token) -> Dict[str, str]:
    """Return authentication headers for the test user."""
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def auth_headers_2(auth_token_2) -> Dict[str, str]:
    """Return authentication headers for the second test user."""
    return {"Authorization": f"Bearer {auth_token_2}"}

# Mock database functions
@pytest.fixture
def mock_db_functions():
    """Mock database functions."""
    with patch("backend.db.dynamodb.get_user_by_id") as mock_get_user, \
         patch("backend.db.dynamodb.get_user_by_email") as mock_get_user_by_email, \
         patch("backend.db.dynamodb.create_user") as mock_create_user, \
         patch("backend.db.dynamodb.create_item") as mock_create_item, \
         patch("backend.db.dynamodb.get_item") as mock_get_item, \
         patch("backend.db.dynamodb.update_item") as mock_update_item, \
         patch("backend.db.dynamodb.delete_item") as mock_delete_item, \
         patch("backend.db.dynamodb.query_items") as mock_query_items:
        
        yield {
            "get_user_by_id": mock_get_user,
            "get_user_by_email": mock_get_user_by_email,
            "create_user": mock_create_user,
            "create_item": mock_create_item,
            "get_item": mock_get_item,
            "update_item": mock_update_item,
            "delete_item": mock_delete_item,
            "query_items": mock_query_items
        }

# Mock AI service functions
@pytest.fixture
def mock_ai_service():
    """Mock AI service functions."""
    with patch("backend.services.ai_service.generate_chatbot_response") as mock_chat, \
         patch("backend.services.ai_service.generate_ai_suggestions") as mock_suggestions, \
         patch("backend.services.ai_service.get_visualization_data") as mock_viz_data, \
         patch("backend.services.ai_service.submit_feedback") as mock_feedback, \
         patch("backend.services.ai_service.generate_weekly_report") as mock_report:
        
        yield {
            "generate_chatbot_response": mock_chat,
            "generate_ai_suggestions": mock_suggestions,
            "get_visualization_data": mock_viz_data,
            "submit_feedback": mock_feedback,
            "generate_weekly_report": mock_report
        }

# Test data fixtures
@pytest.fixture
def test_mood_data() -> Dict[str, Any]:
    """Return test mood data."""
    return {
        "mood_rating": 7,
        "tags": ["happy", "productive"],
        "notes": "Had a great day!"
    }

@pytest.fixture
def test_journal_data() -> Dict[str, Any]:
    """Return test journal data."""
    return {
        "title": "Test Journal Entry",
        "content": "This is a test journal entry.",
        "tags": ["test", "journal"]
    }

@pytest.fixture
def test_medication_data() -> Dict[str, Any]:
    """Return test medication data."""
    return {
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "daily",
        "time_of_day": "morning",
        "start_date": "2023-05-01",
        "notes": "Take with food"
    }

@pytest.fixture
def test_reminder_data(test_medication_id) -> Dict[str, Any]:
    """Return test reminder data."""
    return {
        "medication_id": test_medication_id,
        "scheduled_time": "2023-05-01T08:00:00",
        "notes": "Take with breakfast"
    }

@pytest.fixture
def test_medication_id() -> str:
    """Return a test medication ID."""
    return "test-medication-id"

@pytest.fixture
def test_reminder_id() -> str:
    """Return a test reminder ID."""
    return "test-reminder-id"

@pytest.fixture
def test_mood_id() -> str:
    """Return a test mood entry ID."""
    return "test-mood-id"

@pytest.fixture
def test_journal_id() -> str:
    """Return a test journal entry ID."""
    return "test-journal-id"

# Test response logging
@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test information before and after each test."""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    yield
    logger.info(f"Completed test: {test_name}")

# Test response capture
class ResponseCapture:
    """Capture and log API responses."""
    
    def __init__(self):
        self.responses = []
    
    def capture(self, response):
        """Capture and log an API response."""
        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": self._get_response_body(response)
        }
        self.responses.append(response_data)
        logger.info(f"Response captured: {json.dumps(response_data, indent=2)}")
        return response
    
    def _get_response_body(self, response):
        """Get the response body as a dict or string."""
        try:
            return response.json()
        except:
            return response.text
    
    def get_responses(self):
        """Get all captured responses."""
        return self.responses
    
    def clear(self):
        """Clear all captured responses."""
        self.responses = []

@pytest.fixture
def response_capture():
    """Return a response capture instance."""
    return ResponseCapture()
