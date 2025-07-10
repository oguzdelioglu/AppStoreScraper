# config.py

DEFAULT_RETRY_WAIT_TIME = 5 # seconds

# Set to True to enable proxy usage for API requests
USE_PROXY = False

# Set to True to analyze only popular countries
ONLY_POPULAR_COUNTRIES = True

# List of popular countries (ISO 2-letter codes)
POPULAR_COUNTRIES = ['us', 'gb', 'ca', 'au', 'de', 'fr', 'jp', 'cn', 'br', 'in']

# List of proxies to use (format: 'http://user:pass@host:port' or 'http://host:port')
# This list will be populated dynamically or manually updated.
PROXY_LIST = []
PROXY_URL = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/all/data.txt"
