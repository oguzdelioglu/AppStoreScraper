import logging
from datetime import datetime
import pandas as pd

from src.itunes_api import get_top_app_ids, get_app_details, get_keyword_suggestions
from src.analysis import extract_keywords_from_text, is_app_considered_new, calculate_keyword_metrics

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

def get_user_input():
    """Gets country and chart selection from the user."""
    country = input("Enter the 2-letter country code for the App Store (e.g., us, tr, gb): ").lower()
    
    print("Select the chart to analyze:")
    print("1: Top Free Apps")
    print("2: Top Paid Apps")
    print("3: Top Grossing Apps")
    
    chart_choice = input("Enter your choice (1-3): ")
    
    chart_map = {
        "1": ("top-free", "Top Free Apps"),
        "2": ("top-paid", "Top Paid Apps"),
        "3": ("top-grossing", "Top Grossing Apps")
    }
    
    chart_id, chart_name = chart_map.get(chart_choice, ("top-free", "Top Free Apps"))
    
    return country, chart_id, chart_name

def main():
    """Main function to run the App Store analysis."""
    # Remove hardcoded input for interactive execution
    # country = "us"
    # chart_id = "top-free"
    # chart_name = "Top Free Apps"

    # Loop through all country codes
    for country_code in COUNTRY_CODES:
        logging.info(f"\n--- Starting analysis for country: {country_code.upper()} ---")
        country = country_code
        chart_id = "top-free" # Defaulting to top-free for all countries for now
        chart_name = "Top Free Apps"
        
        app_ids = get_top_app_ids(country, chart=chart_id)

        if not app_ids:
            logging.error(f"Could not retrieve app list for {country_code.upper()}. Skipping this country.")
            continue

        logging.info(f"List fetched, {len(app_ids)} apps found for {country_code.upper()}. Starting analysis...")

        all_app_data = []
        total_apps = len(app_ids)

        for i, app_id in enumerate(app_ids):
            details = get_app_details(app_id, country)
            if not details:
                logging.warning(f"[{i+1}/{total_apps}] Could not fetch details for app ID {app_id} in {country_code.upper()}. Skipping.")
                continue

            app_name = details.get('trackName', 'N/A')
            logging.info(f"[{i+1}/{total_apps}] Analyzing: {app_name} in {country_code.upper()}")

            # Combine text sources for keyword extraction
            text_for_keywords = f"{details.get('trackName', '')} {details.get('description', '')}"
            keywords = extract_keywords_from_text(text_for_keywords, num_keywords=3)

            # Keyword data
            keyword_data = {}
            all_scored_suggestions = [] # To store dictionaries like {'keyword': '...', 'score': ...}
            
            # Dummy data for calculate_keyword_metrics - replace with real data if available
            # These values are placeholders as iTunes API does not provide them.
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
                
                # Get suggestions for each extracted keyword
                suggestion_result = get_keyword_suggestions(keyword, country, limit=5)
                if suggestion_result and suggestion_result['suggestions']:
                    all_scored_suggestions.extend(suggestion_result['suggestions'])

                # Calculate keyword metrics (using dummy data for now)
                metrics = calculate_keyword_metrics(dummy_metrics_input)
                for metric_name, metric_value in metrics.items():
                    keyword_data[f'Keyword {j+1} {metric_name}'] = metric_value
            
            # Sort all collected suggestions by score and get unique ones
            unique_suggestions_map = {}
            for s in all_scored_suggestions:
                if s['keyword'] not in unique_suggestions_map or s['score'] > unique_suggestions_map[s['keyword']]['score']:
                    unique_suggestions_map[s['keyword']] = s
            
            sorted_unique_suggestions = sorted(unique_suggestions_map.values(), key=lambda x: x['score'], reverse=True)

            # Add unique suggestions to app_data
            for k, suggestion_item in enumerate(sorted_unique_suggestions[:5]): # Limit to top 5 unique suggestions
                keyword_data[f'Suggestion {k+1}'] = suggestion_item['keyword']
                keyword_data[f'Suggestion {k+1} Score'] = suggestion_item['score']

            # Determine app status
            status = "New Discovery" if is_app_considered_new(details.get('releaseDate')) else "Trending"

            app_data = {
                "Rank": i + 1,
                "AppName": app_name,
                "Developer": details.get('artistName', 'N/A'),
                "Category": details.get('primaryGenreName', 'N/A'),
                "Rating": details.get('averageUserRating', 0),
                "RatingCount": details.get('userRatingCount', 0),
                "ReleaseDate": details.get('releaseDate', 'N/A').split('T')[0], # Just the date part
                "Status": status,
                "Price": details.get('formattedPrice', 'N/A'),
                "AppStoreLink": details.get('trackViewUrl', 'N/A'),
                **keyword_data
            }
            all_app_data.append(app_data)

        if not all_app_data:
            logging.error(f"No data was analyzed for {country_code.upper()}. Could not generate a report.")
            continue

        # Create and save the report
        logging.info(f"Analysis complete for {country_code.upper()}. Generating report...")
        df = pd.DataFrame(all_app_data)
        
        # Reorder columns for better readability
        cols_order = ['Rank', 'AppName', 'Status', 'Developer', 'Category', 'Rating', 'RatingCount', 'ReleaseDate', 'Price']
        keyword_cols = [col for col in df.columns if 'Keyword' in col and 'Score' not in col and 'Volume' not in col and 'Competitive' not in col and 'Popularity' not in col and 'Quality' not in col and 'Top_10_Chance' not in col and 'Opportunity_Score' not in col]
        keyword_metric_cols = [col for col in df.columns if 'Keyword' in col and ('Volume' in col or 'Competitive' in col or 'Popularity' in col or 'Quality' in col or 'Top_10_Chance' in col or 'Opportunity_Score' in col)]
        suggestion_cols = [col for col in df.columns if 'Suggestion' in col and 'Score' not in col]
        suggestion_score_cols = [col for col in df.columns if 'Suggestion' in col and 'Score' in col]
        
        final_cols = cols_order + sorted(keyword_cols) + sorted(keyword_metric_cols) + sorted(suggestion_cols) + sorted(suggestion_score_cols) + ['AppStoreLink']
        df = df[final_cols]

        filename = f"AppStore_{chart_name.replace(' ', '_')}_{country.upper()}_{datetime.now().strftime('%Y-%m-%d')}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"Report successfully saved as '{filename}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user. Exiting.")
