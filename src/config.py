# project configuration
DATA_DIR = "data"
RESULTS_DIR = "results"

# data sources configuration
ARTICLES_URL = 'https://www.nba.com/warriors/api/content/category/news?page={}'
STATS_URL = "https://www.espn.com/nba/team/schedule/_/name/gs/season/{}"

# --- GSW Articles Data ---
ARTICLE_JSON = 'GoldenStateWarriors_Articles.json'
ARTICLE_CSV = 'GoldenStateWarriors_Articles.csv'
CLEANED_ARTICLE_CSV = "GoldenStateWarriors_Articles_Cleaned.csv"

# --- GSW Game Stats Data ---
STATS_HTML = "GoldenStateWarriors_Stats.html"
STATS_CSV = "GoldenStateWarriors_Stats.csv"
CLEANED_STATS_CSV = "GoldenStateWarriors_Stats_Cleaned.csv"

# --- GSW Sponsor Trends Data ---
TEAM_AND_SPONSORS = ['Golden State Warriors','Rakuten','United Airlines','JPMorgan Chase']
ALL_TRENDS_CSV = 'data/cleaned/All_Trends_Cleaned.csv'
GSW_TREND_CSV='https://drive.google.com/file/d/1drZDsBeIfyDkvmKnmJgcTiieLIWqLpGo/view?usp=drive_link'
CHASE_TREND_CSV = 'https://drive.google.com/file/d/1MY3d2EDP2q9TmZtGrEg8M7BnPaO_CP4Q/view?usp=drive_link'
RAKUTEN_TREND_CSV = 'https://drive.google.com/file/d/1RFxTd88-adlohZQ6bH0gWoJdnlQ0e_lT/view?usp=drive_link'
UNITED_TREND_CSV = 'https://drive.google.com/file/d/1isX0J90Sx-oBwh8A-1S3EPKUBc6Mt0bk/view?usp=drive_link'