import os
from config import (DATA_DIR, CLEANED_DATA_DIR, ARTICLES_RESULTS_DIR, STATS_RESULTS_DIR, TRENDS_RESULTS_DIR, ALL_RESULTS_DIR, 
                    ARTICLES_URL, STATS_URL, TEAM_AND_SPONSORS, ALL_TRENDS_CSV)
from process_data import process_game_data, process_article_data, process_trends_data, combine_all_data
from analyze_data import plot_all_trends, plot_gsw_stats, plot_articles, plot_all_data

if __name__ == "__main__":
    # Create a data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- GSW Articles Data ---
    articles_df = process_article_data(ARTICLES_URL)
    if articles_df is not None:
        print(f"\nGolden State Warriors News Articles Cleaned Data Head:\n{articles_df.head()}")
        plot_articles(articles_df,result_dir = ARTICLES_RESULTS_DIR)
    print("\n" + "=" * 50 + "\n")

    # --- GSW Game Stats Data ---
    stats_df = process_game_data(STATS_URL)
    if stats_df is not None:
        print(f"\nGolden State Warriors Game Stats Cleaned Data Head:\n{stats_df.head()}")
        plot_gsw_stats(stats_df,result_dir = STATS_RESULTS_DIR)
    print("\n" + "=" * 50 + "\n")

    # --- GSW Sponsor Trends Data ---
    for keyword in TEAM_AND_SPONSORS:
        trends_df = process_trends_data(keyword,retrieve_api=False,all_sponsors=True)
        if trends_df is not None:
            print(f"\n {keyword} Trends Data Head:\n{trends_df.head()}")
    plot_all_trends(f'{CLEANED_DATA_DIR}/{ALL_TRENDS_CSV}',result_dir = TRENDS_RESULTS_DIR)
    print("\n" + "=" * 50 + "\n")

    # --- All GSW Data ---
    all_df = combine_all_data(stats_df,articles_df,f'{CLEANED_DATA_DIR}/{ALL_TRENDS_CSV}')
    if all_df is not None:
        print(f"\nGolden State Warriors Combined and Cleaned Data Head:\n{all_df.head()}")
    plot_all_data(all_df,result_dir=ALL_RESULTS_DIR)