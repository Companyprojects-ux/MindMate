# Mental Health Support with Medicine Reminder

A comprehensive mental health support application with medicine reminder functionality. This application helps users track their medications, set reminders, monitor their mood, journal their thoughts, take mental health assessments, and receive AI-powered support.

## Features

- **User Authentication**: Secure user registration and login
- **Medication Management**: Track medications, dosages, and schedules
- **Reminder System**: Get notified when it's time to take medications
- **Mood Tracking**: Monitor mood patterns over time, track mood ratings, and view statistics
- **Journal**: Record thoughts and feelings with searchable entries and tagging
- **Mental Health Assessments**: Take standardized assessments like PHQ-9 and GAD-7
- **AI-powered Support**: Get personalized coping strategies and mental health support
- **Resources**: Access educational content and helpful resources

## AI-Powered Mental Health Support

The application includes advanced AI features that provide personalized mental health support:

### Features

- **Conversational Interface**: Natural, empathetic conversations with users through the AI chatbot
- **Context-Aware Recommendations**: Personalized journal prompts and coping strategies based on mood and journal sentiment
- **Sentiment Analysis**: Automatic analysis of journal entries to detect emotional states
- **Context-Aware Responses**: Personalized support based on user's mood, medications, journal entries, and assessment results
- **Evidence-Based Guidance**: Responses informed by trusted mental health resources using RAG (Retrieval-Augmented Generation)
- **Crisis Detection**: Automatic detection of crisis situations with appropriate support resources
- **Weekly Reports**: AI-generated summaries of progress and personalized recommendations

### RAG Pipeline

The chatbot uses a Retrieval-Augmented Generation (RAG) pipeline to provide evidence-based responses:

1. **Document Processing**: PDF documents from trusted mental health sources are loaded and processed
2. **Text Chunking**: Documents are split into manageable chunks
3. **Embedding Generation**: Text chunks are converted into vector embeddings
4. **Vector Storage**: Embeddings are stored in a FAISS vector database
5. **Similarity Search**: When a user asks a question, the system retrieves the most relevant information
6. **Response Generation**: The LLM generates a response based on the retrieved information and user context

### Context-Aware Personalization

The chatbot personalizes responses based on:

- Recent mood entries and mood statistics
- Current medications and upcoming reminders
- Journal entries and patterns
- Chat history for conversational context

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: AWS DynamoDB
- **Storage**: AWS S3
- **AI/ML**:
  - Google Gemini Pro for LLM capabilities
  - LangChain for RAG pipeline and orchestration
  - FAISS for vector storage and similarity search
  - PyPDF for document processing

### Frontend
- **Framework**: React 18 with Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand
- **Form Handling**: React Hook Form
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Data Visualization**: Chart.js with react-chartjs-2

## Documentation

- [Postman Guide](POSTMAN_GUIDE.md): Detailed instructions for testing the API with Postman
- [RAG Implementation](RAG_IMPLEMENTATION.md): Technical details about the RAG system
- [AI Features](AI_FEATURES.md): Documentation of the AI recommendation features
- [Frontend README](frontend/README.md): Documentation for the frontend module

## Testing

The application includes comprehensive tests for all backend functionality. Tests are organized by feature and include both unit tests and integration tests.

### Running Tests

To run all tests:
```bash
source venv/bin/activate
pytest
```

To run tests for a specific module:
```bash
pytest backend/tests/test_auth.py
```

To run tests with a specific marker:
```bash
pytest -m ai
```

### Test Structure

- `backend/tests/conftest.py`: Common test fixtures and utilities
- `backend/tests/test_*.py`: Tests organized by feature
- `backend/tests/report.py`: Test reporting utilities

### Continuous Integration

The project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/python-tests.yml` and runs automatically when code is pushed to the main branch or when a pull request is created.

The CI pipeline:
1. Sets up a Python environment
2. Installs dependencies
3. Runs the tests
4. Reports test coverage

This ensures that all code changes are tested automatically before being merged.

## Getting Started

### Prerequisites

- Python 3.12+
- AWS Account (for DynamoDB and S3)
- Google API Key (for Gemini Pro)
- NLTK (for natural language processing)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhigyan-Truce/MindMate.git
   cd MindMate
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual credentials.

5. Create DynamoDB tables:
   ```bash
   python scripts/create_tables.py
   ```

### Running the Application

#### Backend

Start the FastAPI server:
```bash
python run.py
```

Or directly with uvicorn:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at http://localhost:8001, and the API documentation at http://localhost:8001/api/docs.

#### Frontend

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Create a `.env` file in the frontend directory with the following variables:
```env
VITE_API_URL=http://localhost:8001
```

Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000 (or another port if 3000 is in use).

For detailed information about the frontend, see the [Frontend README](frontend/README.md).

### Docker

You can also run the application using Docker:

```bash
docker build -t mental-health-app .
docker run -p 8001:8001 --env-file .env mental-health-app
```

## API Endpoints

### Authentication
- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login and get JWT token
- `GET /api/auth/me`: Get current user profile
- `PUT /api/auth/me`: Update user profile
- `PUT /api/auth/password`: Change password

### Medications
- `GET /api/medications`: List all medications
- `POST /api/medications`: Add a new medication
- `GET /api/medications/{id}`: Get medication details
- `PUT /api/medications/{id}`: Update medication
- `DELETE /api/medications/{id}`: Delete medication
- `POST /api/medications/{id}/image`: Upload medication image

### Reminders
- `GET /api/reminders`: List all reminders
- `GET /api/reminders/today`: Get today's reminders
- `GET /api/reminders/upcoming`: Get upcoming reminders
- `POST /api/reminders`: Create a new reminder
- `PUT /api/reminders/{id}`: Update reminder
- `PUT /api/reminders/{id}/status`: Update reminder status
- `DELETE /api/reminders/{id}`: Delete reminder

### Mood Tracking
- `GET /api/moods`: List all mood entries
- `POST /api/moods`: Create a new mood entry
- `GET /api/moods/{id}`: Get mood entry details
- `PUT /api/moods/{id}`: Update mood entry
- `DELETE /api/moods/{id}`: Delete mood entry
- `GET /api/moods/stats`: Get mood statistics

### Journal
- `GET /api/journal`: List all journal entries
- `POST /api/journal`: Create a new journal entry
- `GET /api/journal/{id}`: Get journal entry details
- `PUT /api/journal/{id}`: Update journal entry
- `DELETE /api/journal/{id}`: Delete journal entry
- `GET /api/journal/search`: Search journal entries by content or tags

### AI Support
- `POST /api/ai/chat`: Send a message to the chatbot
- `GET /api/ai/chat/history`: Get chat history
- `GET /api/ai/recommendations`: Get personalized journal prompts and coping strategies based on mood and journal sentiment
- `GET /api/ai/legacy-recommendations`: Get legacy personalized recommendations (deprecated)
- `GET /api/ai/suggestions`: Get AI suggestions based on user context
- `GET /api/ai/weekly-report`: Get weekly progress report
- `POST /api/ai/feedback`: Submit feedback on AI suggestions
- `GET /api/ai/visualization_data`: Get data for visualizations

## License

This project is licensed under the MIT License - see the LICENSE file for details.
