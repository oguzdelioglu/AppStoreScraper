from datetime import datetime, timedelta
import re
import math

# A comprehensive list of common English stop words. Using a set for efficient lookups.
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm',
    'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn',
    'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'your',
    'you', 'app', 'apps', 'get', 'we', 'our', 'us', 'is', 'are', 'it', 'its', 'this', 'that', 'these',
    'those', 'has', 'have', 'had', 'do', 'does', 'did', 'was', 'were', 'be', 'been', 'being', 'i',
    'me', 'my', 'myself', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
    'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'from', 'up', 'down', 'in',
    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how',
    'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
    'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn',
    'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'app', 'apps', 'game', 'games', 'mobile',
    'phone', 'user', 'users', 'play', 'playing', 'new', 'best', 'top', 'free', 'paid', 'version',
    'update', 'updates', 'feature', 'features', 'experience', 'time', 'world', 'story', 'level',
    'levels', 'challenge', 'challenges', 'fun', 'enjoy', 'great', 'good', 'amazing', 'awesome',
    'fantastic', 'super', 'cool', 'easy', 'simple', 'addictive', 'download', 'install', 'get',
    'make', 'made', 'like', 'love', 'much', 'many', 'little', 'big', 'small', 'long', 'short',
    'first', 'second', 'third', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten', 'hundred', 'thousand', 'million', 'billion', 'trillion', 'etc', 'etcetera',
    'example', 'examples', 'e.g', 'i.e', 'vs', 'via'
}

def extract_keywords_from_text(text, num_keywords=5):
    """
    Extracts the most frequent, non-stop-word single words, bigrams, and trigrams from a given text.
    """
    if not text or not isinstance(text, str):
        return []

    # Find all words, convert to lower case
    words = re.findall(r'\b\w+\b', text.lower())

    # Filter out stop words and numeric-only words for single words
    filtered_words = [word for word in words if word not in STOP_WORDS and not word.isdigit()]

    # Generate bigrams and trigrams
    bigrams = [" ".join(words[i:i+2]) for i in range(len(words) - 1)]
    trigrams = [" ".join(words[i:i+3]) for i in range(len(words) - 2)]

    # Filter out n-grams containing stop words or numeric-only words
    # An n-gram is considered a stop-word if any of its constituent words is a stop word
    # or if it's entirely numeric.
    filtered_bigrams = [
        bg for bg in bigrams
        if all(word not in STOP_WORDS and not word.isdigit() for word in bg.split())
    ]
    filtered_trigrams = [
        tg for tg in trigrams
        if all(word not in STOP_WORDS and not word.isdigit() for word in tg.split())
    ]

    # Combine all candidate keywords
    all_candidates = filtered_words + filtered_bigrams + filtered_trigrams

    # Count frequency of all candidates
    keyword_counts = {}
    for keyword in all_candidates:
        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

    # Sort keywords by frequency in descending order
    sorted_keywords = sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)

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

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def calculate_keyword_metrics(input_data):
    """
    Calculates various keyword metrics based on the provided input data.
    """
    autocomplete_rank = input_data.get("autocomplete_rank", 0)
    competing_apps = input_data.get("competing_apps", 0)
    avg_top10_downloads = input_data.get("avg_top10_downloads", 0)
    avg_top10_rating = input_data.get("avg_top10_rating", 0)
    avg_top10_reviews = input_data.get("avg_top10_reviews", 0)
    ads_popularity_score = input_data.get("ads_popularity_score", 0)
    title_keyword_flag = input_data.get("title_keyword_flag", False)
    autocomplete_trend_7d = input_data.get("autocomplete_trend_7d", 0)

    # Volume
    volume = (110 - autocomplete_rank * 10) if autocomplete_rank > 0 else 10

    # Competitive
    competitive = min(100, math.log(competing_apps + 1) * 20)

    # Popularity
    popularity = ads_popularity_score if ads_popularity_score else volume * 0.8

    # Quality
    quality = ((avg_top10_rating / 5) * 50) + (min(avg_top10_downloads, 10000) / 200) + (min(avg_top10_reviews, 10000) / 200)

    # Top_10_Chance
    top_10_chance_numerator = (volume - competitive + (20 if title_keyword_flag else 0) + (autocomplete_trend_7d * 2))
    top_10_chance = sigmoid(top_10_chance_numerator / 10) * 100

    # Opportunity_Score
    opportunity_score = (volume * 0.6) + ((100 - competitive) * 0.3) + (top_10_chance * 0.1)

    return {
        "Volume": round(volume),
        "Competitive": round(competitive),
        "Popularity": round(popularity),
        "Quality": round(quality),
        "Top_10_Chance": round(top_10_chance),
        "Opportunity_Score": round(opportunity_score)
    }