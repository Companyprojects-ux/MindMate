"""
Simplified recommendation service for generating personalized suggestions.
"""
from typing import List, Dict, Any
import random
from datetime import datetime, timedelta
from backend.services import nlp_service
from backend.core.utils import generate_uuid

# Sample recommendation templates
JOURNAL_PROMPTS = [
    {"title": "Mood Reflection", "prompt": "How has your mood been today? What factors might be contributing to your current mood?"},
    {"title": "Gratitude", "prompt": "What are three things you're grateful for today?"},
    {"title": "Self-Care", "prompt": "How did you practice self-care today?"},
    {"title": "Emotions", "prompt": "What emotions were most present for you today?"},
    {"title": "Looking Forward", "prompt": "What's something you're looking forward to tomorrow?"},
    {"title": "Joy", "prompt": "Reflect on a moment that brought you joy today."},
    {"title": "Learning", "prompt": "What's something you learned about yourself recently?"},
    {"title": "Sleep", "prompt": "How have your sleep patterns affected your mood this week?"}
]

COPING_STRATEGIES = [
    {"title": "Deep Breathing", "description": "Practice deep breathing for 5 minutes."},
    {"title": "Mindful Walking", "description": "Take a short walk and focus on your surroundings."},
    {"title": "Gratitude Practice", "description": "Write down three things you're grateful for."},
    {"title": "Progressive Muscle Relaxation", "description": "Tense and relax each muscle group."},
    {"title": "5-4-3-2-1 Grounding", "description": "Name 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, and 1 thing you taste."},
    {"title": "Journaling", "description": "Write about your thoughts and feelings."},
    {"title": "Physical Exercise", "description": "Do 10 minutes of physical activity."},
    {"title": "Social Connection", "description": "Reach out to a friend or family member."}
]

async def generate_recommendations(user_id: str, mood_data: List[Dict[str, Any]], journal_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate personalized recommendations based on user data.
    
    Args:
        user_id: User ID
        mood_data: List of mood entries
        journal_data: List of journal entries
        
    Returns:
        Dictionary with personalized recommendations
    """
    recommendations = {
        "journal_prompts": [],
        "coping_strategies": [],
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id
    }
    
    # Calculate average mood if available
    avg_mood = None
    if mood_data:
        recent_moods = sorted(mood_data, 
                           key=lambda x: x.get('timestamp', ''),
                           reverse=True)[:5]  # Get 5 most recent entries
        if recent_moods:
            avg_mood = sum(entry.get('mood_rating', 5) for entry in recent_moods) / len(recent_moods)
    
    # Calculate average sentiment if available
    avg_sentiment = None
    if journal_data:
        recent_entries = sorted(journal_data, 
                             key=lambda x: x.get('timestamp', ''),
                             reverse=True)[:3]  # Get 3 most recent entries
        if recent_entries:
            sentiments = [nlp_service.calculate_sentiment_score(entry.get('content', '')) for entry in recent_entries]
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else None
    
    # Select journal prompts based on mood and sentiment
    if avg_mood is not None and avg_mood < 5:
        # For low mood, suggest reflection and gratitude
        recommendations["journal_prompts"].append(next((p for p in JOURNAL_PROMPTS if p["title"] == "Mood Reflection"), JOURNAL_PROMPTS[0]))
        recommendations["journal_prompts"].append(next((p for p in JOURNAL_PROMPTS if p["title"] == "Gratitude"), JOURNAL_PROMPTS[1]))
    elif avg_sentiment is not None and avg_sentiment < -0.3:
        # For negative sentiment, suggest joy and gratitude
        recommendations["journal_prompts"].append(next((p for p in JOURNAL_PROMPTS if p["title"] == "Joy"), JOURNAL_PROMPTS[5]))
        recommendations["journal_prompts"].append(next((p for p in JOURNAL_PROMPTS if p["title"] == "Gratitude"), JOURNAL_PROMPTS[1]))
    else:
        # Otherwise, select random prompts
        prompts = random.sample(JOURNAL_PROMPTS, min(2, len(JOURNAL_PROMPTS)))
        recommendations["journal_prompts"].extend(prompts)
    
    # Select coping strategies based on mood
    if avg_mood is not None and avg_mood < 5:
        # For low mood, suggest physical exercise and social connection
        recommendations["coping_strategies"].append(next((s for s in COPING_STRATEGIES if s["title"] == "Physical Exercise"), COPING_STRATEGIES[6]))
        recommendations["coping_strategies"].append(next((s for s in COPING_STRATEGIES if s["title"] == "Social Connection"), COPING_STRATEGIES[7]))
    else:
        # Otherwise, select random strategies
        strategies = random.sample(COPING_STRATEGIES, min(2, len(COPING_STRATEGIES)))
        recommendations["coping_strategies"].extend(strategies)
    
    return recommendations
