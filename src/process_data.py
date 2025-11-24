import re
import os
import pandas as pd
import numpy as np

from config import DATA_DIR, STATS_HTML,STATS_CSV,CLEANED_STATS_CSV, ARTICLE_JSON, ARTICLE_CSV, CLEANED_ARTICLE_CSV
from load_datasets import get_gsw_game_stats_webscrape, get_gsw_articles_api, get_gsw_sponsor_trends

def process_game_data(url: str) -> pd.DataFrame:
    """
    Cleans and transforms loaded GSW statistics from ESPN tables, saves the cleaned data to CSV,
    and loads the data to a pandas DataFrame. 

    :param url: base webscrape URL to request data from ESPN website
    :return: Pandas DataFrame or None
    """
    stats_df = get_gsw_game_stats_webscrape(url,STATS_HTML,STATS_CSV,extract_dir = f'{DATA_DIR}/raw')

    # path to place files into data folder
    cleaned_csv_path = os.path.join(f'{DATA_DIR}/cleaned', CLEANED_STATS_CSV)
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)

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
    stats_df[['Wins', 'Losses']] = stats_df['Record'].str.split('-', expand=True).astype(int)
    stats_df[['Winner_Score', 'Loser_Score']] = stats_df['Result'].str[2:].str.split('-', expand=True).astype(int)
    stats_df['Team_Score'] = np.where(stats_df['Win'] == 1, stats_df['Winner_Score'], stats_df['Loser_Score'])
    stats_df['Opp_Score'] = np.where(stats_df['Win'] == 1, stats_df['Loser_Score'], stats_df['Winner_Score'])
    stats_df['Abs_Point_Difference'] = stats_df['Winner_Score'] - stats_df['Loser_Score']

    stats_df[['Hi_Points_Player', 'Hi_Points_Value']] = stats_df['Hi Points'].str.rsplit(' ', n=1, expand=True)
    stats_df[['Hi_Rebounds_Player', 'Hi_Rebounds_Value']] = stats_df['Hi Rebounds'].str.rsplit(' ', n=1, expand=True)
    stats_df[['Hi_Assists_Player', 'Hi_Assists_Value']] = stats_df['Hi Assists'].str.rsplit(' ', n=1, expand=True)
    stats_df['Hi_Points_Value'] = stats_df['Hi_Points_Value'].astype(int)
    stats_df['Hi_Rebounds_Value'] = stats_df['Hi_Rebounds_Value'].astype(int)
    stats_df['Hi_Assists_Value'] = stats_df['Hi_Assists_Value'].astype(int)

    stats_df = stats_df.drop(columns=['Hi Points', 'Hi Rebounds', 'Hi Assists', 'Result', 'Record','Year','Winner_Score', 'Loser_Score'])

    try:  
        # save cleaned data to csv
        stats_df.to_csv(cleaned_csv_path, index=False)

        return stats_df
    except Exception as e:
        print(f"Error saving GSW stats data to CSV file: {e}")
        return None

def extract_sponsors(text):
    """
    Finds all sponsors with a cell and returns them to a list.

    :param text: text from cell value to extract sponsors
    :return: list of sponsors or empty list
    """
    # filter sponsors and stop after reaching punctuation, end of sentence, or preposition
    sponsors = re.findall(r'(?:presented by|powered by|(?:in )?partnership with)\s+(.*?)(?: for | in | at | on |,|\.|;|$)', text, flags=re.IGNORECASE)

    return [sponsor.strip() for sponsor in sponsors]
  
def process_article_data(url: str) -> pd.DataFrame:
    """
    Cleans and transforms loaded articles from GSW news website, saves the cleaned data to CSV,
    and loads the data to a pandas DataFrame. 

    :param url: base API URL to request data from GSW news website
    :return: Pandas DataFrame or None
    """
    articles_df = get_gsw_articles_api(url,ARTICLE_JSON,ARTICLE_CSV,extract_dir = f'{DATA_DIR}/raw')

    # path to place files into data folder
    cleaned_csv_path = os.path.join(f'{DATA_DIR}/cleaned', CLEANED_ARTICLE_CSV)
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)

    articles_df['Date'] = pd.to_datetime(articles_df['Date']).dt.tz_convert(None).dt.normalize()
    start_date = pd.to_datetime("2020-12-22")
    end_date   = pd.to_datetime("2025-04-13")

    articles_df = articles_df[(articles_df['Date'] >= start_date) & (articles_df['Date'] <= end_date)]

    major_sponsors = ['Rakuten','United Airlines','Chase']
    for sponsor in major_sponsors:
        sponsor_no_spaces = sponsor.replace(" ","")
        articles_df[f'{sponsor_no_spaces}_Title'] = articles_df['Title'].str.contains(sponsor, case=False, na=False)
        articles_df[f'{sponsor_no_spaces}_Description'] = articles_df['Excerpt'].str.contains(sponsor, case=False, na=False)
        articles_df[f'{sponsor_no_spaces}_Count'] = articles_df['Title'].str.count(sponsor, flags=re.IGNORECASE) + articles_df['Excerpt'].str.count(sponsor, flags=re.IGNORECASE)

        articles_df = articles_df.drop(columns=[f'{sponsor_no_spaces}_Description',f'{sponsor_no_spaces}_Title'])
    
    articles_df['Sponsors_List'] = articles_df.apply(lambda row: list(dict.fromkeys(extract_sponsors(row['Title']) + extract_sponsors(row['Excerpt']))),axis=1)
    articles_df['Major_Sponsor'] = articles_df['Sponsors_List'].apply(lambda sponsor_list: [s for s in sponsor_list if s in major_sponsors])
    articles_df['Other_Sponsor'] = articles_df['Sponsors_List'].apply(lambda sponsor_list: [s for s in sponsor_list if s not in major_sponsors])
    articles_df['Total_Sponsor_Count'] = articles_df.apply(lambda row:len(extract_sponsors(row['Title']) + extract_sponsors(row['Excerpt'])),axis=1)

    articles_df = articles_df.drop(columns=['Url','Author'])

    daily_article_df = (articles_df.groupby('Date').agg({
        'Title': 'count',
        'Sponsors_List':'sum',
        'Total_Sponsor_Count': 'sum',
        'Major_Sponsor': 'sum',
        'Other_Sponsor': 'sum',
        'Rakuten_Count': 'sum',
        'UnitedAirlines_Count': 'sum',
        'Chase_Count':'sum'}
    ).rename(columns={'Title': 'Article_Count'})
    .reset_index())

    full_date_range = pd.DataFrame({"Date": pd.date_range(start="2020-12-22", end="2025-04-13")})
    daily_article_df = full_date_range.merge(daily_article_df, on="Date", how="left")
    
    daily_article_df = daily_article_df.fillna({
        'Article_Count': 0,
        'Sponsors_List':0,
        'Total_Sponsor_Count': 0,
        'Major_Sponsor': 0,
        'Other_Sponsor': 0,
        'Rakuten_Count': 0,
        'UnitedAirlines_Count': 0,
        'Chase_Count':0})

    try:  
        # save cleaned data to csv
        daily_article_df.to_csv(cleaned_csv_path, index=False)

        return daily_article_df
    except Exception as e:
        print(f"Error saving GSW stats data to CSV file: {e}")
        return None
    
def add_to_all_trends(sponsor,trend_df):
    """
    Adds cleaned and scaled data to an all sponsor trends table, creates new file if CSV doesn't exist,
    updates and loads to CSV if file exists.

    :param sponsor: keyword to pull trend data
    :param all_sponsors: add trend data to all_sponsor_trends CSV
    :return: None
    """
    all_trends_csv_path = os.path.join(f'{DATA_DIR}/cleaned', f'All_Trends_Cleaned.csv')
    os.makedirs(os.path.dirname(all_trends_csv_path), exist_ok=True)   

    # If file already exists, load it
    if os.path.exists(all_trends_csv_path):
        all_trends_df = pd.read_csv(all_trends_csv_path, parse_dates=['Date'])
    else:
        # Start new combined file with just the Date column
        all_trends_df = trend_df[["Date"]].copy() 

    # Join scaled sponsor data based on Date
    all_trends_df = all_trends_df.merge(
        trend_df[["Date", f"{sponsor}", f'{sponsor.replace(' ','')}_adjusted']], 
        on="Date", 
        how="outer"
    )

    all_trends_df.to_csv(all_trends_csv_path, index=False)

    return None

def process_trends_data(sponsor,all_sponsors=False) -> pd.DataFrame:
    """
    Cleans and transforms trend data from Google Trends, saves the cleaned data to CSV,
    and loads the data to a pandas DataFrame. 

    :param sponsor: keyword to pull trend data
    :param all_sponsors: add trend data to all_sponsor_trends CSV
    :return: Pandas DataFrame or None
    """

    # trend_df = get_gsw_sponsor_trends(sponsor,extract_dir = f'{DATA_DIR}/raw')
    trend_df = pd.read_csv(f'data/raw/{sponsor.replace(' ','')}_Trends.csv')

    cleaned_csv_path = os.path.join(f'{DATA_DIR}/cleaned', f'{sponsor.replace(' ','')}_Trends_Cleaned.csv')
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)

    trend_df['Date'] = pd.date_range(start='2020-12-01',end='2025-4-30',freq='D')
    trend_df[f'{sponsor.replace(' ','')}_adjusted'] = trend_df[f'{sponsor}'].shift(-1)
    start_date = '2020-12-22'
    end_date = '2025-04-13'
    trend_df = trend_df[(trend_df['Date'] >= start_date) & (trend_df['Date'] <= end_date)]

    trend_df = trend_df.reindex(columns=['Date',f'{sponsor}_unscaled',f'{sponsor}_monthly','isPartial','scale',f'{sponsor}',f'{sponsor.replace(' ','')}_adjusted'])

    if all_sponsors == True:
        add_to_all_trends(sponsor, trend_df)
    try:  
        # save cleaned data to csv
        trend_df.to_csv(cleaned_csv_path, index=False)

        return trend_df
    except Exception as e:
        print(f"Error saving {sponsor} trend data to CSV file: {e}")
        return None
    
def combine_all_data(stats_df,articles_df,all_trends_csv) -> pd.DataFrame:
    """
    Combines data from stats_df, articles_df, and trend_df into one dataframe 
    for easier plotting and analysis.

    :param stats_df: GSW stats dataframe
    :param articles_df: GSW news articles dataframe
    :param trend_df: Google Trends dataframe
    :param all_sponsors: add trend data to all_sponsor_trends CSV
    :return: Pandas DataFrame or None
    """

    cleaned_csv_path = os.path.join(f'{DATA_DIR}/cleaned', f'All_GSW_Data.csv')
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)

    trends_df = pd.read_csv(all_trends_csv,parse_dates=["Date"])

    stats_keep = stats_df[['Date','Win','Abs_Point_Difference','Hi_Points_Player', 'Hi_Points_Value','Hi_Rebounds_Player', 'Hi_Rebounds_Value','Hi_Assists_Player', 'Hi_Assists_Value']]
    stats_keep['Curry_Hi_Points'] = (stats_keep['Hi_Points_Player'] == 'Curry').astype(int)
    stats_keep['Curry_Hi_Points_Value'] = np.where(stats_keep['Curry_Hi_Points'] == 1,stats_keep['Hi_Points_Value'],np.nan)

    articles_keep = articles_df[['Date','Article_Count','Rakuten_Count','UnitedAirlines_Count','Chase_Count']]
    
    full_date_range = pd.DataFrame({"Date": pd.date_range(start="2020-12-22", end="2025-04-13")})
    
    combined_df = full_date_range.merge(trends_df, on='Date',how='outer')
    combined_df = combined_df.merge(articles_keep, on='Date',how='left')
    combined_df = combined_df.merge(stats_keep, on='Date',how='left')

    try:  
        # save cleaned data to csv
        combined_df.to_csv(cleaned_csv_path, index=False)

        return combined_df
    except Exception as e:
        print(f"Error saving GSW stats data to CSV file: {e}")
        return None