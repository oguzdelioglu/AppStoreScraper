from datetime import datetime, timedelta
import re

# A simple list of common English stop words. A more robust solution might use a library like NLTK.
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'of', 'at', 'by', 'for', 'with', 
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 
    'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 
    'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'your', 
    'you', 'app', 'apps', 'get', 'we', 'our', 'us', 'is', 'are', 'it', 'its'
}

def extract_keywords_from_text(text, num_keywords=5):
    """
    Extracts the most frequent, non-stop-word keywords from a given text.
    """
    if not text or not isinstance(text, str):
        return []

    # Find all words, convert to lower case
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Count frequency of words that are not stop words
    word_counts = {}
    for word in words:
        if word not in STOP_WORDS and not word.isdigit():
            word_counts[word] = word_counts.get(word, 0) + 1
            
    # Sort words by frequency in descending order
    sorted_keywords = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    
    # Return the top `num_keywords`
    return [keyword for keyword, count in sorted_keywords[:num_keywords]]

def is_app_considered_new(release_date_str, days_threshold=60):
    """
    Checks if an app is considered new based on its release date.
    """
    if not release_date_str:
        return False
    try:
        # Parse the ISO 8601 format date string
        release_date = datetime.fromisoformat(release_date_str.replace('Z', '+00:00'))
        return (datetime.now(release_date.tzinfo) - release_date) < timedelta(days=days_threshold)
    except (ValueError, TypeError):
        return False
