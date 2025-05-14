# Tests for NLP service with explicit NLTK path setup.
import os
import sys
import nltk
import pytest

# Ensure NLTK data is loaded from the correct path
nltk.data.path = [os.environ.get('NLTK_DATA', os.path.expanduser('~/nltk_data'))]
print(f"NLTK data path set to: {nltk.data.path}")

# Import the rest of the test file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.services.nlp_service import (
    calculate_sentiment_score,
    analyze_sentiment,
    extract_keywords
)

@pytest.mark.unit
def test_calculate_sentiment_score():
    """Test sentiment score calculation."""
    # Positive text
    positive_text = "I am feeling great today! Everything is wonderful."
    positive_score = calculate_sentiment_score(positive_text)
    assert isinstance(positive_score, float)
    assert 0 < positive_score <= 1
    
    # Negative text
    negative_text = "I am feeling terrible today. Everything is awful."
    negative_score = calculate_sentiment_score(negative_text)
    assert isinstance(negative_score, float)
    assert -1 <= negative_score < 0
    
    # Neutral text
    neutral_text = "Today is Monday. The sky is blue."
    neutral_score = calculate_sentiment_score(neutral_text)
    assert isinstance(neutral_score, float)
    assert -0.3 < neutral_score < 0.3  # Roughly neutral
    
    # Empty text
    empty_score = calculate_sentiment_score("")
    assert empty_score == 0.0

@pytest.mark.unit
def test_analyze_sentiment():
    """Test sentiment analysis."""
    # Positive text
    positive_text = "I am feeling great today! Everything is wonderful."
    positive_sentiment = analyze_sentiment(positive_text)
    assert isinstance(positive_sentiment, dict)
    assert "compound" in positive_sentiment
    assert "pos" in positive_sentiment
    assert "neg" in positive_sentiment
    assert "neu" in positive_sentiment
    assert positive_sentiment["compound"] > 0
    
    # Negative text
    negative_text = "I am feeling terrible today. Everything is awful."
    negative_sentiment = analyze_sentiment(negative_text)
    assert isinstance(negative_sentiment, dict)
    assert negative_sentiment["compound"] < 0
    
    # Neutral text
    neutral_text = "Today is Monday. The sky is blue."
    neutral_sentiment = analyze_sentiment(neutral_text)
    assert isinstance(neutral_sentiment, dict)
    assert -0.3 < neutral_sentiment["compound"] < 0.3  # Roughly neutral
    
    # Empty text
    empty_sentiment = analyze_sentiment("")
    assert empty_sentiment["compound"] == 0.0

@pytest.mark.unit
def test_extract_keywords():
    """Test keyword extraction."""
    # Test with normal text
    text = "The quick brown fox jumps over the lazy dog. The fox is quick and brown."
    keywords = extract_keywords(text, top_n=3)
    assert isinstance(keywords, list)
    assert len(keywords) <= 3
    
    # Test with empty text
    empty_keywords = extract_keywords("", top_n=3)
    assert isinstance(empty_keywords, list)
    assert len(empty_keywords) == 0
    
    # Test with short text
    short_keywords = extract_keywords("Hello world", top_n=3)
    assert isinstance(short_keywords, list)
    assert len(short_keywords) <= 2  # Should have at most 2 keywords
    
    # Test with different top_n
    many_keywords = extract_keywords(text, top_n=5)
    assert isinstance(many_keywords, list)
    assert len(many_keywords) <= 5
