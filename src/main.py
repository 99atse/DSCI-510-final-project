import os
from config import DATA_DIR, RESULTS_DIR, ARTICLES_URL, STATS_URL
from load_datasets import get_gsw_sponsor_trends
from process_data import process_game_data, process_article_data, process_trends_data
# from analyze_data import plot_statistics
# from process_data import process_wiki_data

if __name__ == "__main__":
    # Create a data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- GSW Articles Data ---
    articles_df = process_article_data(ARTICLES_URL)
    if articles_df is not None:
        print(f"\nGolden State Warriors News Articles Cleaned Data Head:\n{articles_df.head()}")
    #     plot_statistics(articles_df,'Articles',result_dir = RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")

    # --- GSW Game Stats Data ---
    stats_df = process_game_data(STATS_URL)
    if stats_df is not None:
        print(f"\nGolden State Warriors Game Stats Cleaned Data Head:\n{stats_df.head()}")
    #     plot_statistics(stats_df,'Season Stats',result_dir = RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")

    # # --- GSW Sponsor Trends Data ---
    # keyword = 'United Airlines'
    # trends_df = get_gsw_sponsor_trends(keyword)
    # trends_df = process_trends_data('Rakuten')
    # if trends_df is not None:
    #     print(f"\nGolden State Warriors Sponsor Trends Data Head:\n{trends_df.head()}")
    #     # plot_statistics(trends_df,f'{keyword} Trends',result_dir = RESULTS_DIR)
