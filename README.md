# Influence of Golden State Warriors Game Performance on Fan Engagement and Sponsorship Visibility

For my final project, I reviewed the past NBA 5 seasons for the Golden State Warriors to determine the effect of the game performance on fan engagement and sponsorship visibility. 

__Data Sources__

I retrieved data from three sources: Warriors News API, ESPN season schedule webpage, and Google Trend API (pytrends).

| Data Source # | Name/ Short Description | Source URL | Type | List of Fields | Format | Access/Collect data with Python? | Estimated data size/data points |
| :------- | :------ | :------- | :------- | :------ | :------- | :------- | :------ |
| 1     | Team Performance Metrics   | https://www.espn.com/nba/team/schedule/_/name/gs/season    | Webpage     | Date, Opponent, Result, W-L, Hi-Points, Hi-Rebounds, Hi-Assists   | HTML    | Yes     | 403   |
| 2     | Sponsorship Visibility   | https://www.nba.com/warriors/api/content/category/news   | API   | Title, Date, Excerpt, URL, Author   | JSON   | Yes   | 840   |
| 3     | Fan Engagement      | pytrends (API for Google Trends)      | API      | Date, Interest over Time      | CSV      | Yes      | 1800      |

Game Performance:

Sponsorship Visibility:

Fan Engagement:
I measured engagement through Google Trends to evaluate interest over time of the Warriors and their major sponsors (according to Forbes). Sponsorship visibility was evaluated using the frequency of sponsor mentions on Warriors' news website.  

Note: all coding was run in Conda environment.<br>

__Results__
_describe your findings_

__Installation__
- _describe what API keys, user must set where (in .enve) to be able to run the project._
- _describe what special python packages you have used_

From `src/` directory run:

`python main.py `

Results will appear in `results/` folder. All obtained will be stored in `data/`

__References:__
https://pypi.org/project/pytrends/<br>
https://github.com/GeneralMills/pytrends/blob/master/pytrends/dailydata.py