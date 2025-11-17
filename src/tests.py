from load_datasets import get_gsw_articles_api, get_gsw_game_stats_webscrape, get_gsw_sponsor_trends

if __name__ == "__main__":
    print("Running tests for Final Project:\n")

    # --- GSW Articles Data ---
    api_url = 'https://www.nba.com/warriors/api/content/category/news?page={}'
    json_file = 'GoldenStateWarriors_Articles.json'
    dataset_file = 'GoldenStateWarriors_Articles.csv'
    
    articles_df = get_gsw_articles_api(api_url, json_file, dataset_file)
    if articles_df is not None:
        print(f"\nGolden State Warriors News Articles Data Head:\n{articles_df.head()}")

    # --- GSW Game Stats Data ---
    webscrape_url = "https://www.espn.com/nba/team/schedule/_/name/gs/season/{}"
    html_file = "GoldenStateWarriors_Stats.html"
    stats_file = "GoldenStateWarriors_Stats.csv"
    
    stats_df = get_gsw_game_stats_webscrape(webscrape_url,html_file,stats_file)
    if stats_df is not None:
        print(f"\nGolden State Warriors Game Stats Data Head:\n{stats_df.head()}")

    # --- GSW Sponsor Trends Data ---
    keyword = 'United Airlines'
    trends_df = get_gsw_sponsor_trends(keyword)
    if trends_df is not None:
        print(f"\nGolden State Warriors Sponsor Trends Data Head:\n{trends_df.head()}")