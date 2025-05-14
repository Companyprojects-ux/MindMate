# API Testing Documentation

This directory contains comprehensive tests for the MindMate API endpoints. The tests are organized by functionality and cover all API endpoints with both positive and negative test cases.

## Test Structure

The tests are organized into the following files:

- `conftest.py` - Common test fixtures and utilities
- `utils.py` - Test utility functions
- `report.py` - Test reporting utilities
- `test_health.py` - Tests for health check endpoint
- `test_auth.py` - Tests for authentication endpoints
- `test_medications.py` - Tests for medication endpoints
- `test_reminders.py` - Tests for reminder endpoints
- `test_moods.py` - Tests for mood tracking endpoints
- `test_journal.py` - Tests for journal endpoints
- `test_ai.py` - Tests for AI support endpoints

## Test Coverage

For each endpoint, the tests cover:

- **Positive test cases** - Testing with valid inputs
- **Negative test cases** - Testing with invalid inputs
- **Authentication tests** - Verifying protected endpoints
- **Authorization tests** - Verifying user access control
- **Edge cases** - Testing boundary conditions

## Running the Tests

To run all tests:

```bash
pytest
```

To run tests for a specific module:

```bash
pytest backend/tests/test_auth.py
```

To run tests with a specific marker:

```bash
pytest -m auth
```

## Test Reports

Test reports are generated automatically after test execution and saved to the `reports` directory. The reports include:

- Test summary (passed, failed, skipped)
- Detailed test results
- API response logs
- Endpoint coverage information

## Test Fixtures

The tests use the following fixtures:

- `client` - Test client for making HTTP requests
- `test_user_data` - Test user data
- `mock_user` - Mock user for authentication
- `auth_token` - Authentication token for the test user
- `auth_headers` - Authentication headers for the test user
- `mock_db_functions` - Mock database functions
- `mock_ai_service` - Mock AI service functions
- Various test data fixtures (mood, journal, medication, reminder)

## Mocking

The tests use mocking to avoid making actual database calls or API calls to external services. This makes the tests faster, more reliable, and independent of external dependencies.

## Response Capture

All API responses are captured and logged for debugging and reporting purposes. The `response_capture` fixture is used to capture responses.

## Test Documentation

Each test has a clear docstring explaining what it's testing. The test names are also descriptive to make it clear what's being tested.

## Test Reporting

The test reporting utilities in `report.py` are used to generate detailed reports about the test execution. The reports include information about test coverage, test results, and API responses.

## Continuous Integration

These tests can be run in a CI/CD pipeline to ensure that the API is working correctly before deployment. The tests are designed to be fast and reliable, making them suitable for CI/CD.

## Future Improvements

- Add more edge cases and negative test cases
- Add performance tests
- Add load tests
- Add security tests
- Add more detailed reporting
