# project configuration
DATA_DIR = "data"
CLEANED_DATA_DIR = "data/cleaned"
RAW_DATA_DIR = "data/raw"

RESULTS_DIR = "results"
ARTICLES_RESULTS_DIR = "results/articles"
STATS_RESULTS_DIR = "results/stats"
TRENDS_RESULTS_DIR = "results/trends"
ALL_RESULTS_DIR = "results/all"

START_DATE = "2020-12-22"
END_DATE = "2025-04-13"
SEASON_TIME_RANGES = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]


# data sources configuration
ARTICLES_URL = 'https://www.nba.com/warriors/api/content/category/news?page={}'
STATS_URL = "https://www.espn.com/nba/team/schedule/_/name/gs/season/{}"

# --- GSW Articles Data ---
ARTICLE_JSON = 'GoldenStateWarriors_Articles.json'
ARTICLE_CSV = 'GoldenStateWarriors_Articles.csv'
CLEANED_ARTICLE_CSV = "GoldenStateWarriors_Articles_Cleaned.csv"
ALL_ARTICLES_PLOT = '2021-2025_GSW_Article_Plot.png'
SEASON_ARTICLES_PLOT = ['2021_GSW_Article_Plot.png','2022_GSW_Article_Plot.png','2023_GSW_Article_Plot.png','2024_GSW_Article_Plot.png','2025_GSW_Article_Plot.png']

# --- GSW Game Stats Data ---
STATS_HTML = "GoldenStateWarriors_Stats.html"
STATS_CSV = "GoldenStateWarriors_Stats.csv"
CLEANED_STATS_CSV = "GoldenStateWarriors_Stats_Cleaned.csv"
ALL_STATS_PLOT = '2021-2025_GSW_Stats_Plot.png'
SEASON_STATS_PLOT = ['2021_GSW_Stats_Plot.png','2022_GSW_Stats_Plot.png','2023_GSW_Stats_Plot.png','2024_GSW_Stats_Plot.png','2025_GSW_Stats_Plot.png']

# --- GSW Sponsor Trends Data ---
TEAM_AND_SPONSORS = ['Golden State Warriors','Rakuten','United Airlines','JPMorgan Chase']
TEAM = 'Golden State Warriors'
SPONSORS = ['Rakuten','United Airlines','Chase']
FORMATTED_SPONSORS = ['Rakuten','UnitedAirlines','Chase']
TREND_START_DATE = '2020-12-01'
TREND_END_DATE = '2025-4-30'

GSW_DRIVE_CSV='https://drive.google.com/file/d/1drZDsBeIfyDkvmKnmJgcTiieLIWqLpGo/view?usp=drive_link'
CHASE_DRIVE_CSV = 'https://drive.google.com/file/d/1MY3d2EDP2q9TmZtGrEg8M7BnPaO_CP4Q/view?usp=drive_link'
RAKUTEN_DRIVE_CSV = 'https://drive.google.com/file/d/1RFxTd88-adlohZQ6bH0gWoJdnlQ0e_lT/view?usp=drive_link'
UNITED_DRIVE_CSV = 'https://drive.google.com/file/d/1isX0J90Sx-oBwh8A-1S3EPKUBc6Mt0bk/view?usp=drive_link'

ALL_TRENDS_CSV = 'All_Trends_Cleaned.csv'
ALL_SEASONS_DATA_CSV = '2021-2025_GSW_Data.csv'
SEASON_DATA_CSV = ['2021_GSW_Data.csv','2022_GSW_Data.csv','2023_GSW_Data.csv','2024_GSW_Data.csv','2025_GSW_Data.csv']

GSW_TREND_CSV ='GoldenStateWarriors_Trends.csv'
RAKUTEN_TREND_CSV = 'Rakuten_Trends.csv'
UNITED_TREND_CSV = 'UnitedAirlines_Trends.csv'
CHASE_TREND_CSV = 'JPMorganChase_Trends.csv'

GSW_CLEANED_TREND_CSV ='GoldenStateWarriors_Trends_Cleaned.csv'
RAKUTEN_CLEANED_TREND_CSV = 'Rakuten_Trends_Cleaned.csv'
UNITED_CLEANED_TREND_CSV = 'UnitedAirlines_Trends_Cleaned.csv'
CHASE_CLEANED_TREND_CSV = 'JPMorganChase_Trends_Cleaned.csv'

# --- Line/Scatter Plot File Names ---
ALL_DATA_PLOT = ['2021-2025_Rakuten_GSW_Data_Plot.png','2021-2025_UnitedAirlines_GSW_Data_Plot.png','2021-2025_Chase_GSW_Data_Plot.png']
ALL_SEASON_DATA_PLOT = [('2021_GSW_All_Data_Rakuten_Plot.png','2022_GSW_All_Data_Rakuten_Plot.png','2023_GSW_All_Data_Rakuten_Plot.png','2024_GSW_All_Data_Rakuten_Plot.png','2025_GSW_All_Data_Rakuten_Plot.png'),
                            ('2021_GSW_All_Data_UnitedAirlines_Plot.png','2022_GSW_All_Data_UnitedAirlines_Plot.png','2023_GSW_All_Data_UnitedAirlines_Plot.png','2024_GSW_All_Data_UnitedAirlines_Plot.png','2025_GSW_All_Data_UnitedAirlines_Plot.png'),
                            ('2021_GSW_All_Data_Chase_Plot.png','2022_GSW_All_Data_Chase_Plot.png','2023_GSW_All_Data_Chase_Plot.png','2024_GSW_All_Data_Chase_Plot.png','2025_GSW_All_Data_Chase_Plot.png')]
ALL_TRENDS_PLOT = ['2021-2025_Rakuten_Sponsor_Trends_Plot.png','2021-2025_UnitedAirlines_Sponsor_Trends_Plot.png','2021-2025_JPMorganChase_Sponsor_Trends_Plot.png']
ALL_SEASON_TRENDS_PLOT = [('2021_Rakuten_Sponsor_Trends_Plot.png','2022_Rakuten_Sponsor_Trends_Plot.png','2023_Rakuten_Sponsor_Trends_Plot.png','2024_Rakuten_Sponsor_Trends_Plot.png','2025_Rakuten_Sponsor_Trends_Plot.png'),
                          ('2021_UnitedAirlines_Sponsor_Trends_Plot.png','2022_UnitedAirlines_Sponsor_Trends_Plot.png','2023_UnitedAirlines_Sponsor_Trends_Plot.png','2024_UnitedAirlines_Sponsor_Trends_Plot.png','2025_UnitedAirlines_Sponsor_Trends_Plot.png'),
                          ('2021_JPMorganChase_Sponsor_Trends_Plot.png','2022_JPMorganChase_Sponsor_Trends_Plot.png','2023_JPMorganChase_Sponsor_Trends_Plot.png','2024_JPMorganChase_Sponsor_Trends_Plot.png','2025_JPMorganChase_Sponsor_Trends_Plot.png')]

# --- Correlation Matrices File Names ---
ALL_DATA_MATRIX = 'GSW_All_Data_Correlation_Matrix_Plot.png'
ADJUSTED_ALL_DATA_MATRIX ='Adjusted_GSW_All_Data_Correlation_Matrix_Plot.png'
CURRY_MATRIX = 'GSW_Curry_Correlation_Matrix_Plot.png'
ADJUSTED_CURRY_MATRIX = 'Adjusted_GSW_Curry_Correlation_Matrix_Plot.png'
CURRY_WIN_MATRIX = 'GSW_Curry_Win_Correlation_Matrix_Plot.png'
ADJUSTED_CURRY_WIN_MATRIX = 'Adjusted_GSW_Curry_Win_Correlation_Matrix_Plot.png'
SPONSOR_MATRIX = 'GSW_Sponsor_Count_Correlation_Matrix_Plot.png'
ADJUSTED_SPONSOR_MATRIX = 'Adjusted_GSW_Sponsor_Count_Correlation_Matrix_Plot.png'