# AI Features Documentation

This document provides detailed information about the AI features implemented in the MindMate application.

## Context-Aware AI Recommendations

The application provides personalized recommendations based on the user's mood and journal entries. These recommendations are designed to help users improve their mental health and well-being.

### How It Works

1. **Data Collection**: The system collects data from:
   - Mood entries (ratings from 1-10)
   - Journal entries (text content)

2. **Sentiment Analysis**: Journal entries are analyzed using Natural Language Processing (NLP) to determine the emotional tone:
   - Positive sentiment (scores > 0.3)
   - Neutral sentiment (scores between -0.3 and 0.3)
   - Negative sentiment (scores < -0.3)

3. **Recommendation Generation**: Based on the user's mood and journal sentiment, the system generates:
   - **Journal Prompts**: Suggestions for topics to write about in the journal
   - **Coping Strategies**: Techniques to help manage stress, anxiety, or other challenging emotions

### Example Recommendations

#### For Low Mood (< 5/10)

- **Journal Prompts**:
  - "How has your mood been today? What factors might be contributing to your current mood?"
  - "What are three things you're grateful for today?"

- **Coping Strategies**:
  - "Do 10 minutes of physical activity."
  - "Reach out to a friend or family member."

#### For Negative Journal Sentiment

- **Journal Prompts**:
  - "Reflect on a moment that brought you joy today."
  - "What are three things you're grateful for today?"

## API Endpoints

### Get Personalized Recommendations

```
GET /api/ai/recommendations
```

This endpoint returns personalized journal prompts and coping strategies based on the user's recent mood entries and journal entries.

**Response Example**:
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
  "user_id": "user-id-here"
}
```

## Implementation Details

### NLP Service

The NLP service provides sentiment analysis and keyword extraction capabilities:

- **Sentiment Analysis**: Uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze the emotional tone of text
- **Keyword Extraction**: Extracts important keywords from text based on frequency and relevance

### Recommendation Service

The recommendation service generates personalized suggestions based on user data:

- **Journal Prompts**: Selected based on mood ratings and journal sentiment
- **Coping Strategies**: Selected based on mood ratings and patterns

## Future Enhancements

1. **Pattern Detection**: Implement more advanced pattern detection to identify trends in mood and behavior
2. **Personalization Improvements**: Enhance the recommendation algorithm to better tailor suggestions to individual users
3. **Feedback Loop**: Incorporate user feedback to improve recommendation quality over time
4. **Visualization Enhancements**: Add more interactive visualizations for mood trends and correlations

## Technical Implementation

The AI features are implemented using:

- **NLTK**: For natural language processing and sentiment analysis
- **FastAPI**: For API endpoints
- **DynamoDB**: For data storage

The implementation follows a modular architecture with separate services for:
- NLP processing
- Recommendation generation
- API endpoints
