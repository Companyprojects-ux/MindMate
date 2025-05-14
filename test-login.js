// Simple fetch-based test for the login API using global fetch
async function testLogin() {
  const API_URL = 'http://localhost:8001/api/auth/login';

  // Replace with valid credentials
  const credentials = {
    email: 'test@example.com',
    password: 'password123'
  };

  console.log('Testing login API with credentials:', credentials);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    console.log('Response status:', response.status);

    try {
      const data = await response.json();
      console.log('Response data:', data);

      if (response.ok) {
        console.log('Login successful!');
        console.log('Access token:', data.access_token);
        console.log('User:', data.user);
      } else {
        console.log('Login failed:', data.message || 'Unknown error');
      }
    } catch (e) {
      console.log('Failed to parse response as JSON:', await response.text());
    }
  } catch (error) {
    console.error('Error testing login API:', error);
  }
}

// Run the test
testLogin();
