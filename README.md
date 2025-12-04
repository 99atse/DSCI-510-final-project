# Influence of Golden State Warriors Game Performance on Fan Engagement and Sponsorship Visibility

For my final project, I reviewed the past NBA 5 seasons for the Golden State Warriors to determine the effect of the game performance and sponsorship visibility on fan engagement with team sponsors. As a sports fan, I have observed how in many professional sports leagues, companies will participate in team sponsorship to expand brand visibility and build deeper relationships with consumers. My final project examines if and how game-to-game performance and sponsorship visibility affects the engagement of such sponsoring companies.

__Data Sources__

I retrieved data from three sources: Warriors News Website API, ESPN Season Schedule Webpage, and Google Trend API (pytrends).

| Data Source # | Name/ Short Description | Source URL | Type | List of Fields | Format | Access/Collect data with Python? | Estimated data size/data points |
| :------- | :------ | :------- | :------- | :------ | :------- | :------- | :------ |
| 1     | Team Performance Metrics   | https://www.espn.com/nba/team/schedule/_/name/gs/season    | Webpage     | Date, Opponent, Result, W-L, Hi-Points, Hi-Rebounds, Hi-Assists   | HTML    | Yes     | 400   |
| 2     | Sponsorship Visibility   | https://www.nba.com/warriors/api/content/category/news   | API   | Title, Date, Excerpt, URL, Author   | JSON   | Yes   | 738   |
| 3     | Fan Engagement      | pytrends (API for Google Trends)      | API      | Date, Interest over Time      | CSV      | Yes      | 1575      |

__Game Performance:__

__Sponsorship Visibility:__
Sponsorship visibility was evaluated using the frequency of sponsor mentions on the Golden State Warriors' News Website. Using the site's API, I pulled information from all articles within the 5 season time range and created new features for sponsor counts based on frequency. To account for days where multiple articles were published, I summed the values for each column that day, into one.

__Fan Engagement:__
I measured engagement through Google Trends and evaluated the interest over time for the Golden State Warriors and their major sponsors (according to Forbes). Interest over time is a search term's popularity, normalized over a designated time range. Pytrends allows users to download Google Trend reports and can scale the data to more specificity when Google adjusts data frequencies (day to week) for longer time ranges.

Note: all coding was run in Conda environment.<br>

__Results__

_describe your findings_

__Installation__

For both APIs used, no keys are required to run the project. Therefore, no .env file is necessary. All package requirements can be found in `requirements.txt`. Imported packages requried to run the project code include:
- requests
- json
- bs4
- pytrends
- re
- os
- ast
- matplotlib
- pandas
- numpy
- seaborn
- statsmodels

From `src/` directory run:

`python main.py`

The code will retrieve data from all three sources, clean and transform the data, return the head of the data, and create all plots. 

All plots will appear in `results/` folder, separated by data source. To review the linear regression results, see `src/results.ipynb`. All obtained data will be stored in `data/`, separated into raw and cleaned data.

__References:__
https://pypi.org/project/pytrends/<br>
https://github.com/GeneralMills/pytrends/blob/master/pytrends/dailydata.py<br>
https://newsinitiative.withgoogle.com/resources/trainings/google-trends-understanding-the-data/<br>
https://www.forbes.com/teams/golden-state-warriors/<br>