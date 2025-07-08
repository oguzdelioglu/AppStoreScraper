# App Store Opportunity Analysis Tool

This project is a command-line tool designed to analyze the App Store's top charts to identify trends and potential opportunities for new applications. It fetches real-time data, analyzes it for new and trending apps, extracts potential keywords, and estimates their competitive landscape.

## Features

- **Real-time Top Chart Analysis:** Fetches data directly from the App Store for up-to-the-minute insights.
- **Trend & New Discovery:** Identifies apps that are new to the charts or have been trending.
- **Keyword Extraction:** Automatically suggests potential keywords based on app names and descriptions.
- **Competition Estimation:** Measures how many other apps are competing for a specific keyword.
- **CSV Reports:** Exports all findings into a clean, easy-to-read CSV file.

## How to Use

### 1. Installation

First, ensure you have Python 3 installed. Then, clone the repository and install the necessary dependencies:

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/oguzdelioglu/AppStoreScraper.git
cd AppStoreScraper

# Install required Python libraries
pip install -r requirements.txt
```

### 2. Running the Tool

Execute the main script from the project's root directory:

```bash
python main.py
```

The script will then prompt you to enter:
1.  The **2-letter country code** for the App Store you want to analyze (e.g., `us`, `tr`, `gb`).
2.  The **chart** you wish to analyze (e.g., Top Free, Top Paid).

### 3. Output

Once the analysis is complete, the tool will generate a CSV file in the project directory. The filename will be in the format `AppStore_[ChartName]_[Country]_[Date].csv` (e.g., `AppStore_Top_Free_Apps_US_2025-07-09.csv`).

This file can be opened with any spreadsheet software (like Excel, Google Sheets, or Numbers) for further analysis.
