# __Influence of Golden State Warriors Game Performance on Fan Engagement and Sponsorship Visibility__

For my final project, I reviewed the past NBA 5 seasons for the Golden State Warriors to determine the effect of the game performance and sponsorship visibility on fan engagement with team sponsors. As a sports fan, I have observed how in many professional sports leagues, companies will participate in team sponsorship to expand brand visibility and build deeper relationships with consumers. My final project examines if and how game-to-game performance and sponsorship visibility affects the engagement of such sponsoring companies.

## __Data Sources__

I retrieved data from three sources: Warriors News Website API, ESPN Season Schedule Webpage, and Google Trend API (pytrends).

| Data Source # | Name/ Short Description | Source URL | Type | List of Fields | Format | Access/Collect data with Python? | Estimated data size/data points |
| :------- | :------ | :------- | :------- | :------ | :------- | :------- | :------ |
| 1     | Team Performance Metrics   | https://www.espn.com/nba/team/schedule/_/name/gs/season    | Webpage     | Date, Opponent, Result, W-L, Hi-Points, Hi-Rebounds, Hi-Assists   | HTML    | Yes     | 400   |
| 2     | Sponsorship Visibility   | https://www.nba.com/warriors/api/content/category/news   | API   | Title, Date, Excerpt, URL, Author   | JSON   | Yes   | 738   |
| 3     | Fan Engagement      | pytrends (API for Google Trends)      | API      | Date, Interest over Time      | CSV      | Yes      | 1575      |

__Game Performance:__
Using ESPN's webpage, I collected statistics from every Golden State Warriors game played during the 2021-2025 seasons. Tracking win/losses and player performance highs, I also transformed the data to account for absolute point difference, overtime, and other game statistics. To measure game to game performance, I prioritized absolute point difference, game win/loss, and Stephen Curry's performance (if top scorer in game).

__Sponsorship Visibility:__
Sponsorship visibility was evaluated using the frequency of sponsor mentions on the Golden State Warriors' News Website. Using the site's API, I pulled information from all articles within the 5 season time range and created new features for sponsor mentions. To account for days where multiple articles were published, I summed the count values for each column that day, into one.

__Fan Engagement:__
I measured engagement through Google Trends and evaluated the interest over time for the Golden State Warriors and their major sponsors (according to Forbes). Interest over time is a search term's popularity, normalized over a designated time range. Pytrends allows users to download Google Trend reports and can scale the data to more specificity when Google adjusts data frequencies (day to week) for longer time ranges.

Note: all coding was run in Conda environment.<br>

## __Results__

For my analysis, I first created line and scatter plots for all game statistics, articles, and trend data. I also created correlation matrices, and fit linear regression models to the data depending on my findings in the plots. Additionally, to account for potential delay in the effect of game performance or sponsorship visibility on trends, I also conducted my analyses using adjusted data, shifting trend values forward by one day. 

Note: My findings for each sponsor returned relatively similar results so I will describe the generalized findings below for the five season range and individual seasons, elaborating on significant results.

__Game to Game Performance on Engagement__<br>
Predictor(s): Absolute Point Difference

- _Line and Scatter Plots_: For both the 2021-2025 time range and each individual season, there is no obvious relationship between absolute point difference and sponsor interest over time.

- _Correlation Matrix_: Reviewing the correlation matrix across the five seasons, absolute point difference is very weakly correlated with sponsors' trending interest over time. All correlation values fall under |.20|.

- _Linear Regression_: Fitting a linear regression model to the data for both the 2021-2025 time range and individual seasons, absolute point difference accounts for almost none of the variance within the data (R-Squared $\approx 0$).


__Sponsorship Visibility on Engagement__<br>
Predictor(s): Sponsorship Mentions Count

- _Line and Scatter Plots_: When analyzing sponsorship visibility on sponsor interest over time, the line and scatter plots do not provide a distinguishable relationship between the variables. Through my review of the plots, I realize major sponsors are not consistently mentioned in Warriors' articles to serve as a robust data source for analysis. 

- _Linear Regression_: Like game performance, sponsorship visibility accounts for almost none of the variance within the data and all variables are insignificant predictors.


__Stephen Curry Performance and Game Wins on Engagement__<br>
Predictor(s): Stephen Curry Hi Points and Game Win

- _Correlation Matrix_: The correlation matrix for Stephen Curry's performance (when he is top scorer for the game) and game wins reveals stronger effect on major sponsor interest over time, however the correlation between performance and sponsor trends is still weak (<0.15).

- _Linear Regression_: The effect of Stephen Curry's performance and game wins fluctuate significantly on sponsor interest over time. In general these predictors account for 0-10% of the variance within the data, more than the effect of absolute point difference. The coefficients of the predictors again are almost always insignificant.


__Game to Game Performance on Golden State Warriors Engagement__<br>
Predictor(s): Stephen Curry Hi Points, Game Win, and Absolute Point Difference

- _Correlation Matrix_: The correlation coefficients are extremely weak for both adjusted and non-adjusted Warriors interest over time; the strongest relationship is absolute point difference (-0.16).

- _Linear Regression_: When comparing adjusted Golden State Warriors interest over time with all three predictors, there seems to be a more visible relationship. Across the five season range and each individual season, the variance explained ranges from 3.9% to 28.3%. Additionally, in the five season time range, game wins(coefficient: 1.627) and absolute point difference(coefficient: -0.11) are significant (p < 0.05). Based on the sign of the coefficients, this signifies that when the Warriors win, and when absolute point difference decreases (tighter game score), Warriors trending interest over time increases.

## __Installation__

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

From `DSCI-510-final-project/` directory run:

`python src/main.py`

The code will retrieve data from all three sources, clean and transform the data, return the head of the data, and create all plots. 

Note: In `process_trends_data()`, parameters _retrieve_api_ and _all_sponsors_ are initially set to True. This means the function will retrieve GSW trend data from the pytrends api(retrieve_api) and it will be added to the all trends csv file(all_sponsors). It is an option to change retrieve_api to False because pytrends occasionally returns an error if you make too many requests or your time range is long. 

In the initial run, I recommend running `python src/tests.py` first to confirm if the data is loading correctly. If the test runs successfully, switch retrieve_api to _False_ and keep _all_sponsors_ as _True_, then run `python src/main.py`. If pytrends returns an error loading the data, keep _all_sponsors_ to _True_, set _retrieve_api_ to _False_, delete the `All_Trends_Cleaned.csv` file in the `data/cleaned/` directory, then re-run `python src/main.py`.

All plots will appear in `results/` folder, separated by data source. To review the linear regression results, see `src/results.ipynb`. All obtained data will be stored in `data/`, separated into raw and cleaned data.

## __References:__

https://pypi.org/project/pytrends/<br>
https://github.com/GeneralMills/pytrends/blob/master/pytrends/dailydata.py<br>
https://newsinitiative.withgoogle.com/resources/trainings/google-trends-understanding-the-data/<br>
https://www.forbes.com/teams/golden-state-warriors/<br>