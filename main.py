import logging
import os
from datetime import datetime
import pandas as pd
import concurrent.futures

from src.itunes_api import get_keyword_suggestions, fetch_proxies_from_url # Keep get_keyword_suggestions for now, will remove later if not needed
from src.analysis import extract_keywords_from_text, is_app_considered_new, calculate_keyword_metrics
from src.sitemap_parser import get_all_app_urls_from_sitemaps
from config import USE_PROXY, PROXY_LIST, PROXY_URL, ONLY_POPULAR_COUNTRIES, POPULAR_COUNTRIES

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

def process_app_for_keywords(app_entry, country):
    # For sitemap data, we don't have direct access to trackName, description, etc.
    # We will use the app_id to fetch details if needed, or rely on sitemap data.
    # For now, we'll just use the app_id as a placeholder for analysis.
    app_id = app_entry.get('app_id')
    app_url = app_entry.get('url')

    # In a real scenario, you would fetch app details from a reliable source
    # using the app_id or scrape the app_url for description and other metadata.
    # For this example, we'll simulate some data.
    app_name = f"App {app_id}"
    developer = "Unknown Developer"
    category = "Unknown Category"
    release_date = "2023-01-01"
    price = "Free"

    logging.info(f"Analyzing: {app_name} (ID: {app_id}) in {country})")

    # Simulate text for keywords (in a real scenario, this would come from app description)
    text_for_keywords = f"{app_name} {developer} {category} best new app free download"
    keywords = extract_keywords_from_text(text_for_keywords, country, num_keywords=3)

    keyword_data = {}
    all_scored_suggestions = []

    dummy_metrics_input = {
        "autocomplete_rank": 5,
        "competing_apps": 1000,
        "avg_top10_downloads": 5000,
        "avg_top10_rating": 4.0,
        "avg_top10_reviews": 1000,
        "ads_popularity_score": 70,
        "title_keyword_flag": True,
        "autocomplete_trend_7d": 1
    }

    for j, keyword in enumerate(keywords):
        keyword_data[f'Keyword {j+1}'] = keyword
        # We are no longer using get_keyword_suggestions from iTunes API for this phase
        # suggestion_result = get_keyword_suggestions(keyword, country, limit=5)
        # if suggestion_result and suggestion_result['suggestions']:
        #     all_scored_suggestions.extend(suggestion_result['suggestions'])

        metrics = calculate_keyword_metrics(dummy_metrics_input)
        for metric_name, metric_value in metrics.items():
            keyword_data[f'Keyword {j+1} {metric_name}'] = metric_value

    # For now, without get_keyword_suggestions, all_scored_suggestions will be empty
    # We can add dummy suggestions or remove this part if not relevant without API
    # For demonstration, let's add some dummy suggestions based on extracted keywords
    for k, keyword in enumerate(keywords):
        keyword_data[f'Suggestion {k+1}'] = keyword + "_suggest"
        keyword_data[f'Suggestion {k+1} Score'] = random.randint(50, 100)

    status = "Unknown"

    return {
        "AppID": app_id,
        "AppURL": app_url,
        "AppName": app_name,
        "Developer": developer,
        "Category": category,
        "Rating": 0, # Not available from sitemap
        "RatingCount": 0, # Not available from sitemap
        "ReleaseDate": release_date,
        "Status": status,
        "Price": price,
        "AppStoreLink": app_url,
        **keyword_data
    }

def main():
    """Main function to run the App Store analysis."""
    if USE_PROXY and PROXY_URL:
        logging.info(f"Fetching proxies from {PROXY_URL}...")
        fetched_proxies = fetch_proxies_from_url(PROXY_URL)
        if fetched_proxies:
            PROXY_LIST.clear()
            PROXY_LIST.extend(fetched_proxies)
            logging.info(f"Updated PROXY_LIST with {len(PROXY_LIST)} proxies.")
        else:
            logging.warning("Could not fetch proxies. Continuing without proxies.")

    countries_to_analyze = POPULAR_COUNTRIES if ONLY_POPULAR_COUNTRIES else COUNTRY_CODES

    current_run_output_dir = f"outputs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(current_run_output_dir, exist_ok=True)

    all_app_urls = get_all_app_urls_from_sitemaps(MAIN_SITEMAP_URL)

    if not all_app_urls:
        logging.error("Could not retrieve any app URLs from sitemaps. Exiting.")
        return

    logging.info(f"Found {len(all_app_urls)} app URLs from sitemaps. Starting analysis...")

    # Filter app_urls by country if ONLY_POPULAR_COUNTRIES is True
    filtered_app_urls = []
    if ONLY_POPULAR_COUNTRIES:
        for app_entry in all_app_urls:
            # Check if any hreflang matches a popular country
            for hreflang_entry in app_entry.get('hreflangs', []):
                lang_country = hreflang_entry['hreflang'].split('-')
                if len(lang_country) == 2 and lang_country[1].lower() in countries_to_analyze:
                    filtered_app_urls.append(app_entry)
                    break # Found a match, move to next app_entry
        logging.info(f"Filtered to {len(filtered_app_urls)} apps for popular countries.")
    else:
        filtered_app_urls = all_app_urls

    # Process keywords for each app (simulated for now)
    all_app_data_with_keywords = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Pass country to process_app_for_keywords for language-specific stopword filtering
        future_to_app = {executor.submit(process_app_for_keywords, app_entry, app_entry.get('hreflangs', [{}])[0].get('hreflang', 'en-us').split('-')[1].lower()): app_entry for app_entry in filtered_app_urls}
        for future in concurrent.futures.as_completed(future_to_app):
            app_data_with_keywords = future.result()
            if app_data_with_keywords:
                all_app_data_with_keywords.append(app_data_with_keywords)

    if not all_app_data_with_keywords:
        logging.error(f"No keyword data was analyzed. Could not generate a report.")
        return

    logging.info(f"Analysis complete. Generating report...")
    df = pd.DataFrame(all_app_data_with_keywords)

    cols_order = ['AppID', 'AppURL', 'AppName', 'Developer', 'Category', 'Rating', 'RatingCount', 'ReleaseDate', 'Price', 'Status']
    keyword_cols = [col for col in df.columns if 'Keyword' in col and 'Score' not in col and 'Volume' not in col and 'Competitive' not in col and 'Popularity' not in col and 'Quality' not in col and 'Top_10_Chance' not in col and 'Opportunity_Score' not in col]
    keyword_metric_cols = [col for col in df.columns if 'Keyword' in col and ('Volume' in col or 'Competitive' in col or 'Popularity' in col or 'Quality' in col or 'Top_10_Chance' in col or 'Opportunity_Score' in col)]
    suggestion_cols = [col for col in df.columns if 'Suggestion' in col and 'Score' not in col]
    suggestion_score_cols = [col for col in df.columns if 'Suggestion' in col and 'Score' in col]

    final_cols = cols_order + sorted(keyword_cols) + sorted(keyword_metric_cols) + sorted(suggestion_cols) + sorted(suggestion_score_cols) + ['AppStoreLink']
    df = df[final_cols]

    filename = f"{current_run_output_dir}/AppStore_Sitemap_Analysis_{datetime.now().strftime('%Y-%m-%d')}.csv"
    df.to_csv(filename, index=False)
    logging.info(f"Report successfully saved as '{filename}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user. Exiting.")