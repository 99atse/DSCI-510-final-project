from load_datasets import get_gsw_game_stats_webscrape
import pandas as pd
from config import DATA_DIR, STATS_URL,STATS_HTML,STATS_CSV

def process_game_data(url: str) -> pd.DataFrame:
    stats_df = get_gsw_game_stats_webscrape(STATS_URL,STATS_HTML,STATS_CSV,extract_dir = DATA_DIR)
    