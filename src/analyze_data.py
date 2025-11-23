import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

# --- PLOT GSW STATISTICS ---
def plot_gsw_stats(stats_df, result_dir="plots", notebook_plot=False):
    """
    Generates and saves basic plots for GSW stats.

    :param stats_df: The GSW stats pandas DataFrame
    :param result_dir: where to place plots
    :param dataset_name: A name for titling plots (e.g., 'Titanic')
    """

    # Ensure a directory for plots exists
    os.makedirs(result_dir, exist_ok=True)

    wins = stats_df[stats_df["Win"] == 1]
    losses = stats_df[stats_df["Win"] == 0]
    plt.figure(figsize=(36,8))
    plt.scatter(wins["Date"], wins["Abs_Point_Difference"], color="green", label="Win")
    plt.scatter(losses["Date"], losses["Abs_Point_Difference"], color="red", label="Loss")

    plt.title(f'GSW 2021-2025 Season Performance')
    plt.legend()
    plt.xlabel('Game Date')
    plt.ylabel('Point Difference')
    plt.tight_layout()

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.1)

    if not notebook_plot:
        plt.savefig(f'{result_dir}/2021-2025_GSW_Stats_Plot.png')
        print(f"Saved stats plot for entire dataframe.")
        plt.close()
    else:
        plt.plot()
        
    # plot point difference and W/L each season
    season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

    for year,start_date,end_date in season_dates:
        season_range = (stats_df['Date'] >= pd.to_datetime(start_date)) & (stats_df['Date'] <= pd.to_datetime(end_date))
        plt.figure(figsize=(20,12))
        wins = stats_df[season_range & (stats_df["Win"] == 1)]
        losses = stats_df[season_range & (stats_df["Win"] == 0)]

        plt.scatter(wins["Date"], wins["Abs_Point_Difference"], color="green", label="Win")
        plt.scatter(losses["Date"], losses["Abs_Point_Difference"], color="red", label="Loss")

        plt.title(f'{year} GSW Season Performance')
        plt.legend()
        plt.xlabel('Game Date')
        plt.ylabel('Point Difference')
        plt.tight_layout()

        # Set x-axis major ticks every 10 days
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.1)

        if not notebook_plot:
            plt.savefig(f'{result_dir}/{year}_GSW_Stats_Plot.png')
            print(f"Saved stats plot for {year} season.")
            plt.close()
        else:
            plt.plot()

# --- PLOT GSW ARTICLE STATISTICS ---
def plot_articles(articles_df, result_dir="plots", notebook_plot=False):
    """
    Generates and saves basic plots for GSW article.

    :param articles_df: The GSW articles pandas DataFrame
    :param result_dir: where to place plots
    :param dataset_name: A name for titling plots (e.g., 'Titanic')
    """

    # Ensure a directory for plots exists
    os.makedirs(result_dir, exist_ok=True)

    # create a histogram of sponsor count across article
    major_sponsor = articles_df[articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
    other_sponsor = articles_df[articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) == 0)]

    plt.figure(figsize=(36,10))
    plt.scatter(major_sponsor["Date"], major_sponsor["Total_Sponsor_Count"], color="green", label="Major Sponsor")
    plt.scatter(other_sponsor["Date"], other_sponsor["Total_Sponsor_Count"], color="gray", label="Other Sponsor")

    plt.title(f'GSW 2021-2025 Article Sponsor Historgram')
    plt.legend()
    plt.xlabel('Article Date')
    plt.ylabel('Sponsor Count')
    plt.tight_layout()

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.1)

    if not notebook_plot:
        plt.savefig(f'{result_dir}/2021-2025_GSW_Article_Plot.png')
        print(f"Saved articles plot for entire dataframe.")
        plt.close()
    else:
        plt.plot()

        # plot point difference and W/L each season
    season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

    for year,start_date,end_date in season_dates:
        season_range = (articles_df['Date'] >= pd.to_datetime(start_date)) & (articles_df['Date'] <= pd.to_datetime(end_date))
        
        major_sponsor = articles_df[season_range & articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
        other_sponsor = articles_df[season_range & articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) == 0)]

        plt.figure(figsize=(20,12))
        plt.scatter(major_sponsor["Date"], major_sponsor["Total_Sponsor_Count"], color="blue", label="Major Sponsor")
        plt.scatter(other_sponsor["Date"], other_sponsor["Total_Sponsor_Count"], color="gray", label="Other Sponsor")

        plt.title(f'GSW {year} Article Sponsor Historgram')
        plt.legend()
        plt.xlabel('Article Date')
        plt.ylabel('Sponsor Count')
        plt.tight_layout()

        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.1)

        if not notebook_plot:
            plt.savefig(f'{result_dir}/{year}_GSW_Article_Plot.png')
            print(f"Saved articles plot for {year} season.")
            plt.close()
        else:
            plt.plot()

# --- PLOT TREND STATISTICS ---
def plot_all_trends(trends_csv, result_dir="plots", notebook_plot=False):
    """
    Generates and saves basic plots for all Google trends data.

    :param trends_csv: All Trends csv file
    :param result_dir: where to place plots
    :param notebook_plot: show plot if function is called in .ipynb
    """
    
    all_trends = pd.read_csv(trends_csv, parse_dates=['Date'])

    # Ensure a directory for plots exists
    os.makedirs(result_dir, exist_ok=True)

    sponsors = ['Rakuten','United Airlines','JPMorgan Chase']

    for keyword in sponsors:
        plt.figure(figsize=(36,8))
        plt.plot(all_trends["Date"], all_trends['Golden State Warriors'], label='Golden State Warriors')
        plt.plot(all_trends["Date"], all_trends[keyword], label=keyword)
        plt.title(f'2021-2025 {keyword} Sponsor Trend Data')
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Interest over Time')
        plt.tight_layout()
        
        # Set x-axis major ticks every 10 days
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime('2020-12-22'), pd.to_datetime('2025-04-13'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.2)
        if not notebook_plot:
            plt.savefig(f'{result_dir}/2021-2025_{keyword.replace(" ","")}_Sponsor_Trends_Plot.png')
            print(f"Saved trends plot for {keyword} and entire time frame.")
            plt.close()
        else:
            plt.plot()

        season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

        for year,start_date,end_date in season_dates:
            season_range = (all_trends['Date'] >= pd.to_datetime(start_date)) & (all_trends['Date'] <= pd.to_datetime(end_date))
            plt.figure(figsize=(18,12))
            plt.plot(all_trends.loc[season_range,"Date"], all_trends.loc[season_range,'Golden State Warriors'], label='Golden State Warriors')
            plt.plot(all_trends.loc[season_range,"Date"], all_trends.loc[season_range,keyword], label=keyword)

            plt.title(f'{year} {keyword} Sponsor Trend Data')
            plt.legend()
            plt.xlabel('Date')
            plt.ylabel('Interest over Time')
            plt.tight_layout()

            # Set x-axis major ticks every 10 days
            ax = plt.gca()
            ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.1)

            if not notebook_plot:
                plt.savefig(f'{result_dir}/{year}_{keyword.replace(" ","")}_Sponsor_Trends_Plot.png')
                print(f"Saved trends plot for {keyword} in {year} season.")
                plt.close()
            else:
                plt.plot()

def plot_all_data(all_df, result_dir="plots", notebook_plot=False):
    """
    Generates and saves basic plots for all Google trends data.

    :param trends_csv: All Trends csv file
    :param result_dir: where to place plots
    :param notebook_plot: show plot if function is called in .ipynb
    """
    os.makedirs(result_dir, exist_ok=True)

    # create a histogram of sponsor count across article
    sponsors_names = ['Rakuten','United Airlines','JPMorgan Chase']
    count_sponsors = ['Rakuten','UnitedAirlines','Chase']
    wins = all_df[all_df["Win"] == 1]
    losses = all_df[all_df["Win"] == 0]

    for keyword,count_sponsor in zip(sponsors_names,count_sponsors):
        sponsor_count = all_df[all_df[f'{count_sponsor}_Count'] > 0]

        plt.figure(figsize=(36,10))
        plt.plot(all_df["Date"],all_df['Golden State Warriors'], label='Golden State Warriors')
        plt.plot(all_df["Date"], all_df[keyword], label=keyword)
        plt.scatter(wins["Date"], wins["Abs_Point_Difference"], color="green", label="Win")
        plt.scatter(losses["Date"], losses["Abs_Point_Difference"], color="red", label="Loss")
        plt.scatter(sponsor_count["Date"], sponsor_count[f'{count_sponsor}_Count'], color="blue", label=f"{keyword} Mentioned",marker='^')

        plt.title(f'2021-2025 GSW Stats/Sponsorship Mentions/{keyword} Data')
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Game Performance/Sponsorship Count/Interest over Time')
        plt.tight_layout()

        # Set x-axis major ticks every 10 days
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime('2020-12-22'), pd.to_datetime('2025-04-13'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.1)
        if not notebook_plot:
            plt.savefig(f'{result_dir}/2021-2025_{count_sponsor}_GSW_Data_Plot.png')
            print(f"Saved all data and {keyword} plot for entire time frame.")
            plt.close()
        else:
            plt.plot()

        season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]
    
        for year,start_date,end_date in season_dates:
            season_range = (all_df['Date'] >= pd.to_datetime(start_date)) & (all_df['Date'] <= pd.to_datetime(end_date))

            sponsor_count_season = all_df[season_range & (all_df[f'{count_sponsor}_Count'] > 0)]
            wins_season = all_df[season_range & (all_df["Win"] == 1)]
            losses_season = all_df[season_range & (all_df["Win"] == 0)]

            plt.figure(figsize=(24,12))
            plt.plot(all_df.loc[season_range,"Date"], all_df.loc[season_range,'Golden State Warriors'], label='Golden State Warriors')
            plt.plot(all_df.loc[season_range,"Date"], all_df.loc[season_range,keyword], label=keyword)
            plt.scatter(wins_season["Date"], wins_season["Abs_Point_Difference"], color="green", label="Win")
            plt.scatter(losses_season["Date"], losses_season["Abs_Point_Difference"], color="red", label="Loss")
            plt.scatter(sponsor_count_season["Date"], sponsor_count_season[f"{count_sponsor}_Count"], color="blue", label=f"{keyword} Mentioned",marker='^')

            plt.title(f'{year} GSW Stats/Sponsorship Mentions/{keyword} Data')
            plt.legend()
            plt.xlabel('Date')
            plt.ylabel('Game Performance/Sponsorship Count/Interest over Time')
            plt.tight_layout()

            # Set x-axis major ticks every 10 days
            ax = plt.gca()
            ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.1)

            if not notebook_plot:
                plt.savefig(f'{result_dir}/{year}_GSW_All_Data_{count_sponsor}_Plot.png')
                print(f"Saved all data plot and {keyword} for {year} season.")
                plt.close()
            else:
                plt.plot()