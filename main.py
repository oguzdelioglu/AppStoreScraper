import logging
from datetime import datetime
import pandas as pd

from src.itunes_api import get_top_app_ids, get_app_details, get_search_result_count
from src.analysis import extract_keywords_from_text, is_app_considered_new

# Configure logging
logging.basicConfig(level=logging.INFO, format='> %(message)s')

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
    country, chart_id, chart_name = get_user_input()
    
    app_ids = get_top_app_ids(country, chart=chart_id, limit=100) # Limit to top 100 for reasonable performance
    
    if not app_ids:
        logging.error("Could not retrieve app list. Exiting.")
        return

    all_app_data = []
    total_apps = len(app_ids)

    for i, app_id in enumerate(app_ids):
        details = get_app_details(app_id, country)
        if not details:
            logging.warning(f"[{i+1}/{total_apps}] Could not fetch details for app ID {app_id}. Skipping.")
            continue

        app_name = details.get('trackName', 'N/A')
        logging.info(f"[{i+1}/{total_apps}] Analyzing: {app_name}")

        # Combine text sources for keyword extraction
        text_for_keywords = f"{details.get('trackName', '')} {details.get('description', '')}"
        keywords = extract_keywords_from_text(text_for_keywords, num_keywords=3)

        # Analyze competition for each keyword
        keyword_data = {}
        for j, keyword in enumerate(keywords):
            competition = get_search_result_count(keyword, country)
            keyword_data[f'Keyword {j+1}'] = keyword
            keyword_data[f'Competition {j+1}'] = competition

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
        logging.error("No data was analyzed. Could not generate a report.")
        return

    # Create and save the report
    logging.info("Analysis complete. Generating report...")
    df = pd.DataFrame(all_app_data)
    
    # Reorder columns for better readability
    cols_order = ['Rank', 'AppName', 'Status', 'Developer', 'Category', 'Rating', 'RatingCount', 'ReleaseDate', 'Price']
    keyword_cols = [col for col in df.columns if 'Keyword' in col or 'Competition' in col]
    final_cols = cols_order + sorted(keyword_cols) + ['AppStoreLink']
    df = df[final_cols]

    filename = f"AppStore_{chart_name.replace(' ', '_')}_{country.upper()}_{datetime.now().strftime('%Y-%m-%d')}.csv"
    df.to_csv(filename, index=False)
    logging.info(f"Report successfully saved as '{filename}'")

if __name__ == "__main__":
    main()
