from load_datasets import get_dubs_articles_api, get_dubs_game_stats_webscrape, get_dubs_sponsor_trends

if __name__ == "__main__":
    print("Running tests for Final Project:\n")

    # --- Dubs Articles Data ---
    api_url = 'https://www.nba.com/warriors/api/content/category/news?page={}'
    json_file = 'dubs_articles.json'
    dataset_file = 'dubs_articles.csv'
    
    articles_df = get_dubs_articles_api(api_url, json_file, dataset_file)
    if articles_df is not None:
        print(f"\nWarriors News Articles Data Head:\n{articles_df.head()}")

    # --- Dubs Game Stats Data ---
    webscrape_url = "https://www.espn.com/nba/team/schedule/_/name/gs/season/{}"
    html_file = "dubs_stats.html"
    stats_file = "warriors_schedule_2021_2026.csv"
    start_year = 2021
    end_year = 2026
    
    stats_df = get_dubs_game_stats_webscrape(webscrape_url,html_file,stats_file,start_year,end_year)
    if stats_df is not None:
        print(f"\nWarriors Game Stats Data Head:\n{stats_df.head()}")

    # --- Dubs Sponsor Trends Data ---
    keyword = ['Golden State Warriors']
    trends_df = get_dubs_sponsor_trends(keyword)
    if trends_df is not None:
        print(f"\nWarriors Sponsor Trends Data Head:\n{trends_df.head()}")

