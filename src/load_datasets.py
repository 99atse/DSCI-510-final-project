import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
from pytrends.request import TrendReq
from pytrends import dailydata
from datetime import date, timedelta

user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
    }

# load news articles from Golden State Warriors website
def get_dubs_articles_api(api_url, json_file, dataset_file):
    articles = []
    page_number = 1

    # create while loop to continue retrieving articles until reaching 1000 total articles
    while len(articles) < 1000:
        # format url with page number starting at 1 and create API request
        article_url_with_page = api_url.format(page_number)
        print(f"formatted url: {article_url_with_page}")
        response = requests.get(article_url_with_page)

        # parse request as json file and retrieve articles (aka items)
        data = response.json()

        # write page 1 request to json file to examine data
        if page_number == 1:
            with open(json_file,'w',encoding='utf-8') as file:
                json.dump(data,file,indent=4,ensure_ascii=False)
                print("articles json file has been created")

        items = data.get("items",[])

        print(f"parsing articles from page {page_number}")
        # for each item in page, append to articles list (title, date, blurb, url link, author)
        for article in items:
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
            
        # add 1 to page number to continue to next page
        page_number += 1

    # convert list of articles to dataframe then to csv
    article_df = pd.DataFrame(articles)
    article_df.to_csv(dataset_file, index=False)

    # return article dataframe
    return article_df

# load load game stats from ESPN website
def get_dubs_game_stats_webscrape(webscrape_url,html_file,stats_file,start_year:int,end_year:int):
    all_games = []

    # create for loop to retrieve game stats for multiple seasons
    for year in range(start_year, end_year+1):  # 2021–2026 inclusive
        # format url with year starting at start year, create webscrape request and parse with beautifulsoup
        url = webscrape_url.format(year)
        res = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(res.text, "html.parser")

        # write start year request to html file to examine data
        if year == start_year:
            with open(html_file, "w", encoding="utf-8") as file:
                file.write(str(soup.prettify()))

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
                
    # convert list of games to dataframe then to csv
    stats_df = pd.DataFrame(all_games)
    stats_df.to_csv(stats_file, index=False)

    return stats_df


def get_dubs_sponsor_trends(keyword):
    # retrieve the daily trend data for sponsor/gsw and add to csv using pytrends
    trends_df = dailydata.get_daily_data(
    word=keyword,
    start_year=2020,
    start_mon=10,
    stop_year=2025,
    stop_mon=10,
    geo='US'
    )
    keyword = keyword.replace(" ", "")

    trends_df.to_csv(f"{keyword}_trends.csv",index=False)

    return trends_df