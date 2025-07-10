import requests
import logging
import time
import re
import random
from config import USE_PROXY, PROXY_LIST, DEFAULT_RETRY_WAIT_TIME

# Configure logging
logging.basicConfig(level=logging.INFO, format='> %(message)s')

BASE_RSS_URL = "https://rss.applemarketingtools.com/api/v2"
BASE_SEARCH_URL = "https://itunes.apple.com"

# Cache for keyword suggestions
_keyword_suggestions_cache = {}

# Rate limiting variables
_request_timestamps = []
MAX_REQUESTS_PER_MINUTE = 20 # Based on research for iTunes Search API

def _apply_rate_limit():
    global _request_timestamps
    _request_timestamps = [t for t in _request_timestamps if time.time() - t < 60] # Keep only last 60 seconds
    
    if len(_request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        time_to_wait = 60 - (time.time() - _request_timestamps[0])
        if time_to_wait > 0:
            logging.info(f"Rate limit hit. Waiting for {time_to_wait:.2f} seconds before next request.")
            time.sleep(time_to_wait)
    _request_timestamps.append(time.time())

def fetch_proxies_from_url(url):
    """
    Fetches a list of proxies from the given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        proxies = [p.strip() for p in response.text.splitlines() if p.strip()]
        logging.info(f"Fetched {len(proxies)} proxies from {url}")
        return proxies
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch proxies from {url}: {e}")
        return []

def _make_request(url, params=None, retry_count=0):
    """
    A helper function to make requests to the API, handling errors and rate limiting.
    Supports proxy rotation if USE_PROXY is True and PROXY_LIST is not empty.
    """
    _apply_rate_limit() # Apply rate limit before each request

    proxies = None
    if USE_PROXY and PROXY_LIST:
        proxy = random.choice(PROXY_LIST)
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        logging.info(f"Using proxy: {proxy}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, params=params, timeout=10, proxies=proxies, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError) and (e.response.status_code == 429 or e.response.status_code == 403):
            retry_after = e.response.headers.get('Retry-After')
            sleep_time = DEFAULT_RETRY_WAIT_TIME
            if retry_after and retry_after.isdigit():
                sleep_time = int(retry_after)
            logging.warning(f"Rate limit hit or Forbidden ({e.response.status_code}). Retrying after {sleep_time} seconds...")
            time.sleep(sleep_time)
            if retry_count < 3: # Limit retries to prevent infinite loops
                return _make_request(url, params, retry_count + 1)
        logging.error(f"API request failed after retries: {e}")
        return None
    finally:
        # Add a small delay after each request to prevent hitting burst limits
        time.sleep(0.5)

def get_top_app_ids(country, media_type="apps", chart="top-free", limit=100):
    """
    Fetches the top app IDs from the Apple RSS feed.
    """
    # Corrected URL structure based on search results:
    # https://rss.applemarketingtools.com/api/v2/{country}/{media_type}/{chart}/{limit}/{genre}.json
    url = f"{BASE_RSS_URL}/{country}/{media_type}/{chart}/{limit}/apps.json"
    
    logging.info(f"Fetching top {limit} apps from {country}/{chart}...")
    
    data = _make_request(url)
    
    if data and "feed" in data and "results" in data["feed"]:
        app_ids = [app["id"] for app in data["feed"]["results"]]
        logging.info(f"Successfully fetched {len(app_ids)} app IDs.")
        return app_ids
    logging.error("Could not parse top apps feed.")
    return []

def get_app_details(app_id, country):
    """
    Fetches detailed information for a specific app using its ID.
    """
    url = f"{BASE_SEARCH_URL}/lookup"
    params = {"id": app_id, "country": country}
    
    data = _make_request(url, params)
    
    if data and data.get("resultCount") > 0:
        return data["results"][0]
    return None

def clean_keyword(keyword):
    """
    Removes special characters from a keyword, keeping only alphanumeric and spaces.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', keyword).strip()

def get_keyword_suggestions(term, country='us', limit=10):
    """
    Fetches app names from iTunes Search API based on a term to use as suggestions.
    Generates single words and two-word combinations, cleans them, and scores them.
    Uses caching to avoid redundant API calls.
    """
    cache_key = (term, country, limit)
    if cache_key in _keyword_suggestions_cache:
        logging.info(f"Returning keyword suggestions for \"{term}\" from cache.")
        return _keyword_suggestions_cache[cache_key]

    logging.info(f"Fetching keyword suggestions for term: \"{term}\", country: {country}, limit: {limit}")
    
    url = f"{BASE_SEARCH_URL}/search"
    params = {
        "term": term,
        "country": country,
        "limit": limit,
        "entity": "software"  # Search for software (apps)
    }
    logging.info(f"Making request to: {url} with params: {params}")
    
    data = _make_request(url, params)
    
    suggestions = set()
    if data and data.get("resultCount") > 0:
        apps = data["results"]
        logging.info(f"Found {len(apps)} apps in search results")
        
        for app in apps:
            if "trackName" in app:
                words = app["trackName"].lower().split()
                
                # Single words
                for word in words:
                    if len(word) > 3:
                        clean_word = clean_keyword(word)
                        if len(clean_word) > 3:
                            suggestions.add(clean_word)
                
                # Two-word combinations (bigrams)
                for i in range(len(words) - 1):
                    if len(words[i]) > 2 and len(words[i+1]) > 2:
                        phrase = f"{words[i]} {words[i+1]}"
                        clean_phrase = clean_keyword(phrase)
                        if len(clean_phrase) > 3:
                            suggestions.add(clean_phrase)
    
    logging.info(f"Generated {len(suggestions)} unique keyword suggestions")
    
    scored_suggestions = []
    for suggestion in suggestions:
        # Length score
        word_count = len(suggestion.split())
        if word_count == 2:
            length_score = 100
        elif word_count == 3:
            length_score = 90
        elif word_count == 1:
            length_score = 80
        else:
            length_score = 70
        
        # Match score
        match_score = 100 if term.lower() in suggestion.lower() else 50
        
        # Total score
        total_score = round((length_score + match_score) / 2)
        
        scored_suggestions.append({
            "keyword": suggestion,
            "score": total_score
        })
    
    # Sort by score in descending order
    scored_suggestions.sort(key=lambda x: x["score"], reverse=True)
    
    result = {
        "suggestions": scored_suggestions[:20], # Top 20 suggestions
        "count": len(scored_suggestions)
    }
    _keyword_suggestions_cache[cache_key] = result
    return result


