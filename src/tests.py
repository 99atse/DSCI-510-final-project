import os
from load_datasets import get_gsw_articles_api, get_gsw_game_stats_webscrape, get_gsw_sponsor_trends
from config import DATA_DIR, RAW_DATA_DIR, ARTICLES_URL, STATS_URL, STATS_HTML, ARTICLE_JSON, ARTICLE_CSV, STATS_CSV, TEAM
if __name__ == "__main__":
    print("Running tests for Final Project:\n")

    # Create a data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- GSW Articles Data ---
    articles_df = get_gsw_articles_api(ARTICLES_URL, ARTICLE_JSON, ARTICLE_CSV, extract_dir = RAW_DATA_DIR)
    if articles_df is not None:
        print(f"\nGolden State Warriors News Articles Data Head:\n{articles_df.head()}")

    # --- GSW Game Stats Data ---
    stats_df = get_gsw_game_stats_webscrape(STATS_URL, STATS_HTML, STATS_CSV, extract_dir = RAW_DATA_DIR)
    if stats_df is not None:
        print(f"\nGolden State Warriors Game Stats Data Head:\n{stats_df.head()}")

    # --- GSW Sponsor Trends Data ---
    trends_df = get_gsw_sponsor_trends(TEAM,extract_dir = RAW_DATA_DIR)
    if trends_df is not None:
        print(f"\nGolden State Warriors Sponsor Trends Data Head:\n{trends_df.head()}")