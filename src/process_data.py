import re
import os
import pandas as pd
import numpy as np

from config import DATA_DIR, STATS_HTML,STATS_CSV,CLEANED_STATS_CSV, ARTICLE_JSON, ARTICLE_CSV, CLEANED_ARTICLE_CSV
from load_datasets import get_gsw_game_stats_webscrape, get_gsw_articles_api

def process_game_data(url: str) -> pd.DataFrame:
    stats_df = get_gsw_game_stats_webscrape(url,STATS_HTML,STATS_CSV,extract_dir = DATA_DIR)

    # path to place files into data folder
    cleaned_csv_path = os.path.join(DATA_DIR, CLEANED_STATS_CSV)

    before_new_year = stats_df['Date'].str.contains(r'Sep|Oct|Nov|Dec')
    stats_df['Year'] =  stats_df['Season'].astype(int)
    stats_df.loc[before_new_year,'Year'] = stats_df['Season'].astype(int) - 1

    stats_df['Date'] = pd.to_datetime(stats_df['Date'] + ' ' + stats_df['Year'].astype(str),format="%a, %b %d %Y")

    # create new column to designate home/away games based on Opponent Column
    # remove '@ ' and 'vs ' from Opponent Column
    stats_df['Home_Away'] = np.where(stats_df['Opponent'].str.startswith('@ '),'away', np.where(stats_df['Opponent'].str.startswith('vs '),'home', 'unknown'))
    stats_df['Opponent'] = stats_df['Opponent'].replace(r'^(?:@ |vs )', '', regex=True)

    # create new column to designate wins/losses
    # split scores by GSW and Opponent into separate columns
    stats_df['Win'] = np.where(stats_df['Result'].str.startswith('W'), 1, 0)
    stats_df['Overtime'] = np.where(stats_df['Result'].str.endswith('OT'), 1, 0)
    stats_df['Result'] = stats_df['Result'].str.replace(r'\s\d*OT$', '', regex=True)
    stats_df[['wins', 'losses']] = stats_df['Record'].str.split('-', expand=True).astype(int)
    stats_df[['Team_Score', 'Opp_Score']] = stats_df['Result'].str[2:].str.split('-', expand=True).astype(int)

    stats_df[['Hi_Points_Player', 'Hi_Points_Value']] = stats_df['Hi Points'].str.rsplit(' ', n=1, expand=True)
    stats_df[['Hi_Rebounds_Player', 'Hi_Rebounds_Value']] = stats_df['Hi Rebounds'].str.rsplit(' ', n=1, expand=True)
    stats_df[['Hi_Assists_Player', 'Hi_Assists_Value']] = stats_df['Hi Assists'].str.rsplit(' ', n=1, expand=True)
    stats_df['Hi_Points_Value'] = stats_df['Hi_Points_Value'].astype(int)
    stats_df['Hi_Rebounds_Value'] = stats_df['Hi_Rebounds_Value'].astype(int)
    stats_df['Hi_Assists_Value'] = stats_df['Hi_Assists_Value'].astype(int)

    stats_df = stats_df.drop(columns=['Hi Points', 'Hi Rebounds', 'Hi Assists', 'Result', 'Record','Year'])

    try:  
        # save cleaned data to csv
        stats_df.to_csv(cleaned_csv_path, index=False)

        return stats_df
    except Exception as e:
        print(f"Error saving GSW stats data to CSV file: {e}")
        return None

def extract_sponsors(text):

    sponsors = re.findall(r'presented by ([^.,;]+)', text, flags=re.IGNORECASE)

    return [sponsor.strip() for sponsor in sponsors]
  
def process_article_data(url: str) -> pd.DataFrame:
    articles_df = get_gsw_articles_api(url,ARTICLE_JSON,ARTICLE_CSV,extract_dir = DATA_DIR)

    # path to place files into data folder
    cleaned_csv_path = os.path.join(DATA_DIR, CLEANED_ARTICLE_CSV)

    articles_df['Date'] = pd.to_datetime(articles_df['Date']).dt.tz_convert(None)
    start_date = pd.to_datetime("2020-11-01")
    end_date   = pd.to_datetime("2025-10-31")

    articles_df = articles_df[(articles_df['Date'] >= start_date) & (articles_df['Date'] <= end_date)]

    major_sponsors = ['Rakuten','United Airlines','Chase','Kaiser Permanente','Adobe']
    for sponsor in major_sponsors:
        sponsor_no_spaces = sponsor.replace(" ","")
        articles_df[f'{sponsor_no_spaces}_Title'] = articles_df['Title'].str.contains(sponsor, case=False, na=False)
        articles_df[f'{sponsor_no_spaces}_Description'] = articles_df['Excerpt'].str.contains(sponsor, case=False, na=False)
        articles_df[f'{sponsor_no_spaces}_Count'] = articles_df['Title'].str.count(sponsor, flags=re.IGNORECASE) + articles_df['Excerpt'].str.count(sponsor, flags=re.IGNORECASE)

    articles_df['Powered_By'] = (articles_df['Excerpt'].str.contains('powered by', case=False, na=False) | articles_df['Title'].str.contains('powered by', case=False, na=False))
    articles_df['Presented_By'] = (articles_df['Excerpt'].str.contains('presented by', case=False, na=False) | articles_df['Title'].str.contains('presented by', case=False, na=False))

    articles_df['Sponsors_List'] = articles_df.apply(lambda row: extract_sponsors(row['Title']) + extract_sponsors(row['Excerpt']),axis=1)
    articles_df['Major_Sponsor'] = articles_df['Sponsors_List'].apply(lambda sponsor_list: [s for s in sponsor_list if s in major_sponsors])
    articles_df['Other_Sponsor'] = articles_df['Sponsors_List'].apply(lambda sponsor_list: [s for s in sponsor_list if s not in major_sponsors])

    articles_df = articles_df.drop(columns=['Url','Author'])

    try:  
        # save cleaned data to csv
        articles_df.to_csv(cleaned_csv_path, index=False)

        return articles_df
    except Exception as e:
        print(f"Error saving GSW stats data to CSV file: {e}")
        return None
    
def process_trends_data(file: str) -> pd.DataFrame:
    trend_df = pd.read_csv(file)