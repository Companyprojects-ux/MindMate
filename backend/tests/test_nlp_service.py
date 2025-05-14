"""
Tests for NLP service.
"""
import pytest
from backend.services.nlp_service import (
    calculate_sentiment_score,
    analyze_sentiment,
    extract_keywords
)
from backend.tests.report import TestReporter

# Test reporters
sentiment_reporter = TestReporter("nlp_service.calculate_sentiment_score", "UNIT")
analyze_reporter = TestReporter("nlp_service.analyze_sentiment", "UNIT")
keywords_reporter = TestReporter("nlp_service.extract_keywords", "UNIT")

@pytest.mark.unit
@pytest.mark.ai
def test_calculate_sentiment_score():
    """Test sentiment score calculation."""
    # Positive text
    positive_text = "I am feeling great today! Everything is wonderful."
    positive_score = calculate_sentiment_score(positive_text)
    assert isinstance(positive_score, float)
    assert 0 < positive_score <= 1
    sentiment_reporter.register_test("test_calculate_sentiment_score_positive", 
                                    "Test sentiment score calculation with positive text")
    
    # Negative text
    negative_text = "I am feeling terrible today. Everything is awful."
    negative_score = calculate_sentiment_score(negative_text)
    assert isinstance(negative_score, float)
    assert -1 <= negative_score < 0
    sentiment_reporter.register_test("test_calculate_sentiment_score_negative", 
                                    "Test sentiment score calculation with negative text")
    
    # Neutral text
    neutral_text = "Today is Monday. The sky is blue."
    neutral_score = calculate_sentiment_score(neutral_text)
    assert isinstance(neutral_score, float)
    assert -0.3 < neutral_score < 0.3  # Roughly neutral
    sentiment_reporter.register_test("test_calculate_sentiment_score_neutral", 
                                    "Test sentiment score calculation with neutral text")
    
    # Empty text
    empty_score = calculate_sentiment_score("")
    assert empty_score == 0.0
    sentiment_reporter.register_test("test_calculate_sentiment_score_empty", 
                                    "Test sentiment score calculation with empty text")

@pytest.mark.unit
@pytest.mark.ai
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
    analyze_reporter.register_test("test_analyze_sentiment_positive", 
                                  "Test sentiment analysis with positive text")
    
    # Negative text
    negative_text = "I am feeling terrible today. Everything is awful."
    negative_sentiment = analyze_sentiment(negative_text)
    assert isinstance(negative_sentiment, dict)
    assert negative_sentiment["compound"] < 0
    analyze_reporter.register_test("test_analyze_sentiment_negative", 
                                  "Test sentiment analysis with negative text")
    
    # Neutral text
    neutral_text = "Today is Monday. The sky is blue."
    neutral_sentiment = analyze_sentiment(neutral_text)
    assert isinstance(neutral_sentiment, dict)
    assert -0.3 < neutral_sentiment["compound"] < 0.3  # Roughly neutral
    analyze_reporter.register_test("test_analyze_sentiment_neutral", 
                                  "Test sentiment analysis with neutral text")
    
    # Empty text
    empty_sentiment = analyze_sentiment("")
    assert empty_sentiment["compound"] == 0.0
    analyze_reporter.register_test("test_analyze_sentiment_empty", 
                                  "Test sentiment analysis with empty text")

@pytest.mark.unit
@pytest.mark.ai
def test_extract_keywords():
    """Test keyword extraction."""
    # Test with normal text
    text = "The quick brown fox jumps over the lazy dog. The fox is quick and brown."
    keywords = extract_keywords(text, top_n=3)
    assert isinstance(keywords, list)
    assert len(keywords) <= 3
    assert "fox" in keywords  # Should be a top keyword
    keywords_reporter.register_test("test_extract_keywords_normal", 
                                   "Test keyword extraction with normal text")
    
    # Test with empty text
    empty_keywords = extract_keywords("", top_n=3)
    assert isinstance(empty_keywords, list)
    assert len(empty_keywords) == 0
    keywords_reporter.register_test("test_extract_keywords_empty", 
                                   "Test keyword extraction with empty text")
    
    # Test with short text
    short_keywords = extract_keywords("Hello world", top_n=3)
    assert isinstance(short_keywords, list)
    assert len(short_keywords) <= 2  # Should have at most 2 keywords
    keywords_reporter.register_test("test_extract_keywords_short", 
                                   "Test keyword extraction with short text")
    
    # Test with different top_n
    many_keywords = extract_keywords(text, top_n=5)
    assert isinstance(many_keywords, list)
    assert len(many_keywords) <= 5
    keywords_reporter.register_test("test_extract_keywords_many", 
                                   "Test keyword extraction with different top_n")
