import requests
import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from pytrends import dailydata

# --- Load News Articles from Golden State Warriors Website ---
def get_gsw_articles_api(api_url, json_file, dataset_file, **kwargs):
    """
    Retrieves article information from API URL, saves raw data to JSON file
    and CSV, and loads the data to a pandas DataFrame. 

    :param api_url: base API URL to request data from GSW News website
    :param json_file: JSON file to extract data and examine format
    :param dataset_file: CSV file to place raw data from pandas DataFrame
    #param to be added: dir - data directory to place extracted data into
    :return: Pandas DataFrame or None
    """

    articles = []
    page_number = 1

    # extract data directory
    extract_dir = kwargs.get("extract_dir", ".")
    os.makedirs(extract_dir, exist_ok=True)

    # path to place files into data folder
    json_path = os.path.join(extract_dir, json_file)
    csv_path = os.path.join(extract_dir, dataset_file)

    # create while loop to continue retrieving articles until reaching 1000 total articles
    print("loading data from GSW News website")
    while len(articles) < 1000:
        try:
            # format url with page number starting at 1 and create API request
            article_url_with_page = api_url.format(page_number)
            response = requests.get(article_url_with_page,timeout=10)
            response.raise_for_status()
            # parse request as json file and retrieve articles (aka items)
            data = response.json()
        except Exception as e:
            print(f"Error loading GSW news data from page {page_number}: {e}")
            continue
        # write page 1 request to json file to examine data
        if page_number == 1:
            try:
                with open(json_path,'w',encoding='utf-8') as file:
                    json.dump(data,file,indent=4,ensure_ascii=False)
                    print("articles json file has been created")
            except Exception as e:
                print(f"Error saving GSW news data to JSON file: {e}")
                continue
        
        # parse items from data
        items = data.get("items",[])
        print(f"parsing articles from page {page_number}")

        # for each item in page, append to articles list (title, date, blurb, url link, author)
        for article in items:
            try:
                articles.append({
                        "title": article.get("title"),
                        "date": article.get("date"),
                        "excerpt": article.get("excerpt"),
                        "url": article.get("permalink"),
                        "author": (
                            article["authors"][0]["name"] 
                            if article.get("authors") and len(article["authors"]) > 0 
                            else None
                        )
                    })
            except Exception as e:
                print(f"Error appending GSW news article to articles DataFrame: {e}")
                continue
            
        # add 1 to page number to continue to next page
        page_number += 1
    try:
        # convert list of articles to dataframe then to csv
        article_df = pd.DataFrame(articles)
        article_df.to_csv(csv_path, index=False)

        # return article dataframe
        return article_df
    except Exception as e:
        print(f"Error saving GSW news data to CSV file: {e}")
        return None

# --- Load Game Statistics From ESPN Website ---
def get_gsw_game_stats_webscrape(webscrape_url,html_file, dataset_file,**kwargs):
    """
    Scrapes statistics table from ESPN's GSW season schedule, saves raw data to HTML file
    and CSV, and loads the data to a pandas DataFrame. 

    :param webscrape_url: base webscrape URL to request data from ESPN webiste
    :param html_file: HTML file to extract data and examine format
    :param dataset_file: CSV file to place raw data from pandas DataFrame
    :param start_year: first year to begin pulling season data
    :param end_year: last year to pull season data
    #param to be added: dir - data directory to place extracted data into
    :return: Pandas DataFrame or None
    """
        
    all_games = []

    # extract data directory
    extract_dir = kwargs.get("extract_dir", ".")
    os.makedirs(extract_dir, exist_ok=True)

    # path to place files into data folder
    html_path = os.path.join(extract_dir, html_file)
    csv_path = os.path.join(extract_dir, dataset_file)

    #set user agent to prevent 403 error
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
    }
    # create for loop to retrieve game stats for multiple seasons
    for year in range(2021, 2027):  # 2021–2026 inclusive
        try:
            # format url with year starting at start year, create webscrape request and parse with beautifulsoup
            url = webscrape_url.format(year)
            response = requests.get(url, headers=user_agent,timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error loading GSW stats data from year {year}: {e}")
            continue
        
        try:
            # write start year request to html file to examine data
            if year == 2021:
                with open(html_path, "w", encoding="utf-8") as file:
                    file.write(str(soup.prettify()))
        except Exception as e:
            print(f"Error loading GSW stats data to HTML file: {e}")
            continue

        # find game stats table in html
        table = soup.find("table", class_="Table")
        if not table:
            print(f"No table found for {year}")
            continue

        # Extract header names
        headers_row = table.find_all("td", class_="Table_Headers")
        headers_list = [h.get_text(strip=True) for h in headers_row]
        if not headers_list:
            headers_list = ["DATE", "OPPONENT", "RESULT", "W-L", "Hi Points", "Hi Rebounds", "Hi Assists"]

        # Extract game rows (each <tr> with data-testid attributes)
        for row in table.find_all("tr", class_="Table__TR--sm"):
            try:
                # find row data
                columns = row.find_all("td", class_="Table__TD")
                # if number of columns match header, then retrive cell information and append to all_games list
                if len(columns) == 7:
                    date = columns[0].get_text(strip=True)
                    opponent = columns[1].get_text(" ", strip=True)
                    result = columns[2].get_text(" ", strip=True)
                    record = columns[3].get_text(strip=True)
                    hi_points = columns[4].get_text(" ", strip=True)
                    hi_rebounds = columns[5].get_text(" ", strip=True)
                    hi_assists = columns[6].get_text(" ", strip=True)

                    all_games.append({
                        "Season": year,
                        "Date": date,
                        "Opponent": opponent,
                        "Result": result,
                        "Record": record,
                        "Hi Points": hi_points,
                        "Hi Rebounds": hi_rebounds,
                        "Hi Assists": hi_assists
                    })
            except Exception as e:
                print(f"Error loading row stats data to stats list: {e}")
                continue
    try:  
        # convert list of games to dataframe then to csv
        stats_df = pd.DataFrame(all_games)
        stats_df.to_csv(csv_path, index=False)

        return stats_df
    except Exception as e:
        print(f"Error saving GSW stats data to CSV file: {e}")
        return None


# --- Load Daily Trend Data from Google Trends (pytrends) ---
def get_gsw_sponsor_trends(keyword):
    """
    Retrieves daily trend (interest over time) data from Google Trends API pytrends, 
    saves extracted dataframe to CSV, and returns the data to a pandas DataFrame or None
    if exception occurs. 

    :param keyword: keyword to request daily data from ESPN webiste
    #param to be added: dir - data directory to place extracted data into
    :return: Pandas DataFrame or None
    """
    try:
        # retrieve the daily trend data for sponsor/gsw and add to csv using pytrends
        trends_df = dailydata.get_daily_data(
        word=keyword,
        start_year=2020,
        start_mon=10,
        stop_year=2025,
        stop_mon=10,
        geo='US',
        wait_time=5
        )

    except Exception as e:
        print(f"Error retrieving {keyword} trends data from pytrends: {e}")
        return None
    
    # remove spaces in keyword to format for CSV file
    keyword = keyword.replace(" ", "")
    
    try:  
        # save trends data to csv and return data as df
        trends_df.to_csv(f"{keyword}_trends.csv",index=False)

        return trends_df
    except Exception as e:
        print(f"Error saving {keyword} trends data to CSV file: {e}")
        return None