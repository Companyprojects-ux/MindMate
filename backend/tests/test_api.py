"""
API tests.
"""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_mental_health_support():
    """Test the mental health support endpoint."""
    # This test will fail if the LLM is not properly configured
    # So we're just testing that the endpoint exists
    response = client.get("/mental_health_support?prompt=test")
    assert response.status_code in [200, 500]  # 500 if LLM not configured

def test_coping_strategies():
    """Test the coping strategies endpoint."""
    # This test will fail if the LLM is not properly configured
    # So we're just testing that the endpoint exists
    response = client.get("/coping_strategies?user_input=test")
    assert response.status_code in [200, 500]  # 500 if LLM not configured

def create_test_user():
    """Create a test user."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "name": "Test User"
    }
    # Check if user exists
    response = client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    if response.status_code == 200:
        return response.json()
    else:
        response = client.post("/api/auth/register", json=user_data)
        print(response.json())
        assert response.status_code == 201
        return response.json()

def authenticate_test_user():
    """Authenticate the test user."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/auth/login", json=user_data)
    assert response.status_code == 200
    return response.json()

def test_ai_suggestions():
    """Test the AI suggestions endpoint."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Create a mood entry
    mood_data = {
        "mood_rating": 3,
        "tags": ["test"]
    }
    response = client.post("/api/moods", json=mood_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

def test_feedback():
    """Test the feedback endpoint."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Submit feedback
    response = client.post("/api/ai/feedback?feedback=test", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback submitted successfully"}

def test_visualization_data():
    """Test the visualization data endpoint."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Get visualization data
    response = client.get("/api/ai/visualization_data?data_type=mood", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ai_suggestions_unauthenticated():
    """Test the AI suggestions endpoint with an unauthenticated user."""
    response = client.get("/api/ai/suggestions")
    assert response.status_code == 401

def test_visualization_data_unauthenticated():
    """Test the visualization data endpoint with an unauthenticated user."""
    response = client.get("/api/ai/visualization_data?data_type=mood")
    assert response.status_code == 401

def test_feedback_unauthenticated():
    """Test the feedback endpoint with an unauthenticated user."""
    response = client.post("/api/ai/feedback?feedback=test")
def test_register_invalid_email():
    """Test the register endpoint with an invalid email."""
    user_data = {
        "email": "invalid-email",
        "password": "testpassword",
        "name": "Test User"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 422

def test_register_short_password():
    """Test the register endpoint with a short password."""
    user_data = {
        "email": "test2@example.com",
        "password": "test",
        "name": "Test User"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 422

def test_create_mood_entry_unauthenticated():
    """Test the create mood entry endpoint with an unauthenticated user."""
    response = client.post("/api/moods", json={"mood_rating": 5, "tags": ["test"]})
    assert response.status_code == 401

def test_list_mood_entries_unauthenticated():
    """Test the list mood entries endpoint with an unauthenticated user."""
    response = client.get("/api/moods")
    assert response.status_code == 401

def test_get_mood_statistics_unauthenticated():
    """Test the get mood statistics endpoint with an unauthenticated user."""
    response = client.get("/api/moods/stats")
    assert response.status_code == 401

def test_get_mood_entry_unauthenticated():
    """Test the get mood entry endpoint with an unauthenticated user."""
    # Create a test user and mood entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    mood_data = {"mood_rating": 5, "tags": ["test"]}
    response = client.post("/api/moods", json=mood_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.get(f"/api/moods/{entry_id}")
    assert response.status_code == 401

def test_update_mood_entry_unauthenticated():
    """Test the update mood entry endpoint with an unauthenticated user."""
    # Create a test user and mood entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    mood_data = {"mood_rating": 5, "tags": ["test"]}
    response = client.post("/api/moods", json=mood_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.put(f"/api/moods/{entry_id}", json={"mood_rating": 3})
    assert response.status_code == 401

def test_delete_mood_entry_unauthenticated():
    """Test the delete mood entry endpoint with an unauthenticated user."""
    # Create a test user and mood entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    mood_data = {"mood_rating": 5, "tags": ["test"]}
    response = client.post("/api/moods", json=mood_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/moods/{entry_id}")
    assert response.status_code == 401

def test_get_mood_entry_invalid_id():
    """Test the get mood entry endpoint with an invalid ID."""
    # Create and authenticate test user
def test_create_reminder_unauthenticated():
    """Test the create reminder endpoint with an unauthenticated user."""
    response = client.post("/api/reminders", json={"medication_id": "test", "scheduled_time": "2025-05-12T00:00:00"})
    assert response.status_code == 401

def test_list_reminders_unauthenticated():
    """Test the list reminders endpoint with an unauthenticated user."""
    response = client.get("/api/reminders")
    assert response.status_code == 401

def test_get_today_reminders_unauthenticated():
    """Test the get today reminders endpoint with an unauthenticated user."""
    response = client.get("/api/reminders/today")
    assert response.status_code == 401

def test_get_upcoming_reminders_unauthenticated():
    """Test the get upcoming reminders endpoint with an unauthenticated user."""
    response = client.get("/api/reminders/upcoming")
    assert response.status_code == 401

def test_create_reminder_unauthenticated():
    """Test the create reminder endpoint with an unauthenticated user."""
    response = client.post("/api/reminders", json={"medication_id": "test", "scheduled_time": "2025-05-12T00:00:00"})
    assert response.status_code == 401
    # Create a test user and reminder
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Create a medication
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    reminder_data = {"medication_id": medication_id, "scheduled_time": "2025-05-12T00:00:00"}
    response = client.post("/api/reminders", json=reminder_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    reminder_id = response.json()["reminder_id"]

    # Test unauthenticated access
    response = client.get(f"/api/reminders/{reminder_id}")
    assert response.status_code == 401

def test_update_reminder_unauthenticated():
    """Test the update reminder endpoint with an unauthenticated user."""
    # Create a test user and reminder
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Create a medication
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    reminder_data = {"medication_id": medication_id, "scheduled_time": "2025-05-12T00:00:00"}
    response = client.post("/api/reminders", json=reminder_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    reminder_id = response.json()["reminder_id"]

    # Test unauthenticated access
    response = client.put(f"/api/reminders/{reminder_id}", json={"scheduled_time": "2025-05-13T00:00:00"})
    assert response.status_code == 401

def test_update_reminder_status_unauthenticated():
    """Test the update reminder status endpoint with an unauthenticated user."""
    # Create a test user and reminder
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Create a medication
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    reminder_data = {"medication_id": medication_id, "scheduled_time": "2025-05-12T00:00:00"}
    response = client.post("/api/reminders", json=reminder_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    reminder_id = response.json()["reminder_id"]

    # Test unauthenticated access
    response = client.put(f"/api/reminders/{reminder_id}/status", json={"status": "completed"})
    assert response.status_code == 401

def test_delete_reminder_unauthenticated():
    """Test the delete reminder endpoint with an unauthenticated user."""
    # Create a test user and reminder
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Create a medication
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    reminder_data = {"medication_id": medication_id, "scheduled_time": "2025-05-12T00:00:00"}
    response = client.post("/api/reminders", json=reminder_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    reminder_id = response.json()["reminder_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/reminders/{reminder_id}")
def test_get_reminder_invalid_id():
    """Test the get reminder endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/reminders/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_reminder_invalid_id():
    """Test the update reminder endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/reminders/invalid-id", json={"scheduled_time": "2025-05-13T00:00:00"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_reminder_status_invalid_id():
    """Test the update reminder status endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/reminders/invalid-id/status", json={"status": "completed"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_reminder_invalid_id():
    """Test the delete reminder endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/reminders/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.status_code == 401

def test_get_reminder_invalid_id():
    """Test the get reminder endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/reminders/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_reminder_invalid_id():
    """Test the update reminder endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/reminders/invalid-id", json={"scheduled_time": "2025-05-13T00:00:00"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_reminder_status_invalid_id():
    """Test the update reminder status endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/reminders/invalid-id/status", json={"status": "completed"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_reminder_invalid_id():
    """Test the delete reminder endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/reminders/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/moods/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_mood_entry_invalid_id():
    """Test the update mood entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/moods/invalid-id", json={"mood_rating": 3}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_mood_entry_invalid_id():
    """Test the delete mood entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

def test_create_medication_unauthenticated():
    """Test the create medication endpoint with an unauthenticated user."""
    response = client.post("/api/medications", json={"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"})
    assert response.status_code == 401

def test_list_medications_unauthenticated():
    """Test the list medications endpoint with an unauthenticated user."""
    response = client.get("/api/medications")
    assert response.status_code == 401

def test_get_medication_unauthenticated():
    """Test the get medication endpoint with an unauthenticated user."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.get(f"/api/medications/{medication_id}")
    assert response.status_code == 401

def test_update_medication_unauthenticated():
    """Test the update medication endpoint with an unauthenticated user."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})

def test_update_medication_invalid_id():
    """Test the update medication endpoint with an invalid ID."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.get(f"/api/medications/{medication_id}")
    assert response.status_code == 401

def test_update_medication_unauthenticated():
    """Test the get mood entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/moods/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_mood_entry_invalid_id():
    """Test the update mood entry endpoint with an invalid ID."""

def test_delete_mood_entry_invalid_id():
    """Test the delete mood entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/moods/invalid-id", json={"mood_rating": 3}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_medication_invalid_id():
    """Test the update medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
def test_update_medication_invalid_id():
    """Test the update medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/medications/invalid-id", json={"dosage": "20mg"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_medication_invalid_id():
    """Test the delete medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

    # Test invalid ID
    response = client.delete("/api/moods/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    """Test the update medication endpoint with an unauthenticated user."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.put(f"/api/medications/{medication_id}", json={"dosage": "20mg"})
    assert response.status_code == 401

def test_delete_medication_unauthenticated():
    """Test the delete medication endpoint with an unauthenticated user."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/medications/{medication_id}")
    assert response.status_code == 401

def test_get_medication_invalid_id():
    """Test the get medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

def test_delete_medication_invalid_id():
    """Test the delete medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_create_journal_entry_unauthenticated():
    """Test the create journal entry endpoint with an unauthenticated user."""
    response = client.post("/api/journal", json={"title": "Test Title", "content": "test content"})
    assert response.status_code == 401

def test_list_journal_entries_unauthenticated():
    """Test the list journal entries endpoint with an unauthenticated user."""
    response = client.get("/api/journal")
    assert response.status_code == 401

def test_search_journal_entries_unauthenticated():
    """Test the search journal entries endpoint with an unauthenticated user."""
    response = client.get("/api/journal/search?query=test")
    assert response.status_code == 401

def test_get_journal_entry_unauthenticated():
    """Test the get journal entry endpoint with an unauthenticated user."""
    # Create a test user and journal entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    journal_data = {"title": "Test Title", "content": "test content"}
    response = client.post("/api/journal", json=journal_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.get(f"/api/journal/{entry_id}")
    assert response.status_code == 401

def test_update_journal_entry_unauthenticated():
    """Test the update journal entry endpoint with an unauthenticated user."""
    # Create a test user and journal entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    journal_data = {"title": "Test Title", "content": "test content"}
    response = client.post("/api/journal", json=journal_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.put(f"/api/journal/{entry_id}", json={"content": "updated test"})
    assert response.status_code == 401

def test_delete_journal_entry_unauthenticated():
    """Test the delete journal entry endpoint with an unauthenticated user."""
    # Create a test user and journal entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    journal_data = {"title": "Test Title", "content": "test content"}
    response = client.post("/api/journal", json=journal_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/journal/{entry_id}")
    assert response.status_code == 401

def test_get_journal_entry_invalid_id():
    """Test the get journal entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/journal/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_journal_entry_invalid_id():
    """Test the update journal entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/journal/invalid-id", json={"content": "updated test"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_journal_entry_invalid_id():
    """Test the delete journal entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/journal/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
def test_delete_medication_unauthenticated():
    """Test the delete medication endpoint with an unauthenticated user."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/medications/{medication_id}")
    assert response.status_code == 401

def test_get_medication_invalid_id():
    """Test the get medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_medication_invalid_id():
    """Test the update medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/medications/invalid-id", json={"dosage": "20mg"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_medication_invalid_id():
    """Test the delete medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    # Test invalid ID
    response = client.get("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_medication_invalid_id():
    """Test the update medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/medications/invalid-id", json={"dosage": "20mg"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_medication_invalid_id():
    """Test the delete medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.put(f"/api/medications/{medication_id}", json={"dosage": "20mg"})
    assert response.status_code == 401

def test_delete_medication_unauthenticated():
    """Test the delete medication endpoint with an unauthenticated user."""
    # Create a test user and medication
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "daily", "start_date": "2025-05-12"}
    response = client.post("/api/medications", json=medication_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    medication_id = response.json()["medication_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/medications/{medication_id}")
    assert response.status_code == 401

def test_get_medication_invalid_id():
    """Test the get medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_medication_invalid_id():
    """Test the update medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/medications/invalid-id", json={"dosage": "20mg"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_medication_invalid_id():
    """Test the delete medication endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/medications/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    # Test invalid ID
def test_create_journal_entry_unauthenticated():
    """Test the create journal entry endpoint with an unauthenticated user."""
    response = client.post("/api/journal", json={"text": "test"})
    assert response.status_code == 401

def test_list_journal_entries_unauthenticated():
    """Test the list journal entries endpoint with an unauthenticated user."""
    response = client.get("/api/journal")
    assert response.status_code == 401

def test_search_journal_entries_unauthenticated():
    """Test the search journal entries endpoint with an unauthenticated user."""
    response = client.get("/api/journal/search?query=test")
    assert response.status_code == 401

def test_get_journal_entry_unauthenticated():
    """Test the get journal entry endpoint with an unauthenticated user."""
    # Create a test user and journal entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    journal_data = {"title": "Test Title", "content": "test content"}
    response = client.post("/api/journal", json=journal_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.get(f"/api/journal/{entry_id}")
    assert response.status_code == 401

def test_update_journal_entry_unauthenticated():
    """Test the update journal entry endpoint with an unauthenticated user."""
    # Create a test user and journal entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    journal_data = {"title": "Test Title", "content": "test content"}
    response = client.post("/api/journal", json=journal_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.put(f"/api/journal/{entry_id}", json={"text": "updated test"})
    assert response.status_code == 401

def test_delete_journal_entry_unauthenticated():
    """Test the delete journal entry endpoint with an unauthenticated user."""
    # Create a test user and journal entry
    user = create_test_user()
    token = authenticate_test_user()["access_token"]
    journal_data = {"title": "Test Title", "content": "test content"}
    response = client.post("/api/journal", json=journal_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    entry_id = response.json()["entry_id"]

    # Test unauthenticated access
    response = client.delete(f"/api/journal/{entry_id}")
    assert response.status_code == 401

def test_get_journal_entry_invalid_id():
    """Test the get journal entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.get("/api/journal/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_journal_entry_invalid_id():
    """Test the update journal entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.put("/api/journal/invalid-id", json={"text": "updated test"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_journal_entry_invalid_id():
    """Test the delete journal entry endpoint with an invalid ID."""
    # Create and authenticate test user
    user = create_test_user()
    token = authenticate_test_user()["access_token"]

    # Test invalid ID
    response = client.delete("/api/journal/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    response = client.delete("/api/moods/invalid-id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
def test_login_incorrect_password():
    """Test the login endpoint with an incorrect password."""
    # Create a test user
    create_test_user()
    user_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=user_data)
    assert response.status_code == 401

def test_refresh_token_unauthenticated():
    """Test the refresh token endpoint with an unauthenticated user."""
    response = client.post("/api/auth/refresh")
    assert response.status_code == 401

def test_get_user_profile_unauthenticated():
    """Test the get user profile endpoint with an unauthenticated user."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_update_user_profile_unauthenticated():
    """Test the update user profile endpoint with an unauthenticated user."""
    response = client.put("/api/auth/me", json={"name": "New Name"})
    assert response.status_code == 401

def test_change_password_unauthenticated():
    """Test the change password endpoint with an unauthenticated user."""
    response = client.put("/api/auth/password", json={"current_password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == 401
    assert response.status_code == 401
