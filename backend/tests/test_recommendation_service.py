"""
Tests for recommendation service.
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.services.recommendation_service import generate_recommendations
from backend.tests.report import TestReporter

# Test reporters
recommendations_reporter = TestReporter("recommendation_service.generate_recommendations", "UNIT")

@pytest.mark.unit
@pytest.mark.ai
@pytest.mark.asyncio
async def test_generate_recommendations_low_mood():
    """Test recommendation generation with low mood."""
    # Mock data
    user_id = "test-user"
    mood_data = [
        {
            "mood_rating": 3,
            "timestamp": datetime.utcnow().isoformat(),
            "notes": "Feeling down today"
        }
    ]
    journal_data = [
        {
            "content": "Today was a difficult day. I struggled with anxiety.",
            "timestamp": datetime.utcnow().isoformat(),
            "title": "Tough Day"
        }
    ]
    
    # Generate recommendations
    recommendations = await generate_recommendations(user_id, mood_data, journal_data)
    
    # Assertions
    assert isinstance(recommendations, dict)
    assert "journal_prompts" in recommendations
    assert "coping_strategies" in recommendations
    assert "timestamp" in recommendations
    assert "user_id" in recommendations
    assert recommendations["user_id"] == user_id
    
    # Check that we have journal prompts
    assert len(recommendations["journal_prompts"]) > 0
    for prompt in recommendations["journal_prompts"]:
        assert "title" in prompt
        assert "prompt" in prompt
    
    # Check that we have coping strategies
    assert len(recommendations["coping_strategies"]) > 0
    for strategy in recommendations["coping_strategies"]:
        assert "title" in strategy
        assert "description" in strategy
    
    # For low mood, we should have specific recommendations
    prompt_titles = [p["title"] for p in recommendations["journal_prompts"]]
    strategy_titles = [s["title"] for s in recommendations["coping_strategies"]]
    
    # Check for expected recommendations for low mood
    assert "Mood Reflection" in prompt_titles or "Gratitude" in prompt_titles
    assert "Physical Exercise" in strategy_titles or "Social Connection" in strategy_titles
    
    recommendations_reporter.register_test("test_generate_recommendations_low_mood", 
                                         "Test recommendation generation with low mood")

@pytest.mark.unit
@pytest.mark.ai
@pytest.mark.asyncio
async def test_generate_recommendations_negative_sentiment():
    """Test recommendation generation with negative journal sentiment."""
    # Mock data
    user_id = "test-user"
    mood_data = [
        {
            "mood_rating": 6,  # Neutral mood
            "timestamp": datetime.utcnow().isoformat(),
            "notes": "Average day"
        }
    ]
    journal_data = [
        {
            "content": "I'm feeling very anxious and sad today. Nothing seems to be going right.",
            "timestamp": datetime.utcnow().isoformat(),
            "title": "Anxious Day"
        }
    ]
    
    # Generate recommendations
    recommendations = await generate_recommendations(user_id, mood_data, journal_data)
    
    # Assertions
    assert isinstance(recommendations, dict)
    assert "journal_prompts" in recommendations
    assert "coping_strategies" in recommendations
    
    # For negative sentiment, we should have specific recommendations
    prompt_titles = [p["title"] for p in recommendations["journal_prompts"]]
    
    # Check for expected recommendations for negative sentiment
    assert "Joy" in prompt_titles or "Gratitude" in prompt_titles
    
    recommendations_reporter.register_test("test_generate_recommendations_negative_sentiment", 
                                         "Test recommendation generation with negative journal sentiment")

@pytest.mark.unit
@pytest.mark.ai
@pytest.mark.asyncio
async def test_generate_recommendations_positive_mood():
    """Test recommendation generation with positive mood and sentiment."""
    # Mock data
    user_id = "test-user"
    mood_data = [
        {
            "mood_rating": 8,
            "timestamp": datetime.utcnow().isoformat(),
            "notes": "Feeling great today"
        }
    ]
    journal_data = [
        {
            "content": "Today was a wonderful day. I accomplished a lot and felt happy.",
            "timestamp": datetime.utcnow().isoformat(),
            "title": "Great Day"
        }
    ]
    
    # Generate recommendations
    recommendations = await generate_recommendations(user_id, mood_data, journal_data)
    
    # Assertions
    assert isinstance(recommendations, dict)
    assert "journal_prompts" in recommendations
    assert "coping_strategies" in recommendations
    
    # For positive mood, we should get random recommendations
    assert len(recommendations["journal_prompts"]) > 0
    assert len(recommendations["coping_strategies"]) > 0
    
    recommendations_reporter.register_test("test_generate_recommendations_positive_mood", 
                                         "Test recommendation generation with positive mood and sentiment")

@pytest.mark.unit
@pytest.mark.ai
@pytest.mark.asyncio
async def test_generate_recommendations_empty_data():
    """Test recommendation generation with empty data."""
    # Mock data
    user_id = "test-user"
    mood_data = []
    journal_data = []
    
    # Generate recommendations
    recommendations = await generate_recommendations(user_id, mood_data, journal_data)
    
    # Assertions
    assert isinstance(recommendations, dict)
    assert "journal_prompts" in recommendations
    assert "coping_strategies" in recommendations
    
    # Should still get random recommendations
    assert len(recommendations["journal_prompts"]) > 0
    assert len(recommendations["coping_strategies"]) > 0
    
    recommendations_reporter.register_test("test_generate_recommendations_empty_data", 
                                         "Test recommendation generation with empty data")
