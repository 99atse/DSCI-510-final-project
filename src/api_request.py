import requests

import pandas as pd
import json

news_url = 'https://www.nba.com/warriors/api/content/category/news?page={}'
articles = []
page_number = 1

while len(articles) < 1000:
    news_url_with_page = news_url.format(page_number)
    response = requests.get(news_url_with_page)
    data = response.json()
    items = data.get("items",[])
    for item in items:
        articles.append({
                "title": item.get("title"),
                "date": item.get("date"),
                "excerpt": item.get("excerpt"),
                "url": item.get("permalink"),
                "author": (
                    item["authors"][0]["name"] 
                    if item.get("authors") and len(item["authors"]) > 0 
                    else None
                )
            })
    print(f"Page {page_number} fetched — total articles: {len(articles)}")
    page_number += 1

df = pd.DataFrame(articles)

df.to_csv('dubs_articles.csv', index=False)

print(df.head())

