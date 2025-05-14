import asyncio
import json
from backend.services import recommendation_service
from backend.services import nlp_service

async def test_recommendations():
    # Test data
    user_id = 'test-user'
    mood_data = [
        {
            'mood_rating': 4, 
            'timestamp': '2023-05-01T12:00:00', 
            'notes': 'Feeling a bit down today'
        }
    ]
    journal_data = [
        {
            'content': 'Today was a challenging day. I struggled with anxiety.', 
            'timestamp': '2023-05-01T20:00:00', 
            'title': 'Tough Day'
        }
    ]
    
    # Test sentiment analysis
    sentiment = nlp_service.calculate_sentiment_score(journal_data[0]['content'])
    print(f"Sentiment score: {sentiment}")
    
    # Test recommendation generation
    result = await recommendation_service.generate_recommendations(user_id, mood_data, journal_data)
    print("Recommendations:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_recommendations())
