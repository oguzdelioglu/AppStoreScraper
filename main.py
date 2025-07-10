import logging
import os
from datetime import datetime
import pandas as pd
import concurrent.futures

from src.itunes_api import fetch_proxies_from_url # get_keyword_suggestions removed
from src.analysis import extract_keywords_from_text, is_app_considered_new, calculate_keyword_metrics
from src.sitemap_parser import get_all_app_urls_from_sitemaps
from src.app_scraper import scrape_app_details
from config import ONLY_POPULAR_COUNTRIES, POPULAR_COUNTRIES

# Configure logging
logging.basicConfig(level=logging.INFO, format='> %(message)s')

COUNTRY_CODES = [
    'cn', 'co', 'mw', 'sk', 'rw', 'to', 'kg', 'gw', 'pa', 'uy', 'xk', 'sn', 'sv', 'mr', 'fi',
    'is', 'tz', 'st', 'pk', 'dz', 'si', 'bo', 'bz', 'mm', 'ga', 'la', 'zw', 'sl', 'fj', 'by',
    'hu', 'lr', 'za', 'th', 'ao', 'lb', 'jo', 'ne', 'ly', 'hn', 'sc', 'tr', 'dk', 'vg', 'ch',
    'gr', 'tj', 'bm', 'pw', 'lc', 'id', 'vu', 'pg', 'ca', 'jm', 'ai', 'at', 'jp', 'ar', 'bb',
    'de', 'ag', 'gm', 'ky', 'mn', 'bf', 'ye', 'es', 'td', 'my', 'no', 'vc', 'ni', 'ph', 'ke',
    'fm', 'tn', 'ro', 'kz', 'az', 'hr', 'il', 'tt', 'mv', 'eg', 'ng', 'cv', 'br', 'tc', 'be',
    'ug', 'bt', 'kw', 'fr', 'om', 'lu', 'pt', 'cl', 'np', 'lt', 'iq', 'na', 'ci', 'tm', 'ba',
    'bg', 'mx', 'cm', 'ma', 'cr', 'cg', 'rs', 'me', 'mt', 'tw', 've', 'nz', 'gb', 'zm', 'nr',
    'mg', 'bn', 'mz', 'kh', 'do', 'py', 'vn', 'gt', 'dm', 'ee', 'ua', 'kn', 'kr', 'cz', 'us',
    'cy', 'gy', 'sz', 'mu', 'pe', 'qa', 'sr', 'au', 'lv', 'sa', 'cd', 'sb', 'it', 'af', 'uz',
    'md', 'in', 'nl', 'pl', 'hk', 'bh', 'sg', 'bw', 'mk', 'gd', 'ae', 'lk', 'se', 'ru', 'ie',
    'bj', 'am', 'gh', 'mo', 'ml', 'ms', 'bs', 'ec', 'al'
]

MAIN_SITEMAP_URL = "https://apps.apple.com/sitemaps_apps_index_app_1.xml"

def process_app_for_keywords(app_entry):
    app_id = app_entry.get('app_id')
    app_url = app_entry.get('url')
    hreflangs = app_entry.get('hreflangs', [])

    all_keyword_data = []

    # Process the main URL first (usually en-us or default)
    main_app_details = scrape_app_details(app_url)
    if main_app_details:
        country_code = "us" # Assuming main URL is for US or default
        text_for_keywords = f"{main_app_details.get('app_name', '')} {main_app_details.get('description', '')}"
        keywords = extract_keywords_from_text(text_for_keywords, country_code, num_keywords=3)
        
        keyword_entry = {
            'AppID': app_id,
            'AppURL': app_url,
            'AppName': main_app_details.get('app_name'),
            'Developer': main_app_details.get('developer'),
            'Category': main_app_details.get('category'),
            'ReleaseDate': main_app_details.get('release_date'),
            'Price': main_app_details.get('price'),
            'Language': 'en-us', # Assuming main is en-us
            'Keywords': ', '.join(keywords)
        }
        all_keyword_data.append(keyword_entry)

    # Process hreflang URLs
    for hreflang_entry in hreflangs:
        lang_code = hreflang_entry['hreflang']
        href_url = hreflang_entry['href']
        
        # Extract country code from hreflang (e.g., en-us -> us)
        country_code_match = lang_code.split('-')
        country_code = country_code_match[1].lower() if len(country_code_match) == 2 else 'N/A'

        # Skip if not a popular country and ONLY_POPULAR_COUNTRIES is True
        if ONLY_POPULAR_COUNTRIES and country_code not in POPULAR_COUNTRIES:
            continue

        localized_app_details = scrape_app_details(href_url)
        if localized_app_details:
            text_for_keywords = f"{localized_app_details.get('app_name', '')} {localized_app_details.get('description', '')}"
            keywords = extract_keywords_from_text(text_for_keywords, country_code, num_keywords=3)
            
            keyword_entry = {
                'AppID': app_id,
                'AppURL': href_url,
                'AppName': localized_app_details.get('app_name'),
                'Developer': localized_app_details.get('developer'),
                'Category': localized_app_details.get('category'),
                'ReleaseDate': localized_app_details.get('release_date'),
                'Price': localized_app_details.get('price'),
                'Language': lang_code,
                'Keywords': ', '.join(keywords)
            }
            all_keyword_data.append(keyword_entry)

    return all_keyword_data

def main():
    """Main function to run the App Store analysis."""
    # Proxy fetching logic removed as proxies are no longer used in main.py

    countries_to_analyze = POPULAR_COUNTRIES if ONLY_POPULAR_COUNTRIES else COUNTRY_CODES

    current_run_output_dir = f"outputs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(current_run_output_dir, exist_ok=True)

    all_app_urls = get_all_app_urls_from_sitemaps(MAIN_SITEMAP_URL)

    if not all_app_urls:
        logging.error("Could not retrieve any app URLs from sitemaps. Exiting.")
        return

    logging.info(f"Found {len(all_app_urls)} app URLs from sitemaps. Starting analysis...")

    # Filter app_urls by country if ONLY_POPULAR_COUNTRIES is True
    # This filtering will now happen inside process_app_for_keywords for hreflangs
    # For the main URL, we assume it's always processed.
    
    all_processed_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: # Reduced max_workers for scraping
        future_to_app_entry = {executor.submit(process_app_for_keywords, app_entry): app_entry for app_entry in all_app_urls}
        for future in concurrent.futures.as_completed(future_to_app_entry):
            processed_data_for_app = future.result()
            if processed_data_for_app:
                all_processed_data.extend(processed_data_for_app)

    if not all_processed_data:
        logging.error(f"No data was analyzed. Could not generate a report.")
        return

    logging.info(f"Analysis complete. Generating report...")
    df = pd.DataFrame(all_processed_data)

    # Define columns for the final report
    final_cols = ['AppID', 'AppURL', 'AppName', 'Developer', 'Category', 'ReleaseDate', 'Price', 'Language', 'Keywords']
    df = df[final_cols]

    filename = f"{current_run_output_dir}/AppStore_Localized_Keywords_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    df.to_csv(filename, index=False)
    logging.info(f"Report successfully saved as '{filename}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user. Exiting.")
