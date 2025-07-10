import logging
import os
from datetime import datetime
import pandas as pd
import concurrent.futures

from src.itunes_api import get_top_app_ids, get_keyword_suggestions, fetch_proxies_from_url
from src.analysis import extract_keywords_from_text, is_app_considered_new, calculate_keyword_metrics
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

def process_app(app_data, country, rank):
    # app_id = app_data.get('id') # Not needed as app_data is already the full data
    if not app_data:
        logging.warning(f"Could not process app data for rank {rank} in {country}. Skipping.")
        return None

    app_name = app_data.get('name', 'N/A') # Use 'name' from RSS feed
    logging.info(f"Analyzing: {app_name} in {country}")

    # Combine relevant text sources for keyword extraction from RSS feed data
    text_for_keywords = f"{app_data.get('name', '')} {app_data.get('artistName', '')} {app_data.get('genres', [{}])[0].get('name', '')}"
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
        suggestion_result = get_keyword_suggestions(keyword, country, limit=5)
        if suggestion_result and suggestion_result['suggestions']:
            all_scored_suggestions.extend(suggestion_result['suggestions'])

        metrics = calculate_keyword_metrics(dummy_metrics_input)
        for metric_name, metric_value in metrics.items():
            keyword_data[f'Keyword {j+1} {metric_name}'] = metric_value

    unique_suggestions_map = {}
    for s in all_scored_suggestions:
        if s['keyword'] not in unique_suggestions_map or s['score'] > unique_suggestions_map[s['keyword']]['score']:
            unique_suggestions_map[s['keyword']] = s

    sorted_unique_suggestions = sorted(unique_suggestions_map.values(), key=lambda x: x['score'], reverse=True)

    for k, suggestion_item in enumerate(sorted_unique_suggestions[:5]):
        keyword_data[f'Suggestion {k+1}'] = suggestion_item['keyword']
        keyword_data[f'Suggestion {k+1} Score'] = suggestion_item['score']

    status = "New Discovery" if is_app_considered_new(app_data.get('releaseDate')) else "Trending"

    return {
        "Rank": rank,
        "AppName": app_name,
        "Developer": app_data.get('artistName', 'N/A'),
        "Category": app_data.get('genres', [{}])[0].get('name', 'N/A'),
        "Rating": app_data.get('averageUserRating', 0), # Note: averageUserRating and userRatingCount are not directly available in RSS feed, will be 0
        "RatingCount": app_data.get('userRatingCount', 0), # Note: averageUserRating and userRatingCount are not directly available in RSS feed, will be 0
        "ReleaseDate": app_data.get('releaseDate', 'N/A').split('T')[0],
        "Status": status,
        "Price": app_data.get('formattedPrice', 'N/A'),
        "AppStoreLink": app_data.get('url', 'N/A'), # Use 'url' from RSS feed
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

    for country_code in countries_to_analyze:
        logging.info(f"\n--- Starting analysis for country: {country_code.upper()} ---")
        country = country_code
        chart_id = "top-free"
        chart_name = "Top Free Apps"

        app_data_list = get_top_app_ids(country, chart=chart_id)

        if not app_data_list:
            logging.error(f"Could not retrieve app list for {country_code.upper()}. Skipping this country.")
            continue

        logging.info(f"List fetched, {len(app_data_list)} apps found for {country_code.upper()}. Starting analysis...")

        all_app_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_app = {executor.submit(process_app, app_data, country, i + 1): app_data for i, app_data in enumerate(app_data_list)}
            for future in concurrent.futures.as_completed(future_to_app):
                app_data = future.result()
                if app_data:
                    all_app_data.append(app_data)

        if not all_app_data:
            logging.error(f"No data was analyzed for {country_code.upper()}. Could not generate a report.")
            continue

        logging.info(f"Analysis complete for {country_code.upper()}. Generating report...")
        df = pd.DataFrame(all_app_data)

        cols_order = ['Rank', 'AppName', 'Status', 'Developer', 'Category', 'Rating', 'RatingCount', 'ReleaseDate', 'Price']
        keyword_cols = [col for col in df.columns if 'Keyword' in col and 'Score' not in col and 'Volume' not in col and 'Competitive' not in col and 'Popularity' not in col and 'Quality' not in col and 'Top_10_Chance' not in col and 'Opportunity_Score' not in col]
        keyword_metric_cols = [col for col in df.columns if 'Keyword' in col and ('Volume' in col or 'Competitive' in col or 'Popularity' in col or 'Quality' in col or 'Top_10_Chance' in col or 'Opportunity_Score' in col)]
        suggestion_cols = [col for col in df.columns if 'Suggestion' in col and 'Score' not in col]
        suggestion_score_cols = [col for col in df.columns if 'Suggestion' in col and 'Score' in col]

        final_cols = cols_order + sorted(keyword_cols) + sorted(keyword_metric_cols) + sorted(suggestion_cols) + sorted(suggestion_score_cols) + ['AppStoreLink']
        df = df[final_cols]

        output_dir = f"outputs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/AppStore_{chart_name.replace(' ', '_')}_{country.upper()}_{datetime.now().strftime('%Y-%m-%d')}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"Report successfully saved as '{filename}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user. Exiting.")
