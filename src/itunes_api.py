import requests
import logging
import time
import re
import random
from config import USE_PROXY, DEFAULT_RETRY_WAIT_TIME

# Configure logging
logging.basicConfig(level=logging.INFO, format='> %(message)s')

BASE_RSS_URL = "https://rss.applemarketingtools.com/api/v2"
BASE_SEARCH_URL = "https://itunes.apple.com"

# Cache for keyword suggestions (no longer used for iTunes Search API)
_keyword_suggestions_cache = {}
_country_keyword_cache = {}

# Rate limiting variables
_request_timestamps = []
MAX_REQUESTS_PER_MINUTE = 10 # Adjusted based on observed stricter limits

def _apply_rate_limit():
    global _request_timestamps
    _request_timestamps = [t for t in _request_timestamps if time.time() - t < 60] # Keep only last 60 seconds
    
    if len(_request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        time_to_wait = 60 - (time.time() - _request_timestamps[0])
        if time_to_wait > 0:
            logging.info(f"Rate limit hit. Waiting for {time_to_wait:.2f} seconds before next request. (Current requests in last minute: {len(_request_timestamps)})")
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
            sleep_time = DEFAULT_RETRY_WAIT_TIME * (2 ** retry_count)
            if retry_after and retry_after.isdigit():
                sleep_time = int(retry_after)
            logging.warning(f"Rate limit hit or Forbidden ({e.response.status_code}). Retrying after {sleep_time:.2f} seconds. URL: {url} (Proxy: {proxy if USE_PROXY and PROXY_LIST else 'None'})")
            time.sleep(sleep_time)
            if retry_count < 3: # Limit retries to prevent infinite loops
                return _make_request(url, params, retry_count + 1)
        logging.error(f"API request failed after retries: {e}. URL: {url} (Proxy: {proxy if USE_PROXY and PROXY_LIST else 'None'})")
        return None
    finally:
        # Add a small delay after each request to prevent hitting burst limits
        time.sleep(1)

def get_top_app_ids(country, media_type="apps", chart="top-free", limit=100):
    """
    Fetches the top app IDs from the Apple RSS feed.
    """
    url = f"{BASE_RSS_URL}/{country}/{media_type}/{chart}/{limit}/apps.json"
    
    logging.info(f"Fetching top {limit} apps from {country}/{chart}...")
    
    data = _make_request(url)
    
    if data and "feed" in data and "results" in data["feed"]:
        apps = data["feed"]["results"]
        logging.info(f"Successfully fetched {len(apps)} app data.")
        return apps
    logging.error("Could not parse top apps feed.")
    return []

def clean_keyword(keyword):
    """
    Removes special characters from a keyword, keeping only alphanumeric and spaces.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', keyword).strip()