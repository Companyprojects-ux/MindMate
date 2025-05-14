# Postman Guide for Mental Health Support API

This guide provides instructions for testing the Mental Health Support API using Postman.

## Setup

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the collection (optional):
   - Download the Postman collection JSON file (if available)
   - In Postman, click "Import" and select the downloaded file
3. Set up environment variables:
   - Create a new environment in Postman
   - Add the following variables:
     - `base_url`: `http://localhost:8001`
     - `token`: (leave empty initially)

## Authentication

### Register a New User

- **Method**: POST
- **URL**: `{{base_url}}/api/auth/register`
- **Headers**:
  - Content-Type: application/json
- **Request Body** (raw JSON):
  ```json
  {
    "email": "user@example.com",
    "name": "Test User",
    "password": "password123"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "Test User",
    "created_at": 1620000000,
    "updated_at": 1620000000,
    "preferences": {},
    "notification_settings": {}
  }
  ```

### Login

- **Method**: POST
- **URL**: `{{base_url}}/api/auth/login`
- **Headers**:
  - Content-Type: application/json
- **Request Body** (raw JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **After successful login**:
  - Copy the `access_token` from the response
  - Set the `token` environment variable to this value

### Get Current User Profile

- **Method**: GET
- **URL**: `{{base_url}}/api/auth/me`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "Test User",
    "created_at": 1620000000,
    "updated_at": 1620000000,
    "preferences": {
      "theme": "dark",
      "notifications_enabled": true
    },
    "notification_settings": {
      "email": true,
      "push": false
    }
  }
  ```

## Medications

### List All Medications

- **Method**: GET
- **URL**: `{{base_url}}/api/medications`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  [
    {
      "medication_id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Aspirin",
      "dosage": "100mg",
      "frequency": "daily",
      "time_of_day": "morning",
      "specific_times": ["08:00"],
      "start_date": "2023-09-01",
      "end_date": null,
      "notes": "Take with food",
      "medication_type": "pill",
      "image_url": null,
      "created_at": 1620000000,
      "updated_at": 1620000000
    },
    {
      "medication_id": "550e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Vitamin D",
      "dosage": "1000IU",
      "frequency": "daily",
      "time_of_day": "morning",
      "specific_times": ["08:00"],
      "start_date": "2023-09-01",
      "end_date": null,
      "notes": null,
      "medication_type": "pill",
      "image_url": null,
      "created_at": 1620000000,
      "updated_at": 1620000000
    }
  ]
  ```

### Add a New Medication

- **Method**: POST
- **URL**: `{{base_url}}/api/medications`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Request Body** (raw JSON):
  ```json
  {
    "name": "Aspirin",
    "dosage": "100mg",
    "frequency": "daily",
    "time_of_day": "morning",
    "specific_times": ["08:00"],
    "start_date": "2023-09-01",
    "medication_type": "pill"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "medication_id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Aspirin",
    "dosage": "100mg",
    "frequency": "daily",
    "time_of_day": "morning",
    "specific_times": ["08:00"],
    "start_date": "2023-09-01",
    "end_date": null,
    "notes": null,
    "medication_type": "pill",
    "image_url": null,
    "created_at": 1620000000,
    "updated_at": 1620000000
  }
  ```

### Get Medication Details

- **Method**: GET
- **URL**: `{{base_url}}/api/medications/{medication_id}`
- **Headers**:
  - Authorization: Bearer {{token}}

### Update Medication

- **Method**: PUT
- **URL**: `{{base_url}}/api/medications/{medication_id}`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Body** (raw JSON):
  ```json
  {
    "name": "Aspirin",
    "dosage": "200mg",
    "frequency": "daily",
    "time_of_day": "morning",
    "specific_times": ["08:00"],
    "start_date": "2023-09-01",
    "medication_type": "pill"
  }
  ```

### Delete Medication

- **Method**: DELETE
- **URL**: `{{base_url}}/api/medications/{medication_id}`
- **Headers**:
  - Authorization: Bearer {{token}}

## Reminders

### List All Reminders

- **Method**: GET
- **URL**: `{{base_url}}/api/reminders`
- **Headers**:
  - Authorization: Bearer {{token}}

### Create a New Reminder

- **Method**: POST
- **URL**: `{{base_url}}/api/reminders`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Body** (raw JSON):
  ```json
  {
    "medication_id": "{medication_id}",
    "scheduled_time": "2023-09-01T08:00:00",
    "status": "pending"
  }
  ```

### Update Reminder Status

- **Method**: PUT
- **URL**: `{{base_url}}/api/reminders/{reminder_id}/status`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Body** (raw JSON):
  ```json
  {
    "status": "completed"
  }
  ```

## Mood Tracking

### List All Mood Entries

- **Method**: GET
- **URL**: `{{base_url}}/api/moods`
- **Headers**:
  - Authorization: Bearer {{token}}

### Create a New Mood Entry

- **Method**: POST
- **URL**: `{{base_url}}/api/moods`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Request Body** (raw JSON):
  ```json
  {
    "mood_rating": 8,
    "tags": ["happy", "energetic"],
    "notes": "Feeling great today!"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "entry_id": "550e8400-e29b-41d4-a716-446655440003",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "mood_rating": 8,
    "tags": ["happy", "energetic"],
    "notes": "Feeling great today!",
    "timestamp": "2023-09-01T10:00:00",
    "created_at": 1620000000,
    "updated_at": 1620000000
  }
  ```

### Get Mood Statistics

- **Method**: GET
- **URL**: `{{base_url}}/api/moods/stats`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  {
    "average_rating": 7.5,
    "highest_rating": 9,
    "lowest_rating": 4,
    "most_common_tags": [
      {"tag": "happy", "count": 5},
      {"tag": "energetic", "count": 3},
      {"tag": "tired", "count": 2}
    ],
    "mood_trend": [
      {"date": "2023-08-25", "average_rating": 6.5},
      {"date": "2023-08-26", "average_rating": 7.0},
      {"date": "2023-08-27", "average_rating": 8.0}
    ],
    "total_entries": 10
  }
  ```

## Journal

### List All Journal Entries

- **Method**: GET
- **URL**: `{{base_url}}/api/journal`
- **Headers**:
  - Authorization: Bearer {{token}}

### Create a New Journal Entry

- **Method**: POST
- **URL**: `{{base_url}}/api/journal`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Request Body** (raw JSON):
  ```json
  {
    "title": "My First Journal Entry",
    "content": "Today was a great day. I felt energetic and accomplished a lot of tasks.",
    "tags": ["productive", "happy"]
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "entry_id": "550e8400-e29b-41d4-a716-446655440004",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "My First Journal Entry",
    "content": "Today was a great day. I felt energetic and accomplished a lot of tasks.",
    "tags": ["productive", "happy"],
    "timestamp": "2023-09-01T20:00:00",
    "created_at": 1620000000,
    "updated_at": 1620000000
  }
  ```

### Search Journal Entries

- **Method**: GET
- **URL**: `{{base_url}}/api/journal/search?query=great`
- **Headers**:
  - Authorization: Bearer {{token}}

## AI Support

### Send a Message to the Chatbot

- **Method**: POST
- **URL**: `{{base_url}}/api/ai/chat`
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer {{token}}
- **Request Body** (raw JSON):
  ```json
  {
    "message": "How can I manage my anxiety?"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "response": "Anxiety can be challenging to manage, but there are several evidence-based strategies that might help. Deep breathing exercises, progressive muscle relaxation, and mindfulness meditation can be effective for immediate relief. Regular physical activity, adequate sleep, and limiting caffeine and alcohol can help reduce overall anxiety levels. Cognitive-behavioral techniques like identifying and challenging negative thought patterns can also be beneficial. If your anxiety is significantly affecting your daily life, consider speaking with a mental health professional who can provide personalized guidance and support."
  }
  ```

### Get Chat History

- **Method**: GET
- **URL**: `{{base_url}}/api/ai/chat/history`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  [
    {
      "message_id": "550e8400-e29b-41d4-a716-446655440005",
      "message": "How can I manage my anxiety?",
      "is_user": true,
      "timestamp": "2023-09-01T14:30:00"
    },
    {
      "message_id": "550e8400-e29b-41d4-a716-446655440006",
      "message": "Anxiety can be challenging to manage, but there are several evidence-based strategies that might help...",
      "is_user": false,
      "timestamp": "2023-09-01T14:30:05"
    },
    {
      "message_id": "550e8400-e29b-41d4-a716-446655440007",
      "message": "What about meditation techniques?",
      "is_user": true,
      "timestamp": "2023-09-01T14:31:00"
    },
    {
      "message_id": "550e8400-e29b-41d4-a716-446655440008",
      "message": "Meditation can be very effective for managing anxiety...",
      "is_user": false,
      "timestamp": "2023-09-01T14:31:05"
    }
  ]
  ```

### Get AI Suggestions

- **Method**: GET
- **URL**: `{{base_url}}/api/ai/suggestions`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  {
    "journal_prompt": "What is making you feel so good today?",
    "coping_tip": "Continue your positive habits.",
    "motivational_content": "Share your positive energy with others.",
    "medication_tip": "Remember to take your Aspirin as prescribed."
  }
  ```

### Submit Feedback on AI Suggestions

- **Method**: POST
- **URL**: `{{base_url}}/api/ai/feedback?feedback=This was helpful`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  {
    "message": "Feedback submitted successfully"
  }
  ```

### Get Visualization Data

- **Method**: GET
- **URL**: `{{base_url}}/api/ai/visualization_data?data_type=mood`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Query Parameters**:
  - `data_type`: Type of data to retrieve (mood, medication, journal)
- **Response** (200 OK) for `data_type=mood`:
  ```json
  [
    {
      "entry_id": "550e8400-e29b-41d4-a716-446655440003",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "mood_rating": 8,
      "tags": ["happy", "energetic"],
      "notes": "Feeling great today!",
      "timestamp": "2023-09-01T10:00:00",
      "created_at": 1620000000,
      "updated_at": 1620000000
    },
    {
      "entry_id": "550e8400-e29b-41d4-a716-446655440009",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "mood_rating": 6,
      "tags": ["neutral"],
      "notes": "Average day",
      "timestamp": "2023-08-31T10:00:00",
      "created_at": 1619913600,
      "updated_at": 1619913600
    }
  ]
  ```

### Get Personalized Recommendations

- **Method**: GET
- **URL**: `{{base_url}}/api/ai/recommendations`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  {
    "journal_prompts": [
      {
        "title": "Mood Reflection",
        "prompt": "How has your mood been today? What factors might be contributing to your current mood?"
      },
      {
        "title": "Gratitude",
        "prompt": "What are three things you're grateful for today?"
      }
    ],
    "coping_strategies": [
      {
        "title": "Physical Exercise",
        "description": "Do 10 minutes of physical activity."
      },
      {
        "title": "Social Connection",
        "description": "Reach out to a friend or family member."
      }
    ],
    "timestamp": "2023-05-12T04:02:13.416384",
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```

### Get Weekly Progress Report

- **Method**: GET
- **URL**: `{{base_url}}/api/ai/weekly-report`
- **Headers**:
  - Authorization: Bearer {{token}}
- **Response** (200 OK):
  ```json
  {
    "report": "# Weekly Mental Health Report\n\n## Summary\nThis week, your average mood rating was 7.2/10, which is a slight improvement from last week's 6.8/10. You completed 85% of your medication reminders, which is excellent! You also wrote 5 journal entries, focusing on themes of productivity and self-care.\n\n## Mood Patterns\nYour mood was highest on Wednesday (8/10) and lowest on Monday (5/10). There seems to be a pattern of lower mood in the mornings that improves throughout the day.\n\n## Medication Adherence\nYou've been consistent with your morning medications (95% adherence) but have occasionally missed your evening doses (75% adherence).\n\n## Recommendations for Next Week\n1. Consider setting an additional reminder for your evening medications\n2. Continue your journaling habit, which seems to correlate with improved mood\n3. The physical activities you mentioned in your journal entries appear to boost your mood - try to incorporate these regularly\n\nGreat job this week! Remember that consistency is key to mental health improvement."
  }
  ```

## Tips for Testing

1. **Authentication Flow**:
   - Register a new user
   - Login to get the token
   - Use the token for all subsequent requests

2. **Testing Dependencies**:
   - Create a medication before creating a reminder
   - Use valid IDs when referencing other resources

3. **Error Handling**:
   - Test with invalid data to see error responses
   - Test with missing authentication to verify security

4. **AI Features**:
   - Add some mood entries and journal entries before testing AI features
   - Try different types of questions with the chatbot
   - Check if recommendations change based on your mood entries
