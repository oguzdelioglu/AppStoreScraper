import re
import logging

logging.basicConfig(level=logging.INFO, format='> %(message)s')

def extract_app_name_from_url(url):
    """
    Extracts the app name from an App Store URL.
    Example: https://apps.apple.com/id/app/qiandao-art-toys-mart/id1492978492 -> qiandao-art-toys-mart
    """
    match = re.search(r'/app/([^/]+)/id\d+', url)
    if match:
        return match.group(1).replace('-', ' ') # Replace hyphens with spaces for better keywords
    return None