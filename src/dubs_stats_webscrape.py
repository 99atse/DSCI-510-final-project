import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


# while year < 2027:
#     season_url = url.format(year)
#     res = requests.get(season_url, headers=headers)
#     soup = BeautifulSoup(res.text, "html.parser")


#     with open('dubs_stats_24-25.html','w',encoding ='utf-8') as filename:
#         filename.write(soup.prettify())

#     tables = soup.find("table")

#     # --- Extract headers ---
#     headers = [td.get_text(strip=True) for td in tables.find_all("td")]
#     header = headers[1:8]
#     # print(header)
#     body = headers[8:]
#     # print(body)

#     for i in range(0,len(body),7):
#         game_rows.append(body[i:i+7])

#     year += 1

# rows = pd.DataFrame(game_rows,columns = header)
# print(rows)

# rows.to_csv('dubs_game_stats.csv', index=False)

# base_url = "https://www.espn.com/nba/team/schedule/_/name/gs/season/{}"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/118.0.0.0 Safari/537.36"
# }

# all_games = []
# url = base_url.format(2021)
# res = requests.get(url, headers=headers)
# soup = BeautifulSoup(res.text, "html.parser")
# with open('dubs_stats_2021.html', 'w', encoding='utf-8') as f:
#     f.write(soup.prettify())
    
base_url = "https://www.espn.com/nba/team/schedule/_/name/gs/season/{}"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
}

all_games = []

for year in range(2021, 2027):  # 2021–2026 inclusive
    url = base_url.format(year)
    print(f"Fetching {url}")
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

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
        cols = row.find_all("td", class_="Table__TD")
        if len(cols) == 7:
            date = cols[0].get_text(strip=True)
            opponent = cols[1].get_text(" ", strip=True)
            result = cols[2].get_text(" ", strip=True)
            record = cols[3].get_text(strip=True)
            hi_points = cols[4].get_text(" ", strip=True)
            hi_rebounds = cols[5].get_text(" ", strip=True)
            hi_assists = cols[6].get_text(" ", strip=True)

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

    time.sleep(1)

df = pd.DataFrame(all_games)
print(f"✅ Scraped {len(df)} games total.")
df.to_csv("warriors_schedule_2021_2026.csv", index=False)
