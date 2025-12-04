import os
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

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

    # scatter plot for game abs_point_difference, color coded by win/loss
    wins = stats_df[stats_df["Win"] == 1]
    losses = stats_df[stats_df["Win"] == 0]
    plt.figure(figsize=(36,12))
    plt.scatter(wins["Date"], wins["Abs_Point_Difference"], color="green", label="Win")
    plt.scatter(losses["Date"], losses["Abs_Point_Difference"], color="red", label="Loss")

    # add labels
    plt.title(f'GSW 2021-2025 Season Performance',fontsize = 22)
    plt.legend()
    plt.xlabel('Game Date', fontsize=18)
    plt.ylabel('Point Difference', fontsize=18)
    plt.tight_layout()

    # adjust time markers
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.1)

    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/2021-2025_GSW_Stats_Plot.png')
        print(f"Saved stats plot for entire dataframe.")
        plt.close()
    else:
        plt.plot()
        
    # plot point difference and W/L for each season using for loop
    season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

    for year,start_date,end_date in season_dates:
        # determine time range for season
        season_range = (stats_df['Date'] >= pd.to_datetime(start_date)) & (stats_df['Date'] <= pd.to_datetime(end_date))
        
        plt.figure(figsize=(22,12))

        # scatter plot for game abs_point_difference, color coded by win/loss
        wins = stats_df[season_range & (stats_df["Win"] == 1)]
        losses = stats_df[season_range & (stats_df["Win"] == 0)]
        plt.scatter(wins["Date"], wins["Abs_Point_Difference"], color="green", label="Win")
        plt.scatter(losses["Date"], losses["Abs_Point_Difference"], color="red", label="Loss")

        # add labels
        plt.title(f'{year} GSW Season Performance',fontsize = 22)
        plt.legend()
        plt.xlabel('Game Date',fontsize = 18)
        plt.ylabel('Point Difference',fontsize = 18)
        plt.tight_layout()

        # adjust time markers
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.1)

        if not notebook_plot:
            # save plot to results folder if not for jupyter notebook
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

    articles_df['Major_Sponsor'] = articles_df['Major_Sponsor'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # create a histogram of sponsor count across article color coded by sponsor type
    major_sponsor = articles_df[articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
    other_sponsor = articles_df[articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) == 0)]
    plt.figure(figsize=(36,12))
    plt.scatter(major_sponsor["Date"], major_sponsor["Total_Sponsor_Count"], color="green", label="Major Sponsor")
    plt.scatter(other_sponsor["Date"], other_sponsor["Total_Sponsor_Count"], color="gray", label="Other Sponsor")

    # add labels
    plt.title(f'GSW 2021-2025 Article Sponsor Historgram',fontsize = 22)
    plt.legend()
    plt.xlabel('Article Date',fontsize = 20)
    plt.ylabel('Sponsor Count',fontsize = 20)
    plt.tight_layout()

    # adjust time markers
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.1)

    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/2021-2025_GSW_Article_Plot.png')
        print(f"Saved articles plot for entire dataframe.")
        plt.close()
    else:
        plt.plot()

    # plot point difference and W/L each season
    season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

    for year,start_date,end_date in season_dates:
        # determine time range for season
        season_range = (articles_df['Date'] >= pd.to_datetime(start_date)) & (articles_df['Date'] <= pd.to_datetime(end_date))
        
        # create a histogram of sponsor count across article color coded by sponsor type
        major_sponsor = articles_df[season_range & articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
        other_sponsor = articles_df[season_range & articles_df['Major_Sponsor'].apply(lambda x: isinstance(x, list) and len(x) == 0)]
        plt.figure(figsize=(22,12))
        plt.scatter(major_sponsor["Date"], major_sponsor["Total_Sponsor_Count"], color="blue", label="Major Sponsor")
        plt.scatter(other_sponsor["Date"], other_sponsor["Total_Sponsor_Count"], color="gray", label="Other Sponsor")

        # add labels
        plt.title(f'GSW {year} Article Sponsor Historgram',fontsize = 22)
        plt.legend()
        plt.xlabel('Article Date',fontsize = 18)
        plt.ylabel('Sponsor Count',fontsize = 18)
        plt.tight_layout()

        # adjust time markers
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.1)

        if not notebook_plot:
            # save plot to results folder if not for jupyter notebook
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

    # create for loop for plotting each sponsor
    for keyword in sponsors:
        # plot trend lines for GSW and sponsor
        plt.figure(figsize=(36,7))
        plt.plot(all_trends["Date"], all_trends['Golden State Warriors'], label='Golden State Warriors')
        plt.plot(all_trends["Date"], all_trends[keyword], label=keyword)
        
        # add labels
        plt.title(f'2021-2025 {keyword} Sponsor Trend Data',fontsize = 22)
        plt.legend()
        plt.xlabel('Date',fontsize = 22)
        plt.ylabel('Interest over Time',fontsize = 22)
        plt.tight_layout()
        
        # adjust time markers
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime('2020-12-22'), pd.to_datetime('2025-04-13'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.2)

        if not notebook_plot:
            # save plot to results folder if not for jupyter notebook
            plt.savefig(f'{result_dir}/2021-2025_{keyword.replace(" ","")}_Sponsor_Trends_Plot.png')
            print(f"Saved trends plot for {keyword} and entire time frame.")
            plt.close()
        else:
            plt.plot()

        season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

        for year,start_date,end_date in season_dates:
            # determine time range for season
            season_range = (all_trends['Date'] >= pd.to_datetime(start_date)) & (all_trends['Date'] <= pd.to_datetime(end_date))
            
            # plot trend lines for GSW and sponsor
            plt.figure(figsize=(20,12))
            plt.plot(all_trends.loc[season_range,"Date"], all_trends.loc[season_range,'Golden State Warriors'], label='Golden State Warriors')
            plt.plot(all_trends.loc[season_range,"Date"], all_trends.loc[season_range,keyword], label=keyword)

            # add labels
            plt.title(f'{year} {keyword} Sponsor Trend Data',fontsize = 22)
            plt.legend()
            plt.xlabel('Date',fontsize = 18)
            plt.ylabel('Interest over Time',fontsize = 18)
            plt.tight_layout()

            # adjust time markers
            ax = plt.gca()
            ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.1)

            if not notebook_plot:
                # save plot to results folder if not for jupyter notebook
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
    # Ensure a directory for plots exists
    os.makedirs(result_dir, exist_ok=True)

    sponsors_names = ['Rakuten','United Airlines','JPMorgan Chase']
    count_sponsors = ['Rakuten','UnitedAirlines','Chase']
    wins = all_df[all_df["Win"] == 1]
    losses = all_df[all_df["Win"] == 0]


    for keyword,count_sponsor in zip(sponsors_names,count_sponsors):
        sponsor_count = all_df[all_df[f'{count_sponsor}_Count'] > 0]

        # plot trend, stats, and article data
        plt.figure(figsize=(36,12))
        plt.plot(all_df["Date"],all_df['Golden State Warriors'], label='Golden State Warriors')
        plt.plot(all_df["Date"], all_df[keyword], label=keyword)
        plt.scatter(wins["Date"], wins["Abs_Point_Difference"], color="green", label="Win")
        plt.scatter(losses["Date"], losses["Abs_Point_Difference"], color="red", label="Loss")
        plt.scatter(sponsor_count["Date"], sponsor_count[f'{count_sponsor}_Count'], color="blue", label=f"{keyword} Mentioned",marker='^')

        # add labels
        plt.title(f'2021-2025 GSW Stats/Sponsorship Mentions/{keyword} Data',fontsize = 22)
        plt.legend()
        plt.xlabel('Date',fontsize = 20)
        plt.ylabel('Game Performance/Sponsorship Count/Interest over Time',fontsize = 20)
        plt.tight_layout()

        # adjust time markers
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime('2020-12-22'), pd.to_datetime('2025-04-13'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.1)

        if not notebook_plot:
            # save plot to results folder if not for jupyter notebook
            plt.savefig(f'{result_dir}/2021-2025_{count_sponsor}_GSW_Data_Plot.png')
            print(f"Saved all data and {keyword} plot for entire time frame.")
            plt.close()
        else:
            plt.plot()

        season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]
    
        for year,start_date,end_date in season_dates:
            # determine time range for season
            season_range = (all_df['Date'] >= pd.to_datetime(start_date)) & (all_df['Date'] <= pd.to_datetime(end_date))

            sponsor_count_season = all_df[season_range & (all_df[f'{count_sponsor}_Count'] > 0)]
            wins_season = all_df[season_range & (all_df["Win"] == 1)]
            losses_season = all_df[season_range & (all_df["Win"] == 0)]
            
            # plot trend, stats, and article data
            plt.figure(figsize=(26,12))
            plt.plot(all_df.loc[season_range,"Date"], all_df.loc[season_range,'Golden State Warriors'], label='Golden State Warriors')
            plt.plot(all_df.loc[season_range,"Date"], all_df.loc[season_range,keyword], label=keyword)
            plt.scatter(wins_season["Date"], wins_season["Abs_Point_Difference"], color="green", label="Win")
            plt.scatter(losses_season["Date"], losses_season["Abs_Point_Difference"], color="red", label="Loss")
            plt.scatter(sponsor_count_season["Date"], sponsor_count_season[f"{count_sponsor}_Count"], color="blue", label=f"{keyword} Mentioned",marker='^')

            # add labels
            plt.title(f'{year} GSW Stats/Sponsorship Mentions/{keyword} Data',fontsize = 22)
            plt.legend()
            plt.xlabel('Date',fontsize = 18)
            plt.ylabel('Game Performance/Sponsorship Count/Interest over Time',fontsize = 18)
            plt.tight_layout()

            # adjust time markers
            ax = plt.gca()
            ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.1)

            if not notebook_plot:
                # save plot to results folder if not for jupyter notebook
                plt.savefig(f'{result_dir}/{year}_GSW_All_Data_{count_sponsor}_Plot.png')
                print(f"Saved all data plot and {keyword} for {year} season.")
                plt.close()
            else:
                plt.plot()

    # plot correlation matrix
    matrix = all_df.loc[:,['Abs_Point_Difference','Golden State Warriors','Rakuten','United Airlines','JPMorgan Chase']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Game Performance and GSW Sponsor Trends')
    plt.tight_layout()

    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/GSW_All_Data_Correlation_Matrix_Plot.png')
        print(f"Saved all data correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot time adjusted correlation matrix
    adjusted_matrix = all_df.loc[:,['Abs_Point_Difference','GoldenStateWarriors_adjusted','Rakuten_adjusted','UnitedAirlines_adjusted','JPMorganChase_adjusted']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(adjusted_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Game Performance and GSW Sponsor Trends')
    plt.tight_layout()

    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/Adjusted_GSW_All_Data_Correlation_Matrix_Plot.png')
        print(f"Saved adjusted trend data correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot Stephen Curry correlation matrix
    curry_matrix = all_df.loc[:,['Curry_Hi_Points_Value','Golden State Warriors','Rakuten','United Airlines','JPMorgan Chase']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(curry_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Curry Performance and GSW Sponsor Trends')
    plt.tight_layout()
    
    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/GSW_Curry_Correlation_Matrix_Plot.png')
        print(f"Saved Curry correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot time adjusted Stephen Curry correlation matrix
    curry_adjusted_matrix = all_df.loc[:,['Curry_Hi_Points_Value','GoldenStateWarriors_adjusted','Rakuten_adjusted','UnitedAirlines_adjusted','JPMorganChase_adjusted']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(curry_adjusted_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Curry Performance and GSW Sponsor Trends')
    plt.tight_layout()
    
    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/Adjusted_GSW_Curry_Correlation_Matrix_Plot.png')
        print(f"Saved adjusted Curry correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot Stephen Curry and Game Win correlation matrix
    curry_win_matrix = all_df.loc[:,['Curry_Hi_Points_Value','Win','Golden State Warriors','Rakuten','United Airlines','JPMorgan Chase']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(curry_win_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Steph Curry Performance, Game Win, and GSW Sponsor Trends')
    plt.tight_layout()
    
    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/GSW_Curry_Win_Correlation_Matrix_Plot.png')
        print(f"Saved Curry Win correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot time adjusted Stephen Curry and Game Win correlation matrix
    curry_win_adjusted_matrix = all_df.loc[:,['Curry_Hi_Points_Value','Win','GoldenStateWarriors_adjusted','Rakuten_adjusted','UnitedAirlines_adjusted','JPMorganChase_adjusted']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(curry_win_adjusted_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Steph Curry Performance,Game Win, and GSW Sponsor Trends')
    plt.tight_layout()
    
    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/Adjusted_GSW_Curry_Win_Correlation_Matrix_Plot.png')
        print(f"Saved adjusted Curry correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot sponsor count correlation matrix
    count_matrix = all_df.loc[:,['Golden State Warriors','Rakuten','United Airlines','JPMorgan Chase','Rakuten_Count','UnitedAirlines_Count','Chase_Count']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(count_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Sponsor Count and GSW Sponsor Trends')
    plt.tight_layout()

    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/GSW_Sponsor_Count_Correlation_Matrix_Plot.png')
        print(f"Saved Sponsor Count correlation matrix.")
        plt.close()
    else:
        plt.plot()

    # plot time adjusted sponsor count correlation matrix
    count_adjusted_matrix = all_df.loc[:,['GoldenStateWarriors_adjusted','Rakuten_adjusted','UnitedAirlines_adjusted','JPMorganChase_adjusted','Rakuten_Count','UnitedAirlines_Count','Chase_Count']]

    plt.figure(figsize=(10,8))
    sns.color_palette("coolwarm", as_cmap=True)
    sns.heatmap(count_adjusted_matrix.corr(),annot=True,fmt=".2f",cmap="coolwarm_r",vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Sponsor Count and GSW Sponsor Trends')
    plt.tight_layout()

    if not notebook_plot:
        # save plot to results folder if not for jupyter notebook
        plt.savefig(f'{result_dir}/Adjusted_GSW_Sponsor_Count_Correlation_Matrix_Plot.png')
        print(f"Saved adjusted Sponsor Count correlation matrix.")
        plt.close()
    else:
        plt.plot()

def run_regression(datasets:dict, reg_formula):
    for data_range, dataset in datasets.items():
        model = smf.ols(formula=reg_formula, data = dataset)
        results = model.fit()

        r_squared = round(float(results.rsquared),3)
        t_test = results.t_test(np.eye(len(results.params)))

        # return results
        print(f"{data_range} R Squared: {r_squared}\n{t_test}")