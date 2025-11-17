import os
from config import DATA_DIR, RESULTS_DIR, ARTICLES_URL, STATS_URL, ARTICLE_CSV,ARTICLE_JSON,STATS_HTML,STATS_CSV
from load_datasets import get_gsw_articles_api, get_gsw_game_stats_webscrape, get_gsw_sponsor_trends
# from analyze_data import plot_statistics
# from process_data import process_wiki_data

if __name__ == "__main__":
    # Create a data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- GSW Articles Data ---
    api_url = 'https://www.nba.com/warriors/api/content/category/news?page={}'
    json_file = 'GoldenStateWarriors_Articles.json'
    dataset_file = 'GoldenStateWarriors_Articles.csv'
    
    articles_df = get_gsw_articles_api(ARTICLES_URL, ARTICLE_JSON, ARTICLE_CSV, extract_dir = DATA_DIR)
    if articles_df is not None:
        print(f"\nGolden State Warriors News Articles Data Head:\n{articles_df.head()}")
    #     plot_statistics(articles_df,'Articles',result_dir = RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")

    # --- GSW Game Stats Data ---
    stats_df = get_gsw_game_stats_webscrape(STATS_URL,STATS_HTML,STATS_CSV,extract_dir = DATA_DIR)
    if stats_df is not None:
        print(f"\nGolden State Warriors Game Stats Data Head:\n{stats_df.head()}")
    #     plot_statistics(stats_df,'Season Stats',result_dir = RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")

    # --- GSW Sponsor Trends Data ---
    # keyword = ['Golden State Warriors']
    # trends_df = get_gsw_sponsor_trends(keyword)
    # if trends_df is not None:
    #     print(f"\nGolden State Warriors Sponsor Trends Data Head:\n{trends_df.head()}")
    #     plot_statistics(trends_df,f'{keyword} Trends',result_dir = RESULTS_DIR)
    
    # # --- Wikipedia Scraped Data ---
    # # We'll scrape a table of the largest companies
    # # process data firsts
    # plot_df = process_wiki_data(WIKI_LARGEST_COMPANIES)
