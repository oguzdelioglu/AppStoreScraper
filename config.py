# config.py

# Set to True to enable proxy usage for API requests
USE_PROXY = True

# List of proxies to use (format: 'http://user:pass@host:port' or 'http://host:port')
# This list will be populated dynamically or manually updated.
PROXY_LIST = []
PROXY_URL = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text&timeout=6813"
