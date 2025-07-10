import logging
import os
from datetime import datetime
import pandas as pd
import concurrent.futures

from src.itunes_api import fetch_proxies_from_url # get_keyword_suggestions removed
from src.analysis import extract_keywords_from_text, is_app_considered_new, calculate_keyword_metrics
from src.sitemap_parser import get_all_app_urls_from_sitemaps
from src.app_scraper import extract_app_name_from_url
from config import ONLY_POPULAR_COUNTRIES, POPULAR_COUNTRIES

# Configure logging
logging.basicConfig(level=logging.INFO, format='> %(message)s')

COUNTRY_CODES = [
    'cn', 'co', 'mw', 'sk', 'rw', 'to', 'kg', 'gw', 'pa', 'uy', 'xk', 'sn', 'sv', 'mr', 'fi',
    'is', 'tz', 'st', 'pk', 'dz', 'si', 'bo', 'bz', 'mm', 'ga', 'la', 'zw', 'sl', 'fj', 'by',
    'hu', 'lr', 'za', 'th', 'ao', 'lb', 'jo', 'ne', 'ly', 'hn', 'sc', 'tr', 'dk', 'vg', 'ch',
    'gr', 'tj', 'bm', 'pw', 'lc', 'id', 'vu', 'pg', 'ca', 'jm', 'ai', 'at', 'jp', 'ar',
    'bb', 'de', 'ag', 'gm', 'ky', 'mn', 'bf', 'ye', 'es', 'td', 'my', 'no', 'vc', 'ni', 'ph',
    'ke', 'fm', 'tn', 'ro', 'kz', 'az', 'hr', 'il', 'tt', 'mv', 'eg', 'ng', 'cv', 'br', 'tc',
    'be', 'ug', 'bt', 'kw', 'fr', 'om', 'lu', 'pt', 'cl', 'np', 'lt', 'iq', 'na', 'ci', 'tm',
    'ba', 'bg', 'mx', 'cm', 'ma', 'cr', 'cg', 'rs', 'me', 'mt', 'tw', 've', 'nz', 'gb', 'zm',
    'nr', 'mg', 'bn', 'mz', 'kh', 'do', 'py', 'vn', 'gt', 'dm', 'ee', 'ua', 'kn', 'kr', 'cz',
    'us', 'cy', 'gy', 'sz', 'mu', 'pe', 'qa', 'sr', 'au', 'lv', 'sa', 'cd', 'sb', 'it', 'af',
    'uz', 'md', 'in', 'nl', 'pl', 'hk', 'bh', 'sg', 'bw', 'mk', 'gd', 'ae', 'lk', 'se', 'ru',
    'ie', 'bj', 'am', 'gh', 'mo', 'ml', 'ms', 'bs', 'ec', 'al'
]

MAIN_SITEMAP_URL = "https://apps.apple.com/sitemaps_apps_index_app_1.xml"

def process_app_entry(app_entry):
    app_id = app_entry.get('app_id')
    base_app_url = app_entry.get('url')
    hreflangs = app_entry.get('hreflangs', [])

    # Initialize a dictionary for the current app's data
    app_data_row = {
        'AppID': app_id,
        'BaseAppURL': base_app_url,
        'MainAppName': 'N/A',
        'MainDeveloper': 'N/A',
        'MainCategory': 'N/A',
        'MainReleaseDate': 'N/A',
        'MainPrice': 'N/A',
        'MainKeywords': 'N/A'
    }

    # Process the main URL first (usually en-us or default)
    main_app_name = extract_app_name_from_url(base_app_url)
    if main_app_name:
        country_code = "us" # Assuming main URL is for US or default
        text_for_keywords = main_app_name # Use app name from URL as keyword source
        keywords = extract_keywords_from_text(text_for_keywords, country_code, num_keywords=3)
        
        app_data_row.update({
            'MainAppName': main_app_name,
            'MainKeywords': ', '.join(keywords)
        })

    # Process hreflang URLs
    for hreflang_entry in hreflangs:
        lang_code = hreflang_entry['hreflang']
        href_url = hreflang_entry['href']
        
        # Extract country code from hreflang (e.g., en-us -> us)
        country_code_parts = lang_code.split('-')
        country_code = country_code_parts[1].lower() if len(country_code_parts) == 2 else 'N/A'

        # Skip if not a popular country and ONLY_POPULAR_COUNTRIES is True
        if ONLY_POPULAR_COUNTRIES and country_code not in POPULAR_COUNTRIES:
            continue

        localized_app_name = extract_app_name_from_url(href_url)
        if localized_app_name:
            text_for_keywords = localized_app_name # Use app name from URL as keyword source
            keywords = extract_keywords_from_text(text_for_keywords, country_code, num_keywords=3)
            
            # Add localized data as new columns
            app_data_row[f'AppName_{lang_code}'] = localized_app_name
            app_data_row[f'Keywords_{lang_code}'] = ', '.join(keywords)
            app_data_row[f'URL_{lang_code}'] = href_url

    return app_data_row

def main():
    """Main function to run the App Store analysis."""
    countries_to_analyze = POPULAR_COUNTRIES if ONLY_POPULAR_COUNTRIES else COUNTRY_CODES

    current_run_output_dir = f"outputs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(current_run_output_dir, exist_ok=True)

    all_app_urls = get_all_app_urls_from_sitemaps(MAIN_SITEMAP_URL)

    if not all_app_urls:
        logging.error("Could not retrieve any app URLs from sitemaps. Exiting.")
        return

    logging.info(f"Found {len(all_app_urls)} app URLs from sitemaps. Starting analysis...")

    all_processed_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: # Reduced max_workers for scraping
        future_to_app_entry = {executor.submit(process_app_entry, app_entry): app_entry for app_entry in all_app_urls}
        for future in concurrent.futures.as_completed(future_to_app_entry):
            processed_data_for_app = future.result()
            if processed_data_for_app:
                all_processed_data.append(processed_data_for_app)

    if not all_processed_data:
        logging.error(f"No data was analyzed. Could not generate a report.")
        return

    logging.info(f"Analysis complete. Generating report...")
    df = pd.DataFrame(all_processed_data)

    # Dynamically create final_cols based on available data
    dynamic_cols = ['AppID', 'BaseAppURL', 'MainAppName', 'MainDeveloper', 'MainCategory', 'MainReleaseDate', 'MainPrice', 'MainKeywords']
    
    # Add localized columns that were actually generated
    for col in df.columns:
        if col.startswith(('AppName_', 'Keywords_', 'URL_')) and col not in dynamic_cols:
            dynamic_cols.append(col)

    df = df[dynamic_cols]

    filename = f"{current_run_output_dir}/AppStore_Localized_Keywords_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    df.to_csv(filename, index=False)
    logging.info(f"Report successfully saved as '{filename}'")

    # Aggregate and save all keywords by language
    all_keywords_by_language = {}
    for _, row in df.iterrows():
        # Process MainKeywords
        if row['MainKeywords'] and row['MainKeywords'] != 'N/A':
            lang = row['Language'] if 'Language' in row and row['Language'] != 'N/A' else 'en-us' # Default to en-us
            keywords = [k.strip() for k in row['MainKeywords'].split(',') if k.strip()]
            all_keywords_by_language.setdefault(lang, set()).update(keywords)

        # Process localized keywords
        for col in df.columns:
            if col.startswith('Keywords_') and row[col] and row[col] != 'N/A':
                lang = col.replace('Keywords_', '')
                keywords = [k.strip() for k in row[col].split(',') if k.strip()]
                all_keywords_by_language.setdefault(lang, set()).update(keywords)

    keywords_filename = f"{current_run_output_dir}/All_Keywords_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(keywords_filename, 'w', encoding='utf-8') as f:
        for lang, keywords_set in sorted(all_keywords_by_language.items()):
            f.write(f"--- Language: {lang} ---
")
            for keyword in sorted(list(keywords_set)):
                f.write(f"{keyword}
")
            f.write("\n")
    logging.info(f"All keywords saved to '{keywords_filename}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user. Exiting.")
