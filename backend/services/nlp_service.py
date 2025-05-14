"""
NLP service for analyzing text data.
"""
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a given text.
    Returns a dictionary with sentiment scores.
    """
    if not text:
        return {"compound": 0.0, "pos": 0.0, "neu": 0.0, "neg": 0.0}

    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)

def calculate_sentiment_score(text: str) -> float:
    """
    Calculate a normalized sentiment score from -1 (negative) to 1 (positive).
    """
    if not text:
        return 0.0

    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores['compound']

def extract_keywords(text: str, top_n: int = 5) -> list:
    """
    Extract keywords from a given text.
    Returns a list of keywords.
    """
    if not text:
        return []

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())

    # Filter out stopwords and short words
    filtered_words = [w for w in word_tokens if w not in stop_words and len(w) > 2]

    # Count word frequencies
    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Return top N keywords
    return [word for word, freq in sorted_words[:top_n]]