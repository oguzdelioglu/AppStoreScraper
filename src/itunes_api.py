import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='> %(message)s')

BASE_RSS_URL = "https://rss.applemarketingtools.com/api/v2"
BASE_SEARCH_URL = "https://itunes.apple.com"

def _make_request(url, params=None):
    """
    A helper function to make requests to the API, handling errors.
    """
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

def get_top_app_ids(country, feed_type="apps", media_type="ios-apps", chart="top-free", limit=100):
    """
    Fetches the top app IDs from the Apple RSS feed.
    """
    url = f"{BASE_RSS_URL}/{country}/{media_type}/{feed_type}/{chart}/{limit}/explicit.json"
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

def get_search_result_count(term, country):
    """
    Gets the number of search results for a given term to estimate competition.
    """
    url = f"{BASE_SEARCH_URL}/search"
    params = {"term": term, "country": country, "media": "software", "limit": 1}
    
    data = _make_request(url, params)
    
    if data and "resultCount" in data:
        return data["resultCount"]
    return 0
